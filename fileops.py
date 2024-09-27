import os
import shutil
import subprocess

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


