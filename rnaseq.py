__author__ = 'Alex H Wagner'

from model import GMSModel


class RNASeq(GMSModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gms_type = 'rna-seq'

    @staticmethod
    def show_values():
        v = {'id': 'id',
             'last_build_id': 'last_succeeded_build.id',
             'last_build_dir': 'last_succeeded_build.data_directory',
             'subject_common_name': 'subject.common_name',
             'individual_common_name': 'individual_common_name'}
        return v

if __name__ == '__main__':
    r = RNASeq('e570f1bae29048348bf0f1d078ebf8e8')
    r.update()
    print(r.last_build_dir)