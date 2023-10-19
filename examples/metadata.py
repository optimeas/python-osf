from libosf import read_file
from pathlib import Path

EXAMPLE_DIR = Path(__file__).absolute().parent
OSF_FILE = EXAMPLE_DIR.joinpath("example.osf")


def main():
    with read_file(OSF_FILE) as f:
        metadata = f.metadata()
        print(f"{metadata.creator}")
        channels = f.channels()
        for i, c in enumerate(channels):
            print(f"ch{i}: {c.name}, unit: {c.unit}, type: {c.type}")


if __name__ == "__main__":
    main()
