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
    path = Path(args.input) 
    
    if not args.channels:
        print('You need to specify atleast one channel via the -c flag')
        return

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
    main(sys.argv)
