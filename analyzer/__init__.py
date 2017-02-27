import asyncio
import logging

import newrelic.agent
import os

from analyzer.services import OLXApartmentsParsingService

newrelic_conf = os.path.normpath(os.getcwd() + "/newrelic.ini")
newrelic.agent.initialize(config_file=newrelic_conf, environment="development")

loop = asyncio.get_event_loop()

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s \t%(levelname)s\t%(message)s")

logger = logging.getLogger(__name__)

base_url = "https://www.olx.ua/nedvizhimost/arenda-kvartir/dolgosrochnaya-arenda-kvartir/lvov/?search%5Bphotos%5D=1&search%5Bdistrict_id%5D=135&min_id=364828536"

if __name__ == "__main__":
    try:
        service = OLXApartmentsParsingService(base_url=base_url, loop=loop)
        loop.run_until_complete(service.process(pages=50))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
