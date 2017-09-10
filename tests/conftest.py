from pytest import fixture


@fixture(scope="session")
def config():
    return dict(host="mongodb",
                port=27017,
                db_name="default")
