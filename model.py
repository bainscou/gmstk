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

    def show_values(self):
        raise NotImplementedError('Need a show_values method for {0}.'.format(type(self)))

    def update(self):
        vd = self.show_values()
        keys = sorted(vd)
        v_call = ','.join([vd[x] for x in keys])
        c = 'genome model {0} list --noheaders --filter id={1} --show {2}'.format(self.gms_type, self.model_id, v_call)
        r = self.linus.command(c)
        d = dict(zip(keys, r.split()))
        for k in keys:
            setattr(self, k, d[k])
