import src.move as sut


class TestSsh(object):
    def test_connect_to_esling(self):
        client = sut.connect_to_esling()
        assert client is not None
        client.close()
