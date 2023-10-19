import numpy as np
import libosf
from argparse import ArgumentParser
import pandas as pd
from pathlib import Path
import sys

EXAMPLE_DIR = Path(__file__).absolute().parent
OSF_FILE = EXAMPLE_DIR.joinpath("example.osf")


def main(argv: list[str]):
    parser = ArgumentParser(
        "numpy to csv example",
        description="pass an file or directory to dump to a csv file",
    )
    parser.add_argument("-i", action="store", dest="input")
    parser.add_argument("-c", action="append", dest="channels")

    args = parser.parse_args()
    if not args.input:
        print("You need to specify a file or directory via the -i flag")
        parser.print_help()
        return
    if not args.channels:
        print("You need to specify atleast one channel via the -c flag")
        parser.print_help()
        return

    path = Path(args.input)
    print(path)

    if path.is_file():
        with libosf.read_file(path) as osf_file:
            samples = osf_file.get_samples(args.channels)
            data = {"ts_n": samples[0], "value": samples[1]}
            df = pd.DataFrame(data=data)
            with open(
                f"{path.with_suffix('').with_suffix('.csv').absolute()}", "w+"
            ) as f:
                f.write("This is a great line\n")
                df.to_csv(f, sep=";")
    elif path.is_dir():
        for child in path.iterdir():
            with libosf.read_file(path) as osf_file:
                samples = osf_file.get_samples(args.channels)
                data = {"ts_n": samples[0], "value": samples[1]}
                df = pd.DataFrame(data=data)
                with open(
                    f"{child.with_suffix('').with_suffix('.csv').absolute()}", "w+"
                ) as f:
                    f.write("This is a great line\n")
                    df.to_csv(f, sep=";")
    else:
        print("Can not read in anything other than a file or directory")


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except RuntimeError as e:
        print(f"err: {e}")
