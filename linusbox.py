__author__ = 'Alex H Wagner'
import paramiko
import time
import warnings
from .config import *


KNOWN_HOSTS = HOME + "/.ssh/known_hosts"
# Consider rewriting this with the fabric module once it is compatible with 3.x


class LinusBox:

    def __init__(self, name=LINUSNAME, user=USER, port=22):
        self.name = name
        self.user = user
        self.port = port
        self._client = paramiko.SSHClient()
        self._client.get_host_keys().load(KNOWN_HOSTS)
        self._sftp_client = None
        self._terminal = None
        self.cmd_prompt = PROMPT
        self._sep = '===ENDLINUS==='

    def connect(self):
        self._client.connect(self.name, username=self.user, port=self.port)
        self._sftp_client = self._client.open_sftp()
        self._terminal = self._client.invoke_shell()
        try:
            r = self.recv_all(timeout=5, contains=self.cmd_prompt, count=1)
        except TimeoutError as e:
            s = str(e)
            if s:
                a = s.strip().split('~')
                if len(a) > 1 and a[-1]:
                    c = a[-1]
                else:
                    c = s.strip()[-1]
                m = "\nCommand prompt doesn't contain '{0}'.\nConsider changing PROMPT to '{1}' in config.py." \
                    "\nConnection successful.".format(self.cmd_prompt, c)
                warnings.warn(m)
                self.cmd_prompt = c
            else:
                raise TimeoutError('No response from virtual terminal. Check connection.')

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
                    raise TimeoutError(r)
            first = False
            r += self._terminal.recv(1000).decode('utf-8', 'ignore')
        return r

    def open(self, filename):
        remote_file = self._sftp_client.open(filename)
        return remote_file

    def disconnect(self):
        self._sftp_client.close()
        self._client.close()
