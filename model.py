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
        c = 'genome model {0} list --noheaders'.format(self.gms_type)
        if f_call:
            c += ' --filter {0}'.format(f_call)
        if v_call:
            c += ' --show {0}'.format(v_call)
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


class GMSModelGroup(GMSModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.models = []

    def update(self, raw=False):
        """raw=False processes attributes extracted from call response. raw=True returns the call response instead."""
        r = super().update(raw=True)
        if raw:
            return(r)
        keys = sorted(self.show_values)
        for line in r.split('\n'):
            d = dict(zip(keys, line.split()))
            d = {k: v for k, v in d.items() if v != '<NULL>'}
            primary_parent_class = self.__class__.__bases__[0]
            self.models.append(primary_parent_class(**d))

    def __len__(self):
        return len(self.models)

    # def select(self, **kw):
    #     keys = sorted(self.show_values)
    #     result = []
    #     for k in kw:
    #         if k not in keys:
    #             raise KeyError('Invalid key {0}. See self.show_values for keys.'.format(k))
    #         v = kw[k]
    #         try:
    #             d = getattr(self, k)
    #         except AttributeError:
    #             if v is not False:
    #                 return None
    #             else:
    #                 result.append(self.model_ids)
    #                 continue
    #         if v is True:
    #             result.append(set(d))
    #         elif v is False:
    #             result.append(self.model_ids - set(d))
    #         else:
    #             s = set()
    #             for dk in d:
    #                 if d[dk] == v:
    #                     s.add(dk)
    #             result.append(s)
    #     if result:
    #         s = result.pop()
    #         while result:
    #             s &= result.pop()
    #         if s:
    #             return s
    #     return None