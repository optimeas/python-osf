import numpy as np 
import libosf
from argparse import ArgumentParser
import pandas as pd
from pathlib import Path
import sys
import os


def main(argv: list[str]):
    parser = ArgumentParser('numpy to csv example', description='pass an file or directory to dump to a csv file')
    parser.add_argument('-i', action='store', dest='input')
    parser.add_argument('-c', action='append', dest='channels')

    args = parser.parse_args()
    if not args.input:
        print('You need to specify a file or directory via the -i flag')
        parser.print_help()
        return
    
    if not args.channels:
        print('You need to specify atleast one channel via the -c flag')
        parser.print_help()
        return

    path = Path(args.input) 

    if path.is_file():
        with libosf.read_file(path) as f:
            samples = f.get_samples_by_name(args.channels)
            data = {
                    'ts_n': samples[0],
                    'value': samples[1],
                    'ch_index': samples[2]
            }
            df = pd.DataFrame(data=data)
            df.to_csv('output.csv')
            return
    if path.is_dir():
        result_array = None
        for child in path.iterdir():
            samples = f.get_samples_by_name(args.channels)
            data = {
                    'ts_n': samples[0],
                    'value': samples[1],
                    'ch_index': samples[2]
            }
            df = pd.DataFrame(data=data)

        df.to_csv(f'{child.with_suffix("").with_suffix(".csv").absolute()}')
        
    else:
        print('Can not read in anything other than a file or directory')

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except RuntimeError as e:
        print(f'err: {e}')
