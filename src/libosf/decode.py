from enum import Enum
from attrs import define
from array import array

from libosf import Channel4

byteorder = 'little'


def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder=byteorder)


@define
class BlobInfo:
    offset: int
    size: int


metadata_bin = {
    'control': BlobInfo(0, 1),
    'num_samples': BlobInfo(1, 4),
    'text_sample_length': BlobInfo(9, 4)

}


class MetaInfo(Enum):
    bcMessageEvent = 4
    bcAbsTimeStampData = 8


def decode_metadata(metadata_array: array, data_blob_start) -> dict:
    metadata_enum = metadata_array[0] - 128 if metadata_array[0] >= 128 else metadata_array[0]
    control_bit = metadata_array[0] >> 7

    result = dict()
    if metadata_enum == MetaInfo.bcAbsTimeStampData:
        if control_bit == 1:
            result['sample_start'] = (data_blob_start + 1 + 4)
            result['num_samples'] = int.from_bytes(metadata_array[1:5].to_bytes(), byteorder=byteorder)
        else:
            result['sample_start'] = (data_blob_start + 1)
            result['num_samples'] = 1

    elif metadata_enum == 4:
        binary_data = metadata_array[8:16]
        result['sample_start'] = (data_blob_start + 1 + 8 + 4)
        result['num_samples'] = 1
        byte_stream.seek((data_blob_start + 1 + 8))
        binary_data = byte_stream.read(4)
        result['sample_length'] = int.from_bytes(binary_data,
                                                 byteorder='little') - 1  # TODO: Warum wird ein extra Byte ausgelsen?
    else:
        raise Exception('metadata type not supported')

    return result


def convert_channels_to_array(channels: list[Channel4]) -> array:
    result = array('l', [0]) * len(channels)
    for ch in channels:
        result[ch.index] = ch.length_blob_size

    return result


def read_sample_blob(stream, channel_info_array: array, start) -> tuple[array, int]:
    stream.seek(start)
    ch_index = bytes_to_int(stream.read(2))
    size_of_length_value = channel_info_array[ch_index]
    blob_length = bytes_to_int(stream.read(size_of_length_value))
    return array('b', stream.read(blob_length)), stream.tell()
