__author__ = 'Alex H Wagner'

from model import GMSModel

class ClinSeqModel(GMSModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gms_type = 'clin-seq'
        self.data = None
        self.show_values = {'model_id': 'id',
                            'name': 'name',
                            'subject_common_name': 'subject.common_name',
                            'wgs_id': 'wgs_model.id',
                            'exome_id': 'exome_model.id',
                            'tumor_rnaseq': 'tumor_rnaseq_model.id',
                            'normal_rnaseq': 'normal_rnaseq_model.id'}
        self.filter_values = {'model_groups.id': self.model_id}

    def update(self, raw=False):
        """raw=False processes attributes extracted from call response. raw=True returns the call response instead."""
        r = super().update(raw=True)
        if raw:
            return(r)
        keys = sorted(self.show_values)
        for line in r.split('\n'):
            d = dict(zip(keys, line.split()))
            model_id = d['model_id']
            for k in keys:
                if k == 'model_id':
                    try:
                        self.model_ids.add(model_id)
                    except AttributeError:
                        self.model_ids = set(model_id)
                    continue
                if d[k] == '<NULL>':
                    continue
                try:
                    getattr(self, k)[model_id] = d[k]
                except AttributeError:
                    setattr(self, k, {model_id: d[k]})

    def select(self, **kw):
        keys = sorted(self.show_values)
        result = []
        for k in kw:
            if k not in keys:
                raise KeyError('Invalid key {0}. See self.show_values for keys.'.format(k))
            v = kw[k]
            try:
                d = getattr(self, k)
            except AttributeError:
                if v is not False:
                    return None
                else:
                    result.append(self.model_ids)
                    continue
            if v is True:
                result.append(set(d))
            elif v is False:
                result.append(self.model_ids - set(d))
            else:
                s = set()
                for dk in d:
                    if d[dk] == v:
                        s.add(dk)
                result.append(s)
        if result:
            s = result.pop()
            while result:
                s &= result.pop()
            if s:
                return s
        return None




if __name__ == '__main__':
    c = ClinSeqModel('d7369c20395742568c79bdf0999d1f30')
    c.update()
    r = c.select(tumor_rnaseq=True)
    print(len(r))