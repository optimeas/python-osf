from enum import Enum
import sys
import numpy as np
from xml.etree import ElementTree as ET

byteorder = "little"

CH_STRUCT_INDEX = 0
CH_STRUCT_TYPELENGTH = 1
CH_STRUCT_TYPE = 2


class Channel:
    def __init__(self, element: ET.Element):
        attr = element.attrib
        self.name = attr["name"]
        self.unit = attr["physicalunit"]
        self.index = int(attr["index"])
        self.length_blob_size = int(attr["sizeoflengthvalue"])
        self.type = str(attr["datatype"])


class ChannelConversionType(Enum):
    int = 0
    uint = 1
    float = 2
    double = 3
    string = 4
    boolean = 5
    gpsloc = 6


def get_conversion_type(type_string):
    match type_string:
        case "int64" | "int32" | "int16" | "int8":
            return ChannelConversionType.int.value
        case "uint64" | "uint32" | "uint16" | "uint8" | "bool":
            return ChannelConversionType.uint.value
        case "float":
            return ChannelConversionType.float.value
        case "double":
            return ChannelConversionType.double.value
        case "string":
            return ChannelConversionType.string.value
        case "bool":
            return ChannelConversionType.boolean.value
        case "gpslocation":
            return ChannelConversionType.gpsloc.value


type_length = {
    "int64": 8,
    "int32": 4,
    "int16": 2,
    "int8": 1,
    "double": 8,
    "float": 4,
    "uint64": 8,
    "uint32": 4,
    "uint16": 2,
    "uint8": 1,
    "bool": 1,
    "string": 0,
    "gpslocation": 8*3
}


def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder=byteorder)


BC_MESSAGE_EVENT = 4
BC_ABS_TIMESTAMP_DATA = 8


def decode_datablob(metadata_array, ch_info) -> tuple[np.ndarray, np.ndarray]:
    metadata_enum = (
        metadata_array[0] - 128 if metadata_array[0] >= 128 else metadata_array[0]
    )
    control_bit = metadata_array[0] >> 7

    result = dict()
    if metadata_enum == BC_ABS_TIMESTAMP_DATA:
        result["epoch_size"] = 8
        if control_bit == 1:
            result["sample_start"] = 1 + 4
            result["num_samples"] = int.from_bytes(
                metadata_array[1:5].tobytes(), byteorder=byteorder
            )
        else:
            result["sample_start"] = 1
            result["num_samples"] = 1
    elif metadata_enum == BC_MESSAGE_EVENT:
        binary_data = metadata_array[1:9]
        result["ts_epoch"] = int.from_bytes(
            binary_data.tobytes(), byteorder=byteorder, signed=False
        )
        result["epoch_size"] = 0
        result["sample_start"] = 1 + 8 + 4
        result["num_samples"] = 1
        binary_data = metadata_array[9:13]
    else:
        return [], []

    value_result: np.ndarray
    ts_result: np.ndarray
    index = result["sample_start"]
    epoch_size = result["epoch_size"]
    sample_length = ch_info[CH_STRUCT_TYPELENGTH]
    full_length = sample_length + epoch_size

    sample_index = np.intc(0)
    match ch_info[CH_STRUCT_TYPE]:
        case ChannelConversionType.int.value:
            full_array = np.hsplit(
                np.frombuffer(metadata_array[index:], dtype="B").reshape(
                    -1, full_length
                ),
                np.array([epoch_size, full_length]),
            )
            value_result = full_array[1].flatten().view(dtype=f"<u{sample_length}")
            ts_result = full_array[0].flatten().view(dtype="<u8")
        case ChannelConversionType.uint.value:
            full_array = np.hsplit(
                np.frombuffer(metadata_array[index:], dtype="B").reshape(
                    -1, full_length
                ),
                np.array([epoch_size, full_length]),
            )
            value_result = full_array[1].flatten().view(dtype=f"<u{sample_length}")
            ts_result = full_array[0].flatten().view(dtype="<u8")
        case ChannelConversionType.float.value:
            full_array = np.hsplit(
                np.frombuffer(metadata_array[index:], dtype="B").reshape(
                    -1, full_length
                ),
                np.array([epoch_size, full_length]),
            )
            value_result = full_array[1].flatten().view(dtype="<f")
            ts_result = full_array[0].flatten().view(dtype="<u8")
        case ChannelConversionType.double.value:
            full_array = np.frombuffer(metadata_array[index:], dtype=np.float64)
            full_array = full_array.reshape(2, -1, order="F")
            ts_result = full_array[0].view("<u8")
            value_result = full_array[1]
        case 4:
            ts_result = (result["ts_epoch"],)
            value_result = [metadata_array[index:].tobytes().decode()]
        case 5:
            full_array = np.hsplit(
                np.frombuffer(metadata_array[index:], dtype="B").reshape(
                    -1, full_length
                ),
                np.array([epoch_size, full_length]),
            )
            value_result = full_array[1].flatten().view(dtype=np.bool_)
            ts_result = full_array[0].flatten().view(dtype="<u8")
        case 6:
            full_array = np.hsplit(
                np.frombuffer(metadata_array[index:], dtype="B").reshape(
                    -1, full_length
                ),
                np.array([epoch_size, full_length]),
            )
            ts_result = full_array[0].view("<u8")[0]
            value_result = full_array[1].reshape(-1,3,8).view(dtype=np.float64)
        case _:
            print("Unable to decode blob: unsupported channel type", file=sys.stderr)
            return [], []

    return value_result, ts_result


def convert_channels_to_array(channels: list[Channel]) -> np.ndarray:
    result = np.empty((len(channels) + 1, 3), dtype=np.int32)

    for ch in channels:
        result[ch.index][CH_STRUCT_INDEX] = ch.length_blob_size
        result[ch.index][CH_STRUCT_TYPELENGTH] = type_length[ch.type]
        result[ch.index][CH_STRUCT_TYPE] = get_conversion_type(ch.type)

    return result


def read_sample_blob(
    stream, channel_info_array: np.ndarray, start, filter_array
) -> tuple[np.ndarray, int, tuple]:
    size_start = start + 2
    ch_index = stream[start:size_start].view(dtype=np.uint16)[0]
    size_of_length_value = channel_info_array[ch_index][CH_STRUCT_INDEX]
    if size_of_length_value == 2:
        blob_length = stream[size_start: size_start + 2].view(dtype="<u2")
    elif size_of_length_value == 4:
        blob_length = stream[size_start: size_start + 4].view(dtype="<u4")
    end_index = size_start + size_of_length_value + blob_length[0]

    if ch_index not in filter_array:
        return np.empty((0)), end_index, ()

    return (
        stream[size_start + size_of_length_value: end_index],
        end_index,
        (
            ch_index,
            channel_info_array[ch_index][CH_STRUCT_TYPELENGTH],
            channel_info_array[ch_index][CH_STRUCT_TYPE],
        ),
    )
