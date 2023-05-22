from os import listdir, rename
from os.path import isfile, join
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()


def get_final_filename(f: str) -> str:
    f = f.split(".")
    filename = ".".join(f[0:-1])
    processed_file_name = filename + os.environ.get("DEST_TYPE")
    return processed_file_name


# return file extension. pdf or epub or mobi
def get_file_extension(f: str) -> str:
    return f.split(".")[-1]


# list of extensions that needs to be ignored.
ignored_extensions = ["pdf"]

# here all the downloaded files are kept
source_path: str = os.environ.get("SOURCE_PATH")

# path where converted files are stored
dest_path: str = os.environ.get("DEST_PATH")

raw_files: list[str] = [f for f in listdir(source_path) if isfile(join(source_path, f))]
converted_files: list[str] = [
    f for f in listdir(dest_path) if isfile(join(dest_path, f))
]

for f in raw_files:
    final_file_name = get_final_filename(f)
    extension = get_file_extension(f)
    if final_file_name not in converted_files and extension not in ignored_extensions:
        print("Converting : " + f)
        try:
            subprocess.call(
                ["ebook-convert", source_path + f, dest_path + final_file_name]
            )
        except Exception as e:
            print(e)
    else:
        print("Already exists : " + final_file_name)
