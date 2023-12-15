# optiMEAS Streaming Format Version 4

Keywords: OSF, OSF4

Documentation Version: 1.1
Last change date: 10.2023

## Changes

- Doc Layout reworked
- Tranlation to english

## Overview

In measurement systems, data of various data types and recording formats are generated from a wide variety of sources. Starting with physical measured quantities like pressure, vibrations or temperatures, over electrical quantities, up to arbitrary binary data blocks like for example pictures. These quantities are generated over a time axis. Either in fixed time intervals or sampling rates, or depending on how they change, with individual time stamps.
In order to be able to store this data permanently with great reliability, the data stream is converted into OSF files (optically stored file) using a \"streaming\" format into OSF files (optimeas streaming format).

Each file starts with a magic header, which marks the OSF format and the beginning of the binary data stream.
start of the binary data stream. This is followed by an XML block for
Description of the channels, data types and recording formats.

Supported are:

- Standard data types, such as currently bool, double, float, int64, int32,
  int16, int8, string (attribute \"datatype\")
- Scaled integer values, e.g. to save memory at high sampling rates (scaling via attribute "\").
  (scaling via attribute \"scale\")
- Extended data formats with application specific contents
  static or dynamic length
- Recording of time-stamped or equidistant data sets
- recording as scalar value, list of N-values (vector) or
  matrices
- Arbitrary markers within the data stream
- Repeated resynchronization to the time base,
- Binary data are always stored in little endian format (Intel)
- The time base for all time data is nanoseconds (ns) since
  Epoch, in the form of an int64_t value.

More information at:

==== Example of an OSF file ====

```xml
    OSF4 30269
    <?xml version="1.0" encoding="UTF-8"?>
    <osf version="1" created_timezoneoffset="7200000" creator="smartdevice:14001000021" created_utc="1304013600000">
      <channels count="181">
        <channel physicalunit="°C" name="ME03/YP031T407" physicaldimension="temperature" datatype="double" index="0" user_reference="{002d376e-f265-4f58-82c7-358a3b72ca45}"/>
        <channel physicalunit="°C" name="Pt1000/AMP04PT02" physicaldimension="temperature" datatype="double" index="1" user_reference="{01f61f02-4179-4c4e-b423-bddd7ff4cd1e}"/>
        <channel physicalunit="°C" name="ME27/RL040T401" physicaldimension="temperature" datatype="double" index="2" user_reference="{05981247-5a72-4df9-855a-36fbe9caa3a9}"/>
        <channel physicalunit="°C" name="ME22/TJ030T406" physicaldimension="temperature" datatype="double" index="3" user_reference="{060c9013-3e78-42e1-b9e5-c7f1b32e7a7f}"/>
        <channel name="Schranksignale/JV001_DoorOpen_bus" datatype="bool" index="4" user_reference="{06e92479-c709-4636-ab88-5d85027af0cb}"/>
        <channel physicalunit="°C" name="Schranksignale/JV001_Temp_Bottom_bus" physicaldimension="temperature" datatype="double" index="5" user_reference="{0755b76e-015c-4f22-9986-077220de1260}"/>
        <channel physicalunit="°C" name="ME25/TJ010T411" physicaldimension="" datatype="double" index="6" user_reference="{07d039b9-8886-4708-8db8-970cf0bc925c}"/>
        <channel physicalunit="°C" name="ME19/TA000T441" physicaldimension="" datatype="double" index="7" user_reference="{0c771f1b-6004-4a48-82ce-a3f5e8a6c4e0}"/>
    ...
      </channels>
      <info>
        <info name="Some UTF-8 String Value" datatype="string" value="This is a comment"/>
        <info name="Some Byte Array Value" datatype="bytearray" value="SGVsbG8sAFdvcmxkIQ=="/>
        <info name="Some Numerical Value" datatype="float" value="-42.1"/>
        <info name="Some Numerical Value 2" datatype="uint32" value="123"/>
        <info physicalunit="°C" name="system/CPU_Temperature" type="double" value="43.4"/>
      </infos>
    </osf>
    [BEGIN OF BINARY DATA]...
```

From position 30269 binary data follow, which contain with the time progressively
Data records of the individual channels contain.

The info area is optimal. There meta information can be stored in the
file to the measurement data can be stored.

The following entries must be present:

- name
- value

If no data type is specified, \"string\" is used. The remaining
parameters are optional!

## Structure of the OSF4 format

The OSF file consists mainly of the following blocks

1. MAGIC header
2. XML information block describing the stored data
3. binary data block
4. XML termination block (optional) for quick access to
   information in the data
5. MAGIC Trailer (optional)

### MAGIC Header, OSF4

The Magic Header of the file contains exactly one line in ASCII format, terminated with
terminated with LF. UTF format BOMs or other encodings are not included in the
are not included at the beginning of the file.

Example:

OSF4 173762\n

The integer indicates how many bytes follow in the following XML header.
Thus this can be cut out immediately when reading and be supplied to a
parser for processing.

### XML meta information (start)

All META blocks (start, update, end) are in UTF-8 with **LF**.
Unix line endings (0x0A). The decoding of an XML text with
**LF** (0x0A) breaks should generally not be a problem for PC
software.

### XML Prolog

The XML block with the META information for each channel starts with the
typical XML prolog:

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

which is used to specify XML version and encoding. For OSF files this is
this is always UTF-8.

### XML document node **osf**

The document node **osf** gives further information about the file format
and the origin of the file.

```xml
    <osf version="4" 
           created_utc="2009-06-30T18:30:00+02:00" 
           creator="smartdevice:14001000078" 
           created_at_longitude="50.2"
           created_at_latitude="8.65"
           created_at_altitude="193"
     reason="BOOT"
     total_seq_no="0"
     triggered_seq_no="0"
     namespacesep="."
     tag="preview"
     comment"=""
    ...
    </osf>
```

The attributes of the node have the following meaning:

- **version**: Versioning of the OSF-4 format, here initially 1 [default: "1"].
- **created_utc**: System timestamp when creating the file in ISO
    8601 compliant format. Contains date and time in UTC format plus
    optionally the time zone information
- **creator**: A text which uniquely identifies the object which
    created the file. This can be, for example, a program name, a device
    device serial number or a UUID.
- **created_at_longitude**: Optional. Geographic longitude when the file was
    of the file. If the position is known when the file is created,
    is entered.
- **created_at_latitude**: Optional. Latitude when creating the file.
    of the file. If the position is known when the file is created,
    is entered.
- **created_at_altitude**: Optional. Geographic altitude when creating the file.
    of the file. If the position is known when the file is created,
    it will be entered.
- **reason**: Reason for creating the file. Possible values:
 "BOOT" - system start
 "SEQUENCE" - division with respect to file size or temporal file length
 "TRIGGERED" - trigger condition met (rising edge of the trigger)
- **total_seq_no**: Absolute index of the file since system start
 starting with 0.
- **triggered_seq_no**: Relative index of the file since last
 rising edge of the trigger starting with 0.
- **namespacesep**: Namespace separator for hierarchical arrangement
 of the channel names. [default: "."]
- **tag**: Tag (category) of the OSF file [default: "preview"]
- **comment**: User defined comment

### listing of channels **channels**.

As the only subnode in *osf* at the moment the list of channels is
is included. In the future, additional information could be added, e.g.
comments, calculation rules or filter settings could be included.
be included.

```xml
    <channels count="181">
    ...
    </channels>
```

The attributes of the node have the following meaning:

- **count**: Number of channels listed.

### Information about a channel **channel**.

**example**

```xml
    <channel 
      index="0" 
      name="channel1 
      channeltype="scalar"
      datatype="double"
      timeincrement="1000000"
      sizeoflengthvalue="2"
      physicalunit="V"
      reference="user defined reference string"
      physicaldimension="temperature"
   comment=""
   displayname=""
   uselogscale="false"
   mimetype=""
   spectrumtype="amplitude"
   
   <!-- for matrix-valued and vector-valued channels -->
   rows="1"
   row_caption=""
   row_physicalunit=""
   row_min="0.0"
   row_inc="0.0"
   row_max="0.0"
   row_align="center"
   row_labels="TBD"
   
   columns="1"
   column_caption=""
   column_physicalunit=""
   column_min="0.0"
   column_inc="0.0"
   column_max="0.0"
   column_align="center"
   column_labels="TBD"
    />
```

The attributes of the node have the following meaning:

- **index**: Indexing within this file to identify individual
    individual records. The index for the first channel always starts at 0.
    at 0. It is monotonously increasing. The last index is therefore the
    channel number minus 1.

- **reference**: \[optional\] An arbitrary identifier or a
    UUID that uniquely identifies the object that generated the data.
    data. Used on an application-specific basis

- **name**: Channel name with path if applicable. Is the application specific
    designation of the data stream.

- **physicalunit**: \[optional\] Display unit of the channel,
    usually in SI notation, i.e. with distinction of lower and upper case letters, punctuation
    and uppercase letters, punctuation etc., future SW versions will also convert
    will also be converted on the basis of this unit designation. [default: ""]

- **datatype**: Data type of the channel. Beside standard types for
    boolean, integer, and floating point values, any other application-specific
    application-specific identifiers for data types are allowed.

- **cannode**: Only valid if datatype=candata. Number of the CAN
    node. Starting with 1 the number of the CAN node from which the data are
    from which the data is generated.

- **timeincrement**: \[optional\], Fixed time increment in
    nanoseconds for equidistantly stored data. Unless
    **timeincrement** is not specified or \"0\", the data is timestamped.
    is provided with a timestamp. Depending on this entry, the
    the data blocks for data with fixed time increment and data with time
    timestamp are structured differently. See block definition.

- **channeltype**: Channel type of the channel. Here the structural
    structure of a data block is defined in advance. Depending on
    this definition, additional description parameters are
    attribute are created.
  - *scalar*: Channel with one data point per value. Example:
        datatype=\"double\" returns a data track with one value over
        the time. Example datatype=\"gpsdata\" returns the geo position
        over time.
  - *vector*: Channel with n scalar values in the data block. The result is
        a one-dimensional value field with the specified data type over
        the time. Example: FFT or one-dimensional classifications over
        the time.
  - *matrix*: Channel with y\[d1,d2\] values over x. n pairs of values in the
        data block. The x value is the absolute time in nanoseconds as
        int64. Example: Rainflow classifier matrix over time
  - *binary*: Channel with arbitrary data blocks over time.
        Example JPEG files over time.
    [default: "scalar"]

- **sizeoflengthvalue**: \[required\], Each data block has a different
    different length, which is prepended to each data block with the data type
    prepended to each data block. Possible values are:
  - *2*: 2-byte integer - uint16, lengths up to 64 kByte\.
        If the maximum block size is not sufficient to accommodate all data samples of the
        data stream, the data stream is divided into several sufficiently small blocks,
        sufficiently small blocks.
  - *4*: 4-byte integer - uint32, lengths up to 4 GByte (theoretical)
    [default: "2"]

- **scale**: \[optional\] for integer data types (scalar, vector,
    matrix). Scaling of the stored integer value to the
    desired physical size
    [default: "1.0"]

- **offset**: \[optional\] for integer data types (scalar, vector,
    matrix). Offset of the scaled integer value to the desired physical
    physical size
    [default: "0.0"]

- **physicaldimension**: \[optional for future extensions\]
    English name of the physical dimension, e.g.
    \"temperature\", \"force\", \"torque\", \"velocity\", \"pressure\",
    \...
    [default: ""]

- **comment**: \[optional\] comment
 [default: ""]

- **displayname**: \[optional\] Name of the channel in the display.
 [default: ""]

- **uselogscale**: \[optional\] Use single-logarithmic display.
 [default: "false"]

- **mimetype**: \[optional\] MIME type of the channel content.
 [default: ""]

- **spectrumtype**: \[optional\] Spectrum type of the channel.
 [default: "amplitude"]
 Possible representations:
  - \"amplitude\" - representation of real function values (or amplitude of complex function values)
  - \"realImag\" - Cartesian representation of complex function values
  - \"ampPhaseRad\" - Polar representation of complex function values (phase in radians)
  - \"ampPhaseDeg\" - Polar representation of complex function values (phase in degree measure)

- **rows**: \[optional\] number of rows of the matrix/vector valued channel.
 [default: "1"]

- **row_caption**: \[optional\] row description of the matrix/vector-valued channel.
 [default: ""]

- **row_physicalunit**: \[optional\] Physical unit of the row of the matrix/vector-valued channel.
 [default: ""]

- **row_min**: \[optional\] Minimum interpolation point of the row of the matrix/vector-valued channel.
 [default: "0.0"]

- **row_inc**: \[optional\] Interpolation increment of the row of the matrix/vector-valued channel.
 [default: "0.0"]

- **row_max**: \[optional\] Maximum interpolation point of the row of the matrix/vector-valued channel.
 [default: "0.0"]

- **row_align**: \[optional\] Visual orientation of the row component of the value of a matrix/vector-valued channel.
 [default: "center"]
 Possible representations:
  - \"left\" - left-justified representation
  - \"center\" - Centered representation
  - \"right\" - right-aligned representation

- **row_labels**: \[optional\] to be clarified with JAK
 [default: ""]

- **columns**: \[optional\] number of columns of the matrix/vector-valued channel.
 [default: "1"]

- **column_caption**: \[optional\] column description of the matrix/vector-valued channel.
 [default: ""]

- **column_physicalunit**: \[optional\] Physical unit of the column of the matrix/vector-valued channel.
 [default: ""]

- **column_min**: \[optional\] Minimum interpolation point of the column of the matrix/vector-valued channel.
 [default: "0.0"]

- **column_inc**: \[optional\] Interpolation increment of the column of the matrix/vector-valued channel.
 [default: "0.0"]

- **column_max**: \[optional\] Maximum interpolation increment of the column of the matrix/vector-valued channel.
 [default: "0.0"]

- **row_align**: \[optional\] Visual orientation of the column component of the value of a matrix/vector-valued channel.
 [default: "center"]
 Possible representations:
  - \"left\" - left-justified representation
  - \"center\" - Centered representation
  - \"right\" - right-aligned representation

- **row_labels**: \[optional\] <!---to be clarified with JAK -->
 [default: ""]

If for data reduction measured values are stored directly as (signed) integer value with a
short bit length, they must be converted to the physical format by means of the attributes
and *offset* into the physical size. It is valid

physical = scale * binary + offset

#### Standard data types

- Standard data types are (Encoding: Little-Endian (Intel)):
  - *bool*: 1-byte, true (== 1) /false (== 0)
  - *int8*: 1-byte, signed
  - *int16*: 2-byte, with sign
  - *int32*: 4-byte, with sign
  - *int64*: 8-byte, signed
  - *int64*: 8-byte, signed - used for timestamp
  - *float*: 4-byte floating point (single precision), [IEEE
        754](https://de.wikipedia.org/wiki/IEEE_754)
  - double*: 8-byte floating point (double precision), [IEEE
        754](https://de.wikipedia.org/wiki/IEEE_754)
  - *complex\<float\>*: (reserved for future applications)
        real/imag representation of complex numbers, each as float
  - *complex\<double\>*: (reserved for future use)
        real/imag representation of complex numbers, each as double
  - *string*: UTF-8 encoded characters without string termination. The
        length is given by the block description.
  - *candata*: Contains the following struct to describe a
        CAN message, extends the definition in       
    ```C
        include/linux/can.h 
        struct can_frame {
            uint32 can_id; /* 32 bit CAN_ID + EFF/RTR/ERR flags */
            uint8 can_dlc; /* frame payload length in byte (0 .. 8) */
            uint8 data[8];
        }  __attribute__((aligned(8)));
    ```

  - *gpsdata*: Longitude, Latitude, Altitude - each as a double value corresponding to the following struct: 
    ```C
        struct gps_location {
            double longitude;
            double latitude;
            double altitude;
        };
    ```

[//]: # (*FIXME STH revise!*)

<!--- 

**gpsinfo:**: Various information about GPS reception according to the following C-struct:

```C
    struct gps_info {
      uint8 satcount; // Number of satellites
      uint8 qos; // Quality of Service
      uint64 time; // GPS time
    };
```

More information about the definition of [vectors and matrices can be found here] (/development/fileformats/stream4/vector)
-->

### Binary data block

The binary data block starts directly after the XML
header information. The position in the file is specified in the MAGIC HEADER
specified: `OSF4 173762\n
`

Basically, the file is divided into individual data blocks. Each
data block describes a sequence of 1 to N data samples of a channel.
The data stream of the channel can be continued in following blocks.
Each data block automatically points to the next data block by specifying its size.
next following data block. This allows that even in case of
immediate interruption of the write process (e.g. by power failure or interruption of the data
interruption of the data connection), the data can be read until the end of the data stream/file.
readable until the end of the data stream/file.

The basic structure of the data format thus allows:

1. to simply skip information that is not required
2. to retrofit any data and channel types application-specific
3. to ignore data blocks that are not known
4. to interpret the data up to the last data block

#### Same start for all data blocks

The start of a binary data block is defined as follows:

- **uint16**, channel index (as in version 3 also).
- **\<sizeoflengthvalue\>**: In the channel description of the header
    defined. Depending on the definition of the size of the data word for
    the length value of the following block 2-4 bytes (uint16,uint32):
    Number of following bytes for control byte, meta information and
    the actual data samples.
  - The next channel data block thus starts at
        \<start\>+2+\<sizeoflengthvalue\>+\<size of data block in
        byte\>
  - If the writing of the file should have been aborted prematurely
        the end of the data block is beyond the end of the file. In
        the end of the file can be read as long as a complete data sample is
        a complete data sample can be decoded. A
        incomplete data sample is discarded.
- **uint8**, **control byte**, determines the content of the subsequent
    meta information block in the data stream

By specifying the size of the block, the data block can be
or unknown or not (yet) implemented **channeltype** or
**datatype** can be skipped or read in one piece for interpretation.
piece.

In case of interpretation or data errors in a block, the block can be
error message, the data stream for the respective channel can be interrupted.
channel can be interrupted. The interpretation of the OSF stream
can be continued with the next block. Further data blocks for
can be ignored until an absolute time stamp allows the correct interpretation of the data again.
interpretation of the data again.

There are basically two different types of channels
are distinguished:

- Channels with fixed time increment (equidistant).
- Channels with time stamp at each data sample

#### Control byte and meta information in the data stream

The control byte is the same for all channel and data types and determines
which meta information is inserted before the actual data of the block.
is inserted.

In order to reduce the number of implementation variants, the
structure of the following data block is specified by a 7-bit ENUM and a control bit.
control bit.

The control bit 7 indicates whether the data block contains 1- or
n-value/value pairs are contained.

The structure of the control byte **blockContent** as a value enumeration is as follows
following:

| Value | Enum | Meaning | Data block |
| ---- |------| ----------| -----------------|
| 0 | *bcMetaData* | Use this block type only for internal use, e.g. special functions and file termination, not assigned to any channel.| **uint32**: L := length of text block<br/>**uin8\[L+1\]**: UTF-8 encoded text block with \'0\' termination.|
| 1 | *bcTrustedTimestamp* | Absolute timestamp in \"ns since Epoch\",<br/>the previous data value is valid and constant until this time<br> <!--- [\"Trusted Timestamp\"](/development/fileformats/stream4/trusted) link must be fixed or put description in document! --> | **int64**: ns since Epoch |
| 2 | *bcTimebaseRealign* | Adjust timeline | **int64**: Absolute timestamp in \"ns since Epoch\"<br/>**int64**: Shift of time base in ns.<br/><br/>\> 0: Forward jump, gaping data<br/><br/> \< 0: Backward jump, overlapping data |
| 3 | *bcStatusEvent* |Status Event | **int64**: Absolute timestamp in \"ns since Epoch\"<br>**uint32**: Status Word|
| 4 | *bcMessageEvent* | Time-stamped text entry|**int64**: Absolute timestamp in \"ns since Epoch\", applies ONLY to text message.<br>**uint32**: L := length of text message.<br>**uin8\[L+1\]**: UTF-8 encoded text message it \'\'\0\' termination.|
| 5 | *bcContinuedData* | Append data with fixed sample rate| if option bit 7 set:<br>**uint32**: N := number of samples,<br>\... otherwise N := 1<br>**Nx**:<br>**Y**: Data according to channel description (Timeline connects to previous data block.)|.
| 6 | *bcStartData* |First data block with data of fixed sampling rate in stream| **int64**: Absolute timestamp in \"ns since Epoch\"<br>if option bit 7 is set:<br>**uint32**: N := number of samples,<br>\... otherwise N := 1<br> **Nx**:<br>**Y**: Data according to channel description (time axis starts in this data block, e.g. for data stream with trigger control)|.
| 7 | *bcContinuedRelStampData* |Append data with relative timestamp| if option bit 7 set:<br>**uint32**: N := number of samples,<br>\... otherwise N := 1<br>**Nx**:<br>**uint32**: relative distance to previous data sample in ns<br>**Y**: Data according to channel description.|
| 8 | *bcAbsTimeStampData* | Append data with absolute time stamp. Can also be the first data block with relative time stamps.| if option bit 7 set:<br>**uint32**: N := number of samples,<br>\... else N := 1<br>**Nx**:<br>**int64**: Absolute timestamp in \"ns since Epoch\"<br>**Y**: Data according to channel description|

Restriction of block types with respect to channel information:

| ENUM type | Equidistant data | Time-stamped data |
| ------------- |-------------| -----|
| bcTrustedTimestamp | not allowed | allowed
| bcTimebaseRealign | allowed | allowed |
| bcStatusEvent | N/A | N/A
| bcMessage | N/A | N/A |
| bcContinuedData | allowed | not allowed |
| bcContinuedRelStampData | not allowed | allowed |
| bcAbsTimeStampData | N/A | N/A |

By synchronizing the time base to external sources like e.g.
GPS, DCF77 or NTP, e.g. for long time measurements in the data stream
time jumps can occur in any direction. The sequence of the measurement data
is therefore strictly monotonous with respect to the running time of the device,
but not the assignment to the absolute time base. With a
time synchronization with correction of the time axis, in any case a
*bcTimebaseRealign* block is written. With the following
interpretation of the data, this information can be used to

- \"gaps\" can be closed by the insertion of certain error values
    can be closed
- \"overlaps\" can be corrected by cutting out data
    or
- time stamps of previous data can be corrected / recalculated.

Several events can occur in one channel. For each
event a block *bcMessage* is created with the UTC absolute time value of the
event as well as an application specific text block.

For certain data reduction procedures, the situation may occur,
that a (time-stamped) data sample remains valid for a long time.
validity for a long time. Examples are Boolean channels, where only
changes are recorded or measured values that remain constant in a tolerance band
remain constant within a tolerance band over long periods of time. For the representation of life data
the block *bcTrustedTimestamp* is inserted into the data stream in shorter intervals
data stream, typically at the end of each transmitted time interval.
time interval. In a graphical representation one could draw a
constant curve until the given time without using a symbol for a measuring point.
but to set a symbol for a measuring point. The interpretation is
optional. When writing to a file, *bcTrustedTimestamp* is built in before the
file termination for the corresponding channels.

#### Data with fixed time increment (equidistant)

In the channel definition for channels with a fixed time increment the
specification of the **timeincrement** with a value [not equal to zero]{.ul} in
nano-seconds (ns) is mandatory.

The data stream of the channel contains after the header and meta information as the
first a *bcStartData* block. The data records are contained in *bcStartData*-
or *bcContinuedData* blocks and start with either the
with the given timestamp, e.g. after a trigger event (\"Segment\")
or connect to the already transmitted data stream.

The blocks for timestamped information *bcTrustedTimestamp*,
*bcContinuedRelStampData*, *bcAbsTimeStampData*, *bcStartRelStampData*
must not be used for equidistant sampling.

<!--- 

##### Examples of equidistant data blocks.

FIXME Create new

-->

#### Data with timestamp

In the channel definition, for channels with timestamped datasets.
the specification of the **timeincrement** is not included or zero.

The data stream of the channel contains after the header and meta information for
for each record, depending on the block description

- optionally an **int64** value as time stamp for the next
    relative value
- mandatory at each record
  - an **int64** absolute time stamp in ns since epoch **OR**
  - a **uint32** value as relative time interval (max. 4
        seconds) to the preceding data sample

The blocks for equidistant information *bcContinuedData*,
*bcStartData* must not be used for equidistant sampling.

##### Examples of data with timestamp

[//]: # (FIXME New to create)

- Data samples according to data types and number of samples (t,y,t,y,t,y\...).
  - For each data pair: **uint32** as relative time to the last
        data sample or to the last absolute timestamp. The
        data value then according to channel definition and **datatype**.
  - Example: Data format=double; Bit0=1; Number of values=1; (1xuint64,
        1xdouble) 16 bytes until end of block
  - Example: Data format=double; Bit0=0; Number of values=1; (1xuint32,
        1xdouble) 12 bytes to end of block
  - Example: Data format=int32; Bit1=0; valueorder=multiplex;
        number of values=20; (20x (uint32, int32)) 160 byte to end of block
  - Example: Data format=int32; Bit1=1; valueorder=multiplex;
        number of values=20; (20x (uint64, int32)) 168 bytes to end of block
  - Example: data format=int32; bit1=0; valueorder=linear; number of
        values=20; (20xuint32, 20xint32) 160 bytes to end of block
  - Example: data format=int32; bit1=1; valueorder=linear; number of
        values=20; (20xuint64, 20xint32) 240 bytes to end of block
  - Example: dataformat=gpsdata; bit1=1; number of values=1;
        (1xunit64,3xdouble) 32 bytes to end of block
  - Example: Data format=candata; Bit1=1; Number of values=1; 1xuint64
        (8 bytes) + depending on 1st length byte - 6..13 bytes to end of block

### Special functions (Index \>= 0xFFFF)

Since it is extremely improbable (or not very clever) to have more
more than 65000 channels in one OSF file, the following index values are
at the end of the value range are reserved for special control functions:

- **0xFFFF** / **EndOFS**: Regular end of the OSF streaming file,
    final XML block

The structure of the data block for these entries follows the description for an
an XML option block.

- **uint16**: \"channelindex\" (== 0xFFFF).
- **uint32**: Length of the following option block (e.g. up to the
    beginning of the MAGIC-END tag)
- **uint8**: *bcMetaData* - control byte (== zero).
- **string**, XML block, UTF-8 without prologue

This block is optional and does not have to be included in an Osf file!

### Structure of the final frame

```xml
<trailer finalized_utc="2019-08-12T12:23:01+2.00" reason="fileStartGrid_min">
    <channels count="8">
    <channel segments="1473" last_ns="1384899599997800000" samples="29452" index="0" last_utc="2019-11-19T23:19:59"/>
    <channel segments="1473" last_ns="1384899599997800000" samples="29452" index="1" last_utc="2019-11-19T23:19:59"/>
    <channel segments="1473" last_ns="1384899599997800000" samples="29452" index="2" last_utc="2019-11-19T23:19:59"/>
    <channel segments="1473" last_ns="1384899599997800000" samples="29452" index="3" last_utc="2019-11-19T23:19:59"/>
    <channel segments="1473" last_ns="1384899599997800000" samples="29452" index="4" last_utc="2019-11-19T23:19:59"/>
    <channel segments="1473" last_ns="1384899599997800000" samples="29452" index="5" last_utc="2019-11-19T23:19:59"/>
    <channel segments="1473" last_ns="1384899599997800000" samples="29452" index="6" last_utc="2019-11-19T23:19:59"/>
    <channel segments="1473" last_ns="1384899599997800000" samples="29452" index="7" last_utc="2019-11-19T23:19:59"/>
    </channels>
</trailer>
```


#### \<trailer\>

- **finalized_utc**: Time (system time) at which the file was
    was closed
- **reason**: Reason for the end of the file, e.g:
  - *maxFileLen_kB**: Closing of the file was triggered when the
        maximum file size (memory) was reached
  - *maxFileLen_s*: Closing the file was triggered when reaching the
        maximum file length (time)
  - *fileStartGrid_min*: Closing of the file was triggered when reaching
        the next time grid point (e.g. at :00, :15, :30 and :45 of an hour).
        and :45 of an hour).
  - *triggerEnd*: Closing the file was triggered at the end of a
        trigger period (one event per file).
  - \...: further application specific hints.
  - *shutDown*: OsfWriter object was deleted with open file,
        in this case the channel information could be incomplete.

#### \<channels\>

- **count**: Number of channels when closing the file.

#### \<channels\>

- **index**: Channel index
- **first_ns**: high-resolution ns timestamp of the first data sample, UTC Nano-Seconds since Epoch (1970).
- **samples**: number of data samples actually contained
- **last_ns**: high-resolution ns timestamp of the last data sample, UTC Nano-Seconds since Epoch (1970)

### MAGIC trailer, OSF_STREAM_END

The final trailer is always 40 bytes long

```json
OSF_STREAM_END 321316454==============
```

This is followed by \'=\' characters to pad to the 40 bytes.

The given number corresponds to the seek position in the file at which
where the final XML data block with statistical information begins, i.e.
begins, i.e. exactly the 0xFFFF control code would be read next.