from libosf import read_file, Channel, Location
from pathlib import Path
import pandas as pd
import numpy as np
import argparse
import sys

EXAMPLE_DIR = Path(__file__).absolute().parent
EXAMPLE_OSF_FILE = str(EXAMPLE_DIR.joinpath("example.osf"))


def main():
    files = sys.argv[1:]
    if len(files) == 0: # No parameters passed
        files = [EXAMPLE_OSF_FILE]
    for file in files:
        with read_file(file) as f:
            metadata = f.metadata()
            channels = f.channels()

            print(f"creator: {metadata.creator}")
            print(f"Channel count: {len(channels)}")
            print("")

            samples = f.get_samples((c.name for c in channels))
            samples = pd.DataFrame(
                {"index": samples[2], "value": samples[0], "ts": samples[1]}
            )
            samples = samples.astype({"ts": "datetime64[ns]"})
            for i, c in enumerate(channels):
                current_samples = samples[samples["index"] == c.index]
                print("")
                print(f"{i}: name: {c.name}")
                print(f"{i}: unit: {c.unit}")
                print(f"{i}: type: {c.type}")

                if c.type == "gpslocation":
                    gps_list = current_samples['value'].values.tolist()
                    df = pd.DataFrame(columns=["Longitude", "Latitude", "Altitude"])
                    df[df.columns] = gps_list
                    current_samples = pd.merge(current_samples["ts"], df, how="cross")
                    print(f"{i}: length: {current_samples.shape[0]}")
                    print("")
                    print(current_samples[["ts", "Longitude", "Latitude", "Altitude"]])
                else:
                    print(f"{i}: length: {current_samples.shape[0]}")
                    print("")
                    print(current_samples[["ts", "value"]])


if __name__ == "__main__":
    main()
