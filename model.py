__author__ = 'Alex H Wagner'

import linusbox

class GMSModel:

    linus = linusbox.LinusBox()
    linus.connect()

    def __init__(self, model_id, **kwargs):
        self.model_id = model_id
        self.gms_type = ''
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])
        self.show_values = None
        self.filter_values = {'id': self.model_id}

    def update(self, raw=False):
        """raw=False processes attributes extracted from call response. raw=True returns the call response instead."""
        vd = self.show_values
        keys = sorted(vd)
        v_call = ','.join([vd[x] for x in keys])
        fd = self.filter_values
        f_keys = sorted(fd)
        f_call = ','.join(['{0}={1}'.format(x, fd[x]) for x in f_keys])
        c = 'genome model {0} list --noheaders --filter {1} --show {2}'\
            .format(self.gms_type, f_call, v_call)
        c = 'genome model {0} list --noheaders'.format(self.gms_type)
        if f_call:
            c += ' --filter {0}'.format(f_call)
        if v_call:
            c += ' --show {0}'.format(v_call)
        print(c)
        r = self.linus.command(c, timeout=15)
        if raw:
            return(r)
        d = dict(zip(keys, r.split()))
        self.set_attr_from_dict(d)

    def set_attr_from_dict(self, d):
        for k in d:
            if d[k] == '<NULL>':
                continue
            setattr(self, k, d[k])