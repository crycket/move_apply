import src.ssh as sut


# TODO: Add more tests!!!
class TestSsh(object):
    def test_init_ssh(self):
        ssh = sut.SSH()
        assert ssh is not None
        ssh.send_command('ls')
