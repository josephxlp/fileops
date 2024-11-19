from fileops import compress_to_tar
from concurrent.futures import ProcessPoolExecutor
import os
from upaths import rsdata_dpath


data_name = "SENTINEL2"
to_dpath = f"{rsdata_dpath}/compressed/{data_name}"
from_dpath = f"{rsdata_dpath}/data/{data_name}"

if __name__ == '__main__':
    tilenames = os.listdir(from_dpath)
    with ProcessPoolExecutor() as ppe:
        for tilename in tilenames:
            fpath = os.path.join(from_dpath, tilename)
            tpath = os.path.join(to_dpath, tilename+'.tar.gz')

            ppe.submit(compress_to_tar,fpath,tpath)

    print('Done')