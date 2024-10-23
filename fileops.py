import os
import shutil
import subprocess
import shutil
import tarfile
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

path = '/home/ljp238/.local/share/Trash/'
path = "/media/ljp238/12TBWolf/.Trash-1001"
path = "/home/ljp238/.local/share/Trash/files"
path = "/home/ljp238/.local/share/Trash/files//"


def compress_to_tar(source_path, output_path):
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(source_path, arcname=os.path.basename(source_path))

def tarfile_extractall(tar_path,outdir):
    with tarfile.open(tar_path, 'r') as tf:
        tf.extractall(path=outdir)
    print('All files extracted')



def copy_file(source, destination, threshold):
  try:
      file_size = os.path.getsize(source)
      if file_size > threshold:
          # Use rsync for large files
          subprocess.run(['rsync', '-avh', source, destination], check=True)
      else:
          # Use shutil for smaller files
          shutil.copy2(source, destination)
      #print(f"File copied successfully from {source} to {destination}")
      print("File copied successfully")
  except Exception as e:
      print(f"An error occurred while copying the file: {e}")

def move_file(source, destination, threshold):
  try:
      file_size = os.path.getsize(source)
      if file_size > threshold:
          # Use rsync for large files, then remove the source
          subprocess.run(['rsync', '-avh', source, destination], check=True)
          os.remove(source)
      else:
          # Use shutil for smaller files
          shutil.move(source, destination)
      #print(f"File moved successfully from {source} to {destination}")
      print("File copied successfully")
  except Exception as e:
      print(f"An error occurred while moving the file: {e}")





def delete_file(file_path):
  try:
      os.remove(file_path)
  except Exception as e:
      print(f"Error deleting file {file_path}: {e}")

def delete_directory(dir_path):
  try:
      os.rmdir(dir_path)
  except Exception as e:
      print(f"Error deleting directory {dir_path}: {e}")

def remove_directory_and_files(directory_path):
  try:
      # Collect all files and directories
      files_to_delete = []
      dirs_to_delete = []
      for root, dirs, files in os.walk(directory_path, topdown=False):
          files_to_delete.extend([os.path.join(root, name) for name in files])
          dirs_to_delete.extend([os.path.join(root, name) for name in dirs])

      # Delete files in parallel
      with ThreadPoolExecutor() as executor:
          futures = {executor.submit(delete_file, file_path): file_path for file_path in files_to_delete}
          for future in tqdm(as_completed(futures), total=len(futures), desc="Deleting files"):
              future.result()  # This will raise any exceptions caught during execution

      # Delete directories in parallel
      with ThreadPoolExecutor() as executor:
          futures = {executor.submit(delete_directory, dir_path): dir_path for dir_path in dirs_to_delete}
          for future in tqdm(as_completed(futures), total=len(futures), desc="Deleting directories"):
              future.result()  # This will raise any exceptions caught during execution

      # Finally, delete the root directory
      shutil.rmtree(directory_path)
      print(f"Directory {directory_path} deleted successfully.")
  except FileNotFoundError:
      print(f"Directory {directory_path} not found.")
  except Exception as e:
      print(f"Error deleting directory {directory_path}: {e}")



import os
import tarfile
import gzip
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor


def delete_files_and_directories(directory):
    """
    Recursively deletes files and directories within the specified directory.
    
    Parameters:
    - directory: The path to the directory to be deleted.
    """
    try:
        for root, dirs, files in os.walk(directory, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(directory)
        print(f"Successfully deleted {directory} and its contents.")
    except Exception as e:
        print(f"An error occurred while deleting {directory}: {e}")

def copy_files(src, dst):
    dst = os.path.join(dst,src.split('/')[-2])
    os.makedirs(dst, exist_ok=True)
    
    try:
        # Using tar for faster copying
        tar_command = ['tar', 'cf', '-', '-C', src, '.']
        tar_process = subprocess.Popen(tar_command, stdout=subprocess.PIPE)

        # Extracting files into destination directory
        tar_extract_command = ['tar', 'xf', '-', '-C', dst]
        subprocess.check_call(tar_extract_command, stdin=tar_process.stdout)
        tar_process.wait()

        # Synchronize directories using rsync for incremental syncing
        rsync_command = ['rsync', '--info=progress2', '-auvz', src, dst]
        subprocess.check_call(rsync_command)

        print("Files copied successfully.")
        print(dst)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def extract_tarball(source, destination):
    """
    Extract a tarball (.tar or .tar.gz) to a specified destination.
    
    Args:
        source (str): Path to the tarball file to be extracted.
        destination (str): Directory path where the contents will be extracted.
    """
    # Check if the source file exists
    if not os.path.exists(source):
        print(f"Error: {source} does not exist.")
        return
    
    # Check if the destination directory exists, if not create it
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    try:
        # Check if the source is a tar.gz file
        if source.endswith('.tar.gz'):
            with tarfile.open(source, "r:gz") as tar:
                tar.extractall(path=destination)
            print(f"Tarball extracted successfully to {destination}")
        # Check if the source is a tar file
        elif source.endswith('.tar'):
            with tarfile.open(source, "r") as tar:
                tar.extractall(path=destination)
            print(f"Tarball extracted successfully to {destination}")
        else:
            print("Unsupported file format. The source file must end with '.tar' or '.tar.gz'.")
    except Exception as e:
        print(f"Error extracting tarball: {e}")

def create_tarball(source, destination):
    """
    Create a tarball from a directory or file.
    
    Args:
        source (str): Path to the directory or file to be tarred.
        destination (str): Path to save the tarball.
    """
    # Check if the source exists
    if not os.path.exists(source):
        print(f"Error: {source} does not exist.")
        return
    
    # Check if the destination directory exists, if not create it
    destination_dir = os.path.dirname(destination)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    try:
        with tarfile.open(destination, "w") as tar:
            # Add the source to the tarball
            tar.add(source, arcname=os.path.basename(source))
        print(f"Tarball created successfully at {destination}")
    except Exception as e:
        print(f"Error creating tarball: {e}")


def linux_copy(patha, pathb):
    os.makedirs(pathb, exist_ok=True)
    cmd = f'cp -r {patha} {pathb}'
    print(cmd)
    os.system(cmd)
    print('finished')
    print('copiera.py')


def tarfile_extractall(tar_path,outdir):
    with tarfile.open(tar_path, 'r') as tf:
        tf.extractall(path=outdir)
    print('All files extracted')


def tarfile_compress(source_path, output_path):
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(source_path, arcname=os.path.basename(source_path))


