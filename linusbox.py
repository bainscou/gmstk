__author__ = 'Alex H Wagner'
import paramiko
import time

KNOWN_HOSTS = "/Users/awagner/.ssh/known_hosts"


class LinusBox:

    def __init__(self, name='linus202', user='awagner', port=22):
        self.name = name
        self.user = user
        self.port = port
        self._client = paramiko.SSHClient()
        self._client.get_host_keys().load(KNOWN_HOSTS)
        self._sftp_client = None
        self._terminal = None
        self.cmd_prompt = '$ '
        self._sep = '===ENDLINUS==='

    def connect(self):
        self._client.connect(self.name, username=self.user, port=self.port)
        self._sftp_client = self._client.open_sftp()
        self._terminal = self._client.invoke_shell()
        r = self.recv_all(10, self.cmd_prompt, 1)
        self.cmd_prompt = r.strip().split('\n')[-1]

    def command(self, command, timeout=0):
        self._terminal.send(command + '; \\\necho {0}\n'.format(self._sep))
        s = self.recv_all(contains=self._sep, timeout=timeout)
        p, s, c = s.split(self._sep)
        self.cmd_prompt = c.strip()
        return s.strip()

    def recv_all(self, timeout=0, contains=None, count=2):
        t = 0
        interval = 0.1
        first = True
        r = ''
        while first or (contains and r.count(contains) < count):
            while not self._terminal.recv_ready():
                time.sleep(interval)
                t += interval
                if timeout and t > timeout:
                    print(r)
                    raise TimeoutError
            first = False
            r += self._terminal.recv(1000).decode('utf-8')
        return r

    def open(self, filename):
        remote_file = self._sftp_client.open(filename)
        return remote_file

    def disconnect(self):
        self._sftp_client.close()
        self._client.close()


if __name__ == '__main__':
    l = LinusBox()
    l.connect()
    c = 'sleep 1 ; echo "Hello, world."'
    s = l.command(c)
    print(s)