from analyzer.domains import Phone, Offer


def test_phone_domain_obj_creating():
    test_phone = "01234578654"

    phone = Phone(test_phone)

    assert phone.phone == test_phone, phone


def test_phone_domain_obj_repr():
    test_phone = "01234578654"

    phone = Phone(test_phone)

    assert repr(phone) == "Phone: " + test_phone


def test_offer_domain_obj_creating():
    test_str = "test str"
    offer = Offer(title=test_str,
                  price=test_str,
                  address=test_str,
                  data=test_str,
                  url=test_str,
                  images=test_str,
                  description=test_str,
                  offer_id=test_str,
                  room_count=test_str,
                  phones=test_str)

    assert offer.title == test_str
    assert offer.price == test_str
    assert offer.address == test_str
    assert offer.data == test_str
    assert offer.url == test_str
    assert offer.images == test_str
    assert offer.description == test_str
    assert offer.offer_id == test_str
    assert offer.room_count == test_str
    assert offer.phones == test_str


def test_offer_domain_obj_repr():
    test_str = "test str"

    expected_repr = "#{0}\n\tTitle: {0}" \
                    "\n\tPhone: {0}" \
                    "\n\tAddress: {0}\n\tPrice: {0}" \
                    "\n\tData: {0}\n\tUrl: {0}" \
                    "\n\tRoom count: {0}\n\tImages count: {1}" \
                    "\n".format(test_str, len(test_str))

    offer = Offer(title=test_str,
                  price=test_str,
                  address=test_str,
                  data=test_str,
                  url=test_str,
                  images=test_str,
                  description=test_str,
                  offer_id=test_str,
                  room_count=test_str,
                  phones=test_str)

    assert repr(offer) == expected_repr
