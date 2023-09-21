import numpy as np 
import libosf
from datetime import datetime
import matplotlib.pyplot as plt
from argparse import ArgumentParser

def find_max():
    with libosf.read_file(filename) as f:
        samples = np.array(f.get_samples_by_name(['CAN1.ADC104']))

    plt.plot((samples[1] / 1_000 ** 3).astype(np.datetime64), samples[0])
    plt.show()

find_max()


def main():
    parser = ArgumentParser('numpy to csv example', description='pass an file or directory to dump to a csv file')
    parser.add_argument('-i', action='store', dest='input')

    
