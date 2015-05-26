__author__ = 'Alex H Wagner'

from gmstk.model import GMSModel
from biotk.rnaseq import RNASeq as RNAdf
import pandas


class RNAModel(GMSModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gms_type = 'rna-seq'
        self.data = None
        self.show_values =  {'id': 'id',
                             'last_build_id': 'last_succeeded_build.id',
                             'last_build_dir': 'last_succeeded_build.data_directory',
                             'subject_common_name': 'subject.common_name',
                             'individual_common_name': 'individual_common_name'}

    def load_gene_expr(self, df=None, range_dict=None):
        if df is None:
            with self.linus.open(self.last_build_dir + '/expression/genes.fpkm_tracking') as f:
                df = pandas.read_csv(f, sep="\t")
                df = df[['tracking_id', 'FPKM']]
                df.columns = ['id', 'FPKM']
                df.set_index('id')
        if range_dict:
            self.data = RNAdf(fpkm_df=df, range_dict=range_dict)
        else:
            with self.linus.open(self.last_build_dir + '/expression/transcripts.gtf') as f:
                self.data = RNAdf(fpkm_df=df, trx_gtf=f)


if __name__ == '__main__':
    import pickle
    r = RNAModel('e570f1bae29048348bf0f1d078ebf8e8')
    r.update()
    with open('/Users/awagner/Workspace/python/biotk/data/gtf_dict.pickle', 'rb') as f:
        d = pickle.load(f)
    # r.load_gene_expr(range_dict=d)
    # with open('/Users/awagner/Workspace/python/biotk/data/fpkm_df.pickle', 'wb') as f:
    #     pickle.dump(r.data.df, f)
    with open('/Users/awagner/Workspace/python/biotk/data/fpkm_df.pickle', 'rb') as f:
        df = pickle.load(f)
    r.load_gene_expr(df, d)