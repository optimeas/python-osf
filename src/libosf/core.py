import xml.etree.ElementTree
from enum import Enum
import pathlib
from attrs import define
from contextlib import contextmanager
from abc import ABC, abstractmethod
from typing import BinaryIO
from xml.etree import ElementTree as ET


class OSFFormat(str, Enum):
    OSF4 = 'osf4'
    OSF3 = 'osf3'
    UNKNOWN = 'unknown'


def osf_format_from_string(format_string) -> OSFFormat:
    if format_string in ['OCEAN_STREAM_FORMAT4', 'OSF4']:
        return OSFFormat.OSF4
    elif format_string in ['OCEAN_STREAM_FORMAT3']:
        return OSFFormat.OSF3
    else:
        return OSFFormat.UNKNOWN


def read_until(byte_stream: BinaryIO, bytes_value: bytes) -> bytes:
    result = b''
    while c := byte_stream.read(1):
        if bytes_value[0] == c[0]:
            break
        result = result + c

    return result


def get_magic_header(file: BinaryIO) -> dict:
    old_pos = file.tell()
    file.seek(0)

    first_line = read_until(file, b'\n').decode().strip()

    format_string: str
    size_string: str
    try:
        format_string, size_string = first_line.split(' ')
    except ValueError:
        format_string = ' '
        size_string = 0

    file.seek(old_pos)
    return {
        'osf_format': osf_format_from_string(format_string),
        'header_size': int(size_string),
        'magic_length': len(first_line) + 1
    }


class Channel4:
    def __init__(self, element: ET.Element):
        attr = element.attrib
        self.name = attr['name']
        self.unit = attr['physicalunit']
        self.index = int(attr['index'])
        self.length_blob_size = int(attr['sizeoflengthvalue'])


class OSFObjectBase(ABC):
    def __init__(self, file, header):
        self._file = file
        self._header = header

    @property
    def osf_version(self):
        return self._header['osf_format']

    @property
    def header_size(self) -> int:
        return self._header['header_size']

    @property
    @abstractmethod
    def version_supported(self) -> bool:
        ...

    def channels(self) -> list:
        ...

    def _read_xml_header(self) -> ET.Element:
        self._file.seek(self._header['magic_length'])
        data = self._file.read(self._header['header_size'])
        return ET.fromstring(data)


class OSF4Object(OSFObjectBase):
    @property
    def version_supported(self) -> bool:
        return True

    def channels(self) -> list[Channel4]:
        elements = self._read_xml_header().findall('.//channel')

        return [Channel4(element) for element in elements]


class OSF3Object(OSFObjectBase):
    @property
    def version_supported(self):
        return False


class OSFUNKOWNObject(OSFObjectBase):
    @property
    def version_supported(self):
        return False


@contextmanager
def read_file(osf_file: str):
    file = open(osf_file, 'rb')

    try:
        header = get_magic_header(file)

        osf_object: OSFObjectBase = None
        match header['osf_format']:
            case OSFFormat.OSF3:
                osf_object = OSF3Object(file, header)
            case OSFFormat.OSF4:
                osf_object = OSF4Object(file, header)
            case OSFFormat.UNKNOWN:
                osf_object = OSFUNKOWNObject(file, header)

        yield osf_object
    finally:
        file.close()
