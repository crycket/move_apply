import src.ssh as sut


class TestSsh(object):
    def test_init_ssh(self):
        ssh = sut.SSH()
        assert ssh is not None
        ssh.send_command('ls')
