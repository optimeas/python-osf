import libosf as osf
from libosf import OSFFormat
from pathlib import Path

tests_directory = Path(__file__).parent.parent
osf4_file = tests_directory.joinpath('data/osf4_ruvvi.osf')
osf3_file = tests_directory.joinpath('data/osf3.osf')
trash_file =  tests_directory.joinpath('data/trash.txt')

def test_osf_version_open():
    with osf.read_file(osf4_file) as file:
        assert file.osf_version == OSFFormat.OSF4
        assert file.version_supported is True
    with osf.read_file(osf3_file) as file:
        assert file.osf_version == OSFFormat.OSF3
        assert file.version_supported is False
    with osf.read_file(trash_file) as file:
        assert file.osf_version == OSFFormat.UNKNOWN
        assert file.version_supported is False


def test_qload_channel():
    with osf.read_file(osf4_file) as file:
        channels = file.channels()

    assert len(channels) == 23

    queried_channels = [ch for ch in channels if
                        ch.name in [
                            'Ruuvi.Sensor.Motor.BatteryVoltage',
                            'Ruuvi.Sensor.Motor.MacAddress'
                        ]]
    assert len(queried_channels) == 2


def test_qload_metadata():
    with osf.read_file(osf4_file) as file:
        metadata = file.metadata()

    assert metadata.creator == '17002700018'
    assert metadata.created_utc == '2023-09-04T09:01:45Z'
    assert metadata.channel_count == 23
    assert metadata.infos.get('libosf','') == '355b1caa'


def test_load_all_channels():
    with osf.read_file(osf4_file) as file:
        samples = file.all_samples()

    assert len(list(samples)) > 500


def test_get_samples_by_channel_name():
    with osf.read_file(osf4_file) as file:
        samples = file.get_samples_by_name([
            'Ruuvi.Sensor.Motor.BatteryVoltage',
            'Ruuvi.Sensor.Motor.MacAddress'
        ])

    assert len(list(samples)) == 10
