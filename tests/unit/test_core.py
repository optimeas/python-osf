from libosf.core import Metadata, construct_metadata
from xml.etree import ElementTree as ET


def test_metadata_construction():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<optimeas creator="17002700018" created_utc="2023-09-04T09:01:45Z" created_at_latitude="0" created_at_longitude="0" created_at_altitude="0" tag="preview" namespacesep="." reason="SEQUENCE" total_seq_no="12" triggered_seq_no="12">
    <channels count="23">
        <channel datatype="float" sizeoflengthvalue="2" index="0" channeltype="scalar" name="Ruuvi.Sensor.Abteil1.BatteryVoltage" ancient_utc="2023-09-04T09:01:18.148875629Z" physicalunit="V"/>
        <channel datatype="float" sizeoflengthvalue="2" index="1" channeltype="scalar" name="Ruuvi.Sensor.Motor.Pressure" physicalunit="hPa"/>
        <channel datatype="int32" sizeoflengthvalue="2" index="2" channeltype="scalar" name="STATUS.Opticloud.ConnectionLossTimestamps" ancient_utc="2023-09-04T08:42:32.509080883Z" physicalunit="s"/>
        <channel datatype="int64" sizeoflengthvalue="2" index="3" channeltype="scalar" name="STATUS.Opticloud.LoadCycleCounter" physicalunit=""/>
        <channel datatype="int64" sizeoflengthvalue="2" index="4" channeltype="scalar" name="Osfwriter.EstimatedDataVolume" ancient_utc="2023-09-04T09:01:11.152238730Z" physicalunit="MB/h"/>
        <channel datatype="int32" sizeoflengthvalue="2" index="5" channeltype="scalar" name="Ruuvi.Sensor.Motor.RSSI" physicalunit="dBm"/>
        <channel datatype="double" sizeoflengthvalue="2" index="6" channeltype="scalar" name="STATUS.Opticloud.EstimatedUploadTraffic" ancient_utc="2023-09-04T09:01:07.964888065Z" physicalunit="MB/h"/>
        <channel datatype="float" sizeoflengthvalue="2" index="7" channeltype="scalar" name="Ruuvi.Sensor.Abteil1.Temperature" physicalunit="°C"/>
        <channel datatype="int64" sizeoflengthvalue="2" index="8" channeltype="scalar" name="STATUS.Opticloud.TotalCycleCounter" physicalunit=""/>
        <channel datatype="float" sizeoflengthvalue="2" index="9" channeltype="scalar" name="Ruuvi.Sensor.Motor.Temperature" physicalunit="°C"/>
        <channel datatype="uint8" sizeoflengthvalue="2" index="10" channeltype="scalar" name="Ruuvi.Sensor.Abteil1.Humidity" physicalunit="%"/>
        <channel datatype="float" sizeoflengthvalue="2" index="11" channeltype="scalar" name="Ruuvi.Sensor.Abteil1.Pressure" physicalunit="hPa"/>
        <channel datatype="int64" sizeoflengthvalue="2" index="12" channeltype="scalar" name="STATUS.Opticloud.SendCompletionTime" physicalunit="ms"/>
        <channel datatype="uint8" sizeoflengthvalue="2" index="13" channeltype="scalar" name="Ruuvi.Sensor.Motor.Humidity" ancient_utc="2023-09-04T09:00:48.149494844Z" physicalunit="%"/>
        <channel datatype="string" sizeoflengthvalue="4" index="14" channeltype="scalar" name="Ruuvi.Sensor.Abteil1.MacAddress" ancient_utc="2023-09-04T09:00:36.243566993Z" physicalunit=""/>
        <channel datatype="int64" sizeoflengthvalue="2" index="15" channeltype="scalar" name="STATUS.Opticloud.IdleCycleCounter" physicalunit=""/>
        <channel datatype="int32" sizeoflengthvalue="2" index="16" channeltype="scalar" name="Ruuvi.Sensor.Abteil1.RSSI" physicalunit="dBm"/>
        <channel datatype="int64" sizeoflengthvalue="2" index="17" channeltype="scalar" name="STATUS.Opticloud.InstantaneousTraffic" physicalunit="Bytes"/>
        <channel datatype="int32" sizeoflengthvalue="2" index="18" channeltype="scalar" name="STATUS.Opticloud.ConnectionReconnectTimestamps" ancient_utc="2023-09-04T08:43:34.171478846Z" physicalunit="s"/>
        <channel datatype="float" sizeoflengthvalue="2" index="19" channeltype="scalar" name="Ruuvi.Sensor.Motor.BatteryVoltage" ancient_utc="2023-09-04T09:00:48.149494844Z" physicalunit="V"/>
        <channel datatype="string" sizeoflengthvalue="4" index="20" channeltype="scalar" name="Ruuvi.Sensor.Motor.MacAddress" ancient_utc="2023-09-04T08:59:46.236557309Z" physicalunit=""/>
        <channel datatype="int64" sizeoflengthvalue="2" index="21" channeltype="scalar" name="STATUS.Opticloud.ConnectionLossCounter" ancient_utc="2023-09-04T08:42:32.509080883Z" physicalunit=""/>
        <channel datatype="int64" sizeoflengthvalue="2" index="22" channeltype="scalar" name="STATUS.Opticloud.ConnectionReconnectCounter" ancient_utc="2023-09-04T08:43:34.171478846Z" physicalunit=""/>
    </channels>
    <infos>
        <info name="smartcore" datatype="string" value="2.5+64 [d675c0db] EXPERIMENTAL VERSION (21.08.23 16:07:10)"/>
        <info name="libosf" datatype="string" value="355b1caa"/>
    </infos>
</optimeas>
    """
    element = ET.fromstring(xml.strip())
    metadata = construct_metadata(element)
    assert metadata.creator == '17002700018'
    assert metadata.infos.get('smartcore','') == '2.5+64 [d675c0db] EXPERIMENTAL VERSION (21.08.23 16:07:10)'