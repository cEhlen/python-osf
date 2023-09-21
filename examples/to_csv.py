import numpy as np 
import libosf
from argparse import ArgumentParser
import pandas as pd
from pathlib import Path
import sys


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
            df = pd.DataFrame(np.array(f.get_samples_by_name(args.channels)))
            df.to_csv('output.csv')
            return
    if path.is_dir():
        result_array = None
        for child in path.iterdir():
            print(child)
            with libosf.read_file(child) as f:
                if result_array is None:
                    result_array = np.array(f.get_samples_by_name(args.channels)).T

                result_array = np.concatenate((result_array, np.array(f.get_samples_by_name(args.channels)).T))
        
        pd.DataFrame(result_array).to_csv('output.csv')
        
    else:
        print('Can not read in anything other than a file')

if __name__ == '__main__':
    main(sys.argv)