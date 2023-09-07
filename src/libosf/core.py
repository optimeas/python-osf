from enum import Enum
import pathlib


class OSFFormat(str, Enum):
    OSF4 = 'osf4'
    OSF3 = 'osf3'


class OSFObject:
    ...


class Channel:
    ...


def read(osf_file: str) -> OSFObject:
    return OSFObject()
