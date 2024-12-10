
import os 
from glob import glob 
from tqdm import tqdm

def osremove(path):
     os.remove(path)

def clean_zout_xml_files(zout_xml_dpattern):
  
    zout_xml_files = glob(zout_xml_dpattern)

    # Print the number of files found
    print(f"Found {len(zout_xml_files)} XML files to remove.")

    # Iterate over the files with a progress bar
    for kf in tqdm(zout_xml_files, desc="Removing XML files", unit="file"):
        osremove(kf)
    print('Done')


if __name__ == '__main__':
    from upaths import zout_xml_dpattern
    clean_zout_xml_files(zout_xml_dpattern)