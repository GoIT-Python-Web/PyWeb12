"""
Відсортувати файли в папці.
"""

import argparse
import logging
from pathlib import Path
from shutil import copyfile
from multiprocessing import Process, current_process

"""
--source [-s] 
--output [-o] default folder = dist
"""

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

print(parser.parse_args())
args = vars(parser.parse_args())
print(args)

source = Path(args.get("source"))
output = Path(args.get("output"))


def reader_folder(path: Path) -> None:
    print(f"Start {current_process().name} in {path}")
    for el in path.iterdir():
        if el.is_dir():
            inner_process = Process(target=reader_folder, args=(el, ))
            inner_process.start()
        else:
            copy_file(el)


def copy_file(el: Path) -> None:
    ext = el.suffix[1:]
    new_folder = output / ext
    try:
        new_folder.mkdir(parents=True, exist_ok=True)
        copyfile(el, new_folder / el.name)
    except OSError as err:
        logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    pr = Process(target=reader_folder, args=(source, ))
    pr.start()
    pr.join()
    print("Можно видалять стару папку якщо треба")
