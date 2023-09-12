from enum import Enum
from attrs import define
from array import array
from libosf import Channel4
import numpy as np
from struct import unpack

byteorder = 'little'

CH_STRUCT_INDEX = 0
CH_STRUCT_TYPELENGTH = 1
CH_STRUCT_TYPE = 2


class ChannelConversionType(Enum):
    int = 0
    uint = 1
    float = 2
    double = 3
    string = 4
    boolean = 5


def get_conversion_type(type_string):
    match type_string:
        case 'int64' | 'int32' | 'int16' | 'int8':
            return ChannelConversionType.int.value
        case 'uint64'|  'uint32'|  'uint16'|  'uint8'| 'bool':
            return ChannelConversionType.uint.value
        case 'float':
            return ChannelConversionType.float.value
        case 'double':
            return ChannelConversionType.double.value
        case 'string':
            return ChannelConversionType.string.value
        case 'bool':
            return ChannelConversionType.boolean.value




type_length = {
    'int64': 8,
    'int32': 4,
    'int16': 2,
    'int8': 1,
    'double': 8,
    'float': 4,
    'uint64': 8,
    'uint32': 4,
    'uint16': 2,
    'uint8': 1,
    'bool': 1,
    'string': 0
}


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


def encode_datablob(metadata_array: array, ch_info) -> tuple[array, array]:
    metadata_enum = metadata_array[0] - 128 if metadata_array[0] >= 128 else metadata_array[0]
    control_bit = metadata_array[0] >> 7

    result = dict()
    if metadata_enum == MetaInfo.bcAbsTimeStampData.value:
        result['epoch_size'] = 8
        if control_bit == 1:
            result['sample_start'] = 1 + 4
            result['num_samples'] = int.from_bytes(metadata_array[1:5].to_bytes(), byteorder=byteorder)
        else:
            result['sample_start'] = 1
            result['num_samples'] = 1
    elif metadata_enum == MetaInfo.bcMessageEvent.value:
        binary_data = metadata_array[8:16]
        result['ts_epoch'] = binary_data.encode()
        result['sample_start'] = 1 + 8 + 4
        result['num_samples'] = 1
        binary_data = metadata_array[9:13]
        result['sample_length'] = bytes_to_int(binary_data)
    else:
        raise Exception('metadata type not supported')

    value_result = []
    ts_result = []
    index = result['sample_start']
    epoch_size = result['epoch_size']
    sample_length = ch_info[CH_STRUCT_TYPELENGTH]
    full_length = epoch_size + sample_length

    match ch_info[CH_STRUCT_TYPE]:
        case 0:
            while index < len(metadata_array):
                ts_result.append(bytes_to_int(metadata_array[index:index + epoch_size]))
                value_result.append(bytes_to_int(metadata_array[index + epoch_size:index + full_length]))
                index = index + full_length
        case 1:
            while index < len(metadata_array):
                ts_result.append(bytes_to_int(metadata_array[index:index + epoch_size]))
                value_result.append(int.from_bytes(metadata_array[index + epoch_size:index + full_length], byteorder=byteorder,
                                                   signed=False))
                index = index + full_length
        case 2:
            while index < len(metadata_array):
                ts_result.append(bytes_to_int(metadata_array[index:index + epoch_size]))
                value_result.append(unpack('<f',metadata_array[index + epoch_size:index + full_length])[0])
                index = index + full_length
        case 3:
            while index < len(metadata_array):
                ts_result.append(bytes_to_int(metadata_array[index:index + epoch_size]))
                value_result.append(unpack('<d',metadata_array[index + epoch_size:index + full_length])[0])
                index = index + full_length
        case 4:
            ts_result.append(result['ts_epoch'])
            value_result.append(metadata_array[index:].decode())
        case 5:
            while index < len(metadata_array):
                ts_result.append(bytes_to_int(metadata_array[index:index + epoch_size]))
                value_result.append(unpack('?',metadata_array[index + epoch_size:index + full_length])[0])
                index = index + full_length

    return value_result, ts_result


def convert_channels_to_array(channels: list[Channel4]) -> np.ndarray:
    result = np.empty((len(channels), 3), dtype=np.int32)
    for ch in channels:
        result[ch.index][CH_STRUCT_INDEX] = ch.length_blob_size
        result[ch.index][CH_STRUCT_TYPELENGTH] = type_length[ch.type]
        result[ch.index][CH_STRUCT_TYPE] = get_conversion_type(ch.type)

    return result


def read_sample_blob(stream, channel_info_array: array, start) -> tuple[array, int, tuple]:
    stream.seek(start)
    ch_index = bytes_to_int(stream.read(2))
    size_of_length_value = channel_info_array[ch_index][CH_STRUCT_INDEX]
    blob_length = bytes_to_int(stream.read(size_of_length_value))
    return array('b', stream.read(blob_length)), stream.tell(), (
        ch_index, channel_info_array[ch_index][CH_STRUCT_TYPELENGTH],
        channel_info_array[ch_index][CH_STRUCT_TYPE])
