import asyncio
import json
import random
import string
import time

import logging

import aiohttp
from bs4 import BeautifulSoup

from analyzer.factories import OfferFactory, PhoneFactory
from analyzer.storages import OfferStorage, PhoneStorage

logger = logging.getLogger(__name__)


class Cache:
    _cache = dict()

    def get(self, key):
        return self._cache.get(key)

    def put(self, key, value):
        self._cache[key] = value

    def exists(self, key):
        return key in self._cache.keys()


class OLXSearchUrlBuilder:
    page_url_param = "&page={page_number}"

    def __init__(self, base_url: str):
        self._base_url = base_url

    def get_base_url(self):
        return self._base_url

    def get_page_url(self, page_number: int):
        return self._base_url + self.page_url_param.format(page_number=page_number)


class ControlledHttpClient:
    def __init__(self, initial_call_per_interval, interval):
        self.requests_per_interval = initial_call_per_interval
        self.interval = interval
        self._requests_count = 0
        self._retried_requests = 0
        self._time_marker = time.time() + self.interval
        self.lock = asyncio.Lock()
        self.cache = Cache()

    async def call(self, method, path, headers=()):
        if self.cache.exists((method, path,)):
            logger.info("Returned from cache {}".format(path))
            return self.cache.get((method, path,))
        await self.lock.acquire()
        if self._requests_count < self.requests_per_interval and self._time_marker > time.time():
            self._requests_count += 1
            logger.debug("Do call number {}".format(self._requests_count))
            self.lock.release()
            return await self._do_call(method, path, headers)
        else:
            time_to_sleep = self._time_marker - time.time()
            logger.info("Waiting {} seconds.".format(time_to_sleep, self._time_marker))
            await asyncio.sleep(time_to_sleep)
            successful_requests = self._requests_count - self._retried_requests + 5
            logger.info("Call count limit per {}s is {}".format(self.interval, successful_requests))
            self.requests_per_interval = successful_requests
            self._requests_count = 0
            self._retried_requests = 0
            self._time_marker = time.time() + self.interval
            self.lock.release()
            return await self.call(method, path, headers)

    async def _do_call(self, method, path, headers=()):
        uri = "{}#{}".format(path.split("#")[0],
                             ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)).lower())
        logger.debug("Send request to {}".format(path))
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=uri, headers=headers, timeout=2 * 60) as response:
                data = await response.content.read()
                if response.status not in (200, 404):
                    await self.lock.acquire()
                    self._retried_requests += 1
                    self.lock.release()
                    logger.warning("Retry request: {}".format(path))
                    return await self.call(method, path, headers=())
                self.cache.put((method, path,), (response, data))
                return response, data


class OLXApartmentsParsingService:
    http_client = ControlledHttpClient(initial_call_per_interval=20, interval=10)
    phone_url = "https://www.olx.ua/ajax/misc/contact/phone/"

    def __init__(self, base_url, loop):
        self.loop = loop
        self.base_url = base_url
        self.search = OLXSearchUrlBuilder(base_url=self.base_url)
        self.offers_storage = OfferStorage(host="mongodb",
                                           port=27017,
                                           db_name="default",
                                           loop=self.loop)
        self.phones_storage = PhoneStorage(host="mongodb",
                                           port=27017,
                                           db_name="default",
                                           loop=self.loop)

    async def parse_page(self, page_url: str):
        headers = [
            ("User-Agent",
             """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKi
             t/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36""")]

        main_page_response, main_page_data = await self.http_client.call(path=page_url, method="GET", headers=headers)
        soup = BeautifulSoup(main_page_data, 'html.parser')

        content = soup.find("div", attrs={"class": "content"})
        count = 0
        for offer in content.find_all("td", attrs={"class": "offer"}):
            top_part = offer.find("td", attrs={"valign": "top"})
            page_url = top_part.div.h3.a.get("href")
            self.loop.create_task(self.parse_offer(page_url))
            count += 1
        logger.debug("Offers count: {}".format(count))

    async def parse_offer(self, offer_url: str):
        _, offer_data = await self.http_client.call("GET", offer_url)

        offer_page = BeautifulSoup(offer_data, "html.parser")

        price = offer_page.find("div", attrs={"class": "price-label"}).strong.text
        phone_data = offer_page.find("div", attrs={"class": "contact-button", "data-rel": "phone"})
        phones = await self._parse_phones(phone_data)

        offer_detailed_info = offer_page.find("div", attrs={"id": "offerdescription"})

        title = offer_detailed_info.find("div", attrs={"class": "offer-titlebox"}).h1.text
        description = ""
        if offer_detailed_info:
            description = offer_detailed_info.find("div", attrs={"id": "textContent"}).p.text
        room_count = offer_detailed_info.find("th", text="Количество комнат").parent.td.text
        offer_details = offer_detailed_info.find("div", attrs={"class": "offer-titlebox__details"})
        address = offer_details.a.strong.text
        data = offer_details.em.contents[0]
        offer_id = offer_details.em.small.text
        images = [img.get("src", "") for img in offer_detailed_info.find_all("img")]
        phones_insertion_result = await self.phones_storage.insert_many(phones)
        phone_ids = []
        if phones_insertion_result:
            phone_ids = [str(phone_id) for phone_id in phones_insertion_result.inserted_ids]
        offer = OfferFactory.create_offer(
            title=title,
            price=price,
            data=data,
            url=offer_url,
            images=images,
            description=description,
            offer_id=offer_id,
            address=address,
            room_count=room_count,
            phones=phone_ids
        )
        self.loop.create_task(self.offers_storage.insert(offer))

    async def _parse_phones(self, phone_data):
        phones = []
        if phone_data:
            phone_id = phone_data.get("class")[3].split(":")[1].strip("',")
            _, phone_response = await self.http_client.call("GET", self.phone_url + phone_id)
            phones_data_value = json.loads(phone_response.decode()).get("value")
            if "span" not in phones_data_value:
                phones.append(PhoneFactory.create_phone(phones_data_value))
            else:
                phones_parser = BeautifulSoup(phones_data_value, "html.parser")
                for span in phones_parser.find_all("span"):
                    phones.append(PhoneFactory.create_phone(span.text))
        return phones

    async def process(self, pages: int):
        await self.offers_storage.connect()
        await self.phones_storage.connect()
        for i in range(1, pages):
            url = self.search.get_page_url(page_number=i)
            self.loop.create_task(self.parse_page(page_url=url))
