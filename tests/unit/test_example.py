import libosf as osf
import io
import pytest

valid_test_input = b''


def test_header_creation():
    invalid_data_bytes = b'Some invalid bytes\x0a\x00\x01'
    input_data = io.BytesIO(invalid_data_bytes)
    header = Header(input_data)
    assert header.data == invalid_data_bytes
    with pytest.raises(RuntimeError):
        channels = header.parse()
    # TODO: Add valid parsing of channels
