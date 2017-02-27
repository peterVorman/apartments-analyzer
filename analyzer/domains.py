class Offer:
    def __init__(self, title, price, address, data, url, images, description, offer_id, room_count, phones):
        self.price = price
        self.title = title
        self.address = address
        self.data = data
        self.url = url
        self.images = images or []
        self.description = description
        self.offer_id = offer_id
        self.room_count = room_count
        self.phones = phones

    def __repr__(self):
        return "#{}\n\tTitle: {}" \
               "\n\tPhone: {}" \
               "\n\tAddress: {}\n\tPrice: {}" \
               "\n\tData: {}\n\tUrl: {}" \
               "\n\tRoom count: {}\n\tImages count: {}" \
               "\n".format(self.offer_id, self.title,
                           self.phones,
                           self.address, self.price,
                           self.data, self.url,
                           self.room_count, len(self.images))


class Phone:
    def __init__(self, phone):
        self.phone = phone

    def __repr__(self):
        return "Phone: {}".format(self.phone)