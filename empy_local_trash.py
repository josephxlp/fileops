import os
import shutil
from tqdm import tqdm

def delete_all_in_directory(directory_path):
  # Expand the tilde to the full home directory path
  full_path = os.path.expanduser(directory_path)
  
  # List all items in the directory
  try:
      items = os.listdir(full_path)
  except FileNotFoundError:
      print(f"The directory {full_path} does not exist.")
      return
  except PermissionError:
      print(f"Permission denied for accessing {full_path}.")
      return

  # Iterate over each item and delete it with a progress bar
  for item in tqdm(items, desc="Deleting items", unit="item"):
      item_path = os.path.join(full_path, item)
      
      # Check if it's a file or directory
      if os.path.isfile(item_path):
          os.remove(item_path)  # Delete the file
      elif os.path.isdir(item_path):
          shutil.rmtree(item_path)  # Delete the directory and its contents

  print(f"All items in {full_path} have been deleted.")

# Example usage
if __name__ == "__main__":
    delete_all_in_directory("~/.local/share/Trash/files")
    # make it parallel 