from enum import Enum
from attrs import define, field
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

    first_line = read_until(file, b'\n').decode()

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
    def __init__(self, file, magic_header):
        self._file = file
        self._magic_header = magic_header

    @property
    def osf_version(self):
        return self._magic_header['osf_format']

    @property
    def header_size(self) -> int:
        return self._magic_header['header_size']

    @property
    @abstractmethod
    def version_supported(self) -> bool:
        ...


""""
FIXME: 
Could this the metadata be autoconstructed? Perhaps only define defaults for the fields and then construct if its 
found inside the xml elements attributes?
"""


@define
class Metadata:
    creator = field(default='')
    created_utc = field(default='')
    tag = field(default='')
    namespacesep = field(default='')
    channel_count = field(default=0)
    infos = field(default={})


def construct_metadata(element: ET.Element) -> Metadata:
    count = int(element.find('.//channels').attrib["count"])
    infos_element = element.find('.//infos')
    infos = {}
    if infos_element is not None:
        for info_element in infos_element:
            if info_element.attrib.get('datatype', '') != 'string':
                continue
            try:
                key = info_element.attrib['name']
                value = info_element.attrib['value']
                infos[key] = value
            except KeyError:
                continue

    # FIXME: build an dictonary with catching of KeyErrors and pass to Metadata constructor
    metadata = Metadata(
        creator=element.attrib["creator"],
        created_utc=element.attrib["created_utc"],
        tag=element.attrib["tag"],
        namespacesep=element.attrib['namespacesep'],
        channel_count=count,
        infos=infos
    )

    return metadata


class OSF4Object(OSFObjectBase):
    def __init__(self, stream, magic_header):
        super().__init__(stream, magic_header)

        self._xml_header = self._read_xml_header()

    @property
    def version_supported(self) -> bool:
        return True

    def channels(self) -> list[Channel4]:
        elements = self._xml_header.findall('.//channel')

        return [Channel4(element) for element in elements]

    def metadata(self):
        return construct_metadata(self._xml_header)

    def _read_xml_header(self) -> ET.Element:
        self._file.seek(self._magic_header['magic_length'])
        data = self._file.read(self._magic_header['header_size'])
        return ET.fromstring(data)


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
