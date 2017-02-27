from analyzer.domains import Offer, Phone


class OfferFactory:

    @classmethod
    def create_offer(cls, title, price, address, data, url, images, description, offer_id, room_count, phones):
        price = cls.normalize_text(price)
        title = cls.normalize_text(title)
        address = cls.normalize_text(address)
        data = cls.normalize_text(data)
        if data:
            data = data.split(":в")[1].strip()
        url = url
        description = cls.normalize_text(description)
        offer_id = int(cls.normalize_text(offer_id).split(":")[1])
        room_count = int(cls.normalize_text(room_count))
        phones = phones

        return Offer(
                title=title,
                price=price,
                data=data,
                url=url,
                images=images,
                description=description,
                offer_id=offer_id,
                address=address,
                room_count=room_count,
                phones=phones,
            )

    @staticmethod
    def normalize_text(text):
        return text.replace("\n", "").replace("\t", "").replace("  ", "").strip()


class PhoneFactory:

    @classmethod
    def create_phone(cls, phone):
        return Phone(phone=cls.normalize_phone(phone))

    @classmethod
    def normalize_phone(cls, phone_str):
        normalized_phone = OfferFactory.normalize_text(phone_str)
        return normalized_phone.lstrip("+38").replace(" ", "").replace("-", "")
