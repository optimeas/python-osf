from libosf import read_file, Channel, Location
from pathlib import Path
import numpy as np

EXAMPLE_DIR = Path(__file__).absolute().parent
OSF_FILE = str(EXAMPLE_DIR.joinpath("example.osf"))


def main():
    with read_file(OSF_FILE) as f:
        metadata = f.metadata()
        channels = f.channels()

        print(f"creator: {metadata.creator}")
        print(f"Channel count: {len(channels)}")
        print("")

        for i, c in enumerate(channels):
            print("")
            print(f"{i}: name: {c.name}")
            print(f"{i}: unit: {c.unit}")
            print(f"{i}: type: {c.type}")

            samples: None
            if c.type == "gpslocation":
                v, t, i = f.get_samples([c.name])
                v = [Location.from_tuple(val) for val in v]
                for i, (ts, loc) in enumerate(zip(t,v)):
                    ns = np.datetime64(int(ts), "ns")
                    print(f"{i}: ts= {ns} | y= {loc}")
                    # hint: use loc.latitude for example to process specific coordinates
            else:
                samples: np.ndarray = np.array(f.get_samples([c.name]))

                print(f"{i}: length: {samples.shape[1]}")
                print("")

                # print channel values
                for x in range(samples.shape[1]):
                    ns = np.datetime64(int(samples[1][x]), "ns")
                    print(f"{x}: ts= {ns} | y= {samples[0][x]}")


if __name__ == "__main__":
    main()
