from analyzer.factories import OfferFactory, PhoneFactory


def test_phone_factory_with_clean_number():
    test_phone = "01234567"

    phone = PhoneFactory.create_phone(phone=test_phone)

    assert phone.phone == test_phone


def test_phone_factory_with_dirty_number():
    test_phone = "+38-012-34-56-777"
    expected_phone_number = "0123456777"

    phone = PhoneFactory.create_phone(phone=test_phone)

    assert phone.phone == expected_phone_number


def test_offer_factory_on_clean_data():
    test_str = "sample string for testing"
    test_int = 123456

    offer = OfferFactory.create_offer(title=test_str,
                                      images=test_str,
                                      offer_id="offer_id :{}".format(test_int),
                                      price=test_str,
                                      address=test_str,
                                      url=test_str,
                                      description=test_str,
                                      room_count=str(test_int),
                                      phones=test_str,
                                      data=":в" + test_str)
    assert offer.title == test_str
    assert offer.price == test_str
    assert offer.address == test_str
    assert offer.data == test_str
    assert offer.url == test_str
    assert offer.images == test_str
    assert offer.description == test_str
    assert offer.offer_id == test_int
    assert offer.room_count == test_int
    assert offer.phones == test_str


def test_str_normalizing_of_offer_factory():
    source_str = " \n  A b c  \n\n\t  \t"
    expected_str = "A b c"

    result = OfferFactory.normalize_text(source_str)

    assert result == expected_str


def test_phone_normalizing_of_phone_factory():
    source_str = " \n  +38-099-99-99-999  \n\n\t  \t"
    expected_phone = "0999999999"

    result = PhoneFactory.normalize_phone(source_str)

    assert result == expected_phone
