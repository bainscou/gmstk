__author__ = 'Alex H Wagner'
import paramiko

KNOWN_HOSTS = "/Users/awagner/.ssh/known_hosts"


class LinusBox:

    def __init__(self, name='linus202', user='awagner', port=22):
        self.name = name
        self.user = user
        self.port = port
        self._client = paramiko.SSHClient()
        self._client.get_host_keys().load(KNOWN_HOSTS)
        self._sftp_client = None

    def connect(self):
        self._client.connect(self.name, username=self.user, port=self.port)
        self._sftp_client = self._client.open_sftp()

    def command(self, command):
        stdin, stdout, stderr = self._client.exec_command(command)
        return stdin, stdout, stderr

    def open(self, filename):
        remote_file = self._sftp_client.open(filename)
        return remote_file

    def disconnect(self):
        self._sftp_client.close()
        self._client.close()


if __name__ == '__main__':
    l = LinusBox()
    l.connect()
    stdin, stdout, stderr = l.command('ls')
    for line in stdout:
        print ('... ' + line.strip())
    with l.open('test') as f:
        for line in f:
            print('> ' + line.strip())
    l.disconnect()