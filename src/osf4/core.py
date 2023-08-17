import io


class Channel:
    ...


class Header:
    def __init__(self, stream: io.BytesIO):
        stream.seek(0)
        self._data = stream.read(-1)

    @property
    def data(self) -> bytes:
        return self._data

    def parse(self) -> list[Channel]:
        return []


class Datatype:
    ...
