__author__ = 'Alex H Wagner'

import paramiko
import time
import warnings
import scp
from gmstk.config import *


KNOWN_HOSTS = HOME + "/.ssh/known_hosts"
# Consider rewriting this with the fabric module once it is compatible with 3.x

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class LinusBox:

    def __init__(self, name=LINUSNAME, user=USER, port=22):
        self._name = name
        self._user = user
        self._port = port
        self._client = paramiko.SSHClient()
        self._client.get_host_keys().load(KNOWN_HOSTS)
        self._scp_client = scp.SCPClient(self._client.get_transport())
        self._sftp_client = None
        self._terminal = None
        self._cmd_prompt = PROMPT
        self._sep = '===ENDLINUS==='

    def connect(self):
        self._client.connect(self._name, username=self._user, port=self._port)
        self._sftp_client = self._client.open_sftp()
        self._terminal = self._client.invoke_shell()
        try:
            self.recv_all(timeout=5, contains=self._cmd_prompt, count=1)
        except TimeoutError as e:
            s = str(e)
            if s:
                a = s.strip().split('~')
                if len(a) > 1 and a[-1]:
                    c = a[-1]
                else:
                    c = s.strip()[-1]
                m = "\nCommand prompt doesn't contain '{0}'.\nConsider changing PROMPT to '{1}' in config.py." \
                    "\nConnection successful.".format(self._cmd_prompt, c)
                warnings.warn(m)
                self._cmd_prompt = c
            else:
                raise TimeoutError('No response from virtual terminal. Check connection.')

    def command(self, command, timeout=5):
        """Returns list of stdout lines and list of stderr lines"""
        print(command)
        self._terminal.send(command + '; \\\necho {0}\n'.format(self._sep))
        r = self.recv_all(contains=self._sep, timeout=timeout)
        s = r.stdout
        p, s, c = s.split(self._sep)
        self._cmd_prompt = c.strip()
        r.stdout = s.strip().splitlines()
        r.stderr = r.stderr.strip().splitlines()
        return r

    def recv_all(self, timeout=0, contains=None, count=2):
        t = 0
        interval = 0.1
        first = True
        e = r = ''
        while first or (contains and r.count(contains) < count):
            while not self._terminal.recv_ready() or self._terminal.recv_stderr_ready():
                time.sleep(interval)
                t += interval
                if timeout and t > timeout:
                    raise TimeoutError(r)
            first = False
            while self._terminal.recv_ready():
                r += self._terminal.recv(1000).decode('utf-8', 'ignore')
            while self._terminal.recv_stderr_ready():
                e += self._terminal.recv_stderr(1000).decode('utf-8', 'ignore')
        return Bunch(stdout=r, stderr=e)

    def open(self, filename):
        remote_file = self._sftp_client.open(filename)
        return remote_file

    def scp_get(self, remote, local, recursive=False, preserve_times=False):
        self._scp_client.get(remote, local, recursive, preserve_times)

    def scp_put(self, local, remote='.', recursive=False, preserve_times=False):
        self._scp_client.put(local, remote, recursive, preserve_times)

    def ls(self, *args):
        return self.command(' '.join(['ls', '-1'] + [str(x) for x in args]))

    def __getattr__(self, item):
        return lambda *args: self.command(' '.join([item] + [str(x) for x in args]))

    def disconnect(self):
        self._sftp_client.close()
        self._client.close()
