import libosf as osf
from libosf import OSFFormat


def test_osf_version_open():
    with osf.read_file('../data/osf4_ruvvi.osf') as file:
        assert file.osf_version == OSFFormat.OSF4
        assert file.version_supported is True
    with osf.read_file('../data/osf3.osf') as file:
        assert file.osf_version == OSFFormat.OSF3
        assert file.version_supported is False
    with osf.read_file('../data/trash.txt') as file:
        assert file.osf_version == OSFFormat.UNKNOWN
        assert file.version_supported is False


def test_qload_channel():
    with osf.read_file('../data/osf4_ruvvi.osf') as file:
        channels = file.channels()

    assert len(channels) == 23


def test_qload_metadata():
    with osf.read_file('../data/osf4_ruvvi.osf') as file:
        metadata = file.metadata()

    assert metadata.creator == '17002700018'
    assert metadata.created_at_latitude == '0'
    assert metadata.libosf == '355b1caa'


def test_load_all_channels():
    with osf.read_file('../data/osf4_ruvvi.osf') as file:
        samples = file.all_samples()

    assert len(samples) > 500


def test_get_samples_by_channel_name():
    with osf.read_file('../data/osf4_ruvvi.osf') as file:
        samples = file.get_samples_by_name([
            'Ruuvi.Sensor.Motor.BatteryVoltage',
            'Ruuvi.Sensor.Motor.MacAddress'
        ])

    assert len(samples) > 10
