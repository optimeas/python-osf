# optiMEAS Streaming Format Version 4

- Keywords: OSF, OSF4
- Documentation version: 1.0
- Last modification date: 11.2022

## Changes
- Translation to English

## Overview

In measuring systems, data of mostly different data types and recording formats arises from lots of different sources.
These can either be mechanical or electrical physical quantities such as pressures, vibrations or temperatures, voltages and currents, intermediate calculation results, or even more sophisticated arbitrary binary data blocks such as images.
These quantities are generated over a time axis and can either timestamped at fixed intervals according to a sampling rate, or depending on their change characteristics with individual time stamps.
In order to be able to permanently store this data with great reliability, the data stream is written into OSF files utilizing the optiMEAS Streaming Format \"streaming\" format.

Each file starts with a magic header entry, which specifies the OSF format and the bytewise offset denoting the beginning of the binary data stream.
This is then followed by an XML block containing the description of the channels w.r.t their data types and recording formats.

Supported are:

- Standard data types, such as currently bool, double, float, int64, int32, int16, int8, string (attribute \"datatype\")
- Scaled integer values, e.g. for saving storage space when high sampling rates are being utilized (scaling and offsetting specified via attributes \"scale\" and \"offset\" - respectively)
- Extended data formats with application specific contents using an either static or dynamic size
- Recording of time-stamped or equidistant data sets
- Recording of vectors and matrices specified via description of their dimensions
- Arbitrary markers within the data stream
- Repeated resynchronization of the time base,
- Binary data is always stored in little endian byte order (Intel)
- The time base for all data is nanoseconds (ns) since epoch specified as an int64 value.

More information about:

- [Trusted Timestamp](/development/fileformats/stream4/trusted)
- [Vectors and Matrices](/development/fileformats/stream4/vector)

### Example of OSF file ###

```xml
    OSF4 30269
    <?xml version="1.0" encoding="UTF-8"?>
    <osf version="1" created_timezoneoffset="7200000" creator="smartdevice:14001000021" created_utc="1304013600000">
      <channels count="181">
        <channel physicalunit="Â°C" name="ME03/YP031T407" physicaldimension="temperature" datatype="double" index="0" user_reference="{002d376e-f265-4f58-82c7-358a3b72ca45}"/>
        <channel physicalunit="Â°C" name="Pt1000/AMP04PT02" physicaldimension="temperature" datatype="double" index="1" user_reference="{01f61f02-4179-4c4e-b423-bddd7ff4cd1e}"/>
        <channel physicalunit="Â°C" name="ME27/RL040T401" physicaldimension="temperature" datatype="double" index="2" user_reference="{05981247-5a72-4df9-855a-36fbe9caa3a9}"/>
        <channel physicalunit="Â°C" name="ME22/TJ030T406" physicaldimension="temperature" datatype="double" index="3" user_reference="{060c9013-3e78-42e1-b9e5-c7f1b32e7a7f}"/>
        <channel name="Schranksignale/JV001_DoorOpen_bus" datatype="bool" index="4" user_reference="{06e92479-c709-4636-ab88-5d85027af0cb}"/>
        <channel physicalunit="Â°C" name="Schranksignale/JV001_Temp_Bottom_bus" physicaldimension="temperature" datatype="double" index="5" user_reference="{0755b76e-015c-4f22-9986-077220de1260}"/>
        <channel physicalunit="Â°C" name="ME25/TJ010T411" physicaldimension="" datatype="double" index="6" user_reference="{07d039b9-8886-4708-8db8-970cf0bc925c}"/>
        <channel physicalunit="Â°C" name="ME19/TA000T441" physicaldimension="" datatype="double" index="7" user_reference="{0c771f1b-6004-4a48-82ce-a3f5e8a6c4e0}"/>
    ...
      </channels>
      <info>
        <info name="Some UTF-8 String Value" datatype="string" value="This is a comment"/>
        <info name="Some Byte Array Value" datatype="bytearray" value="SGVsbG8sAFdvcmxkIQ=="/>
        <info name="Some Numerical Value" datatype="float" value="-42.1"/>
        <info name="Some Numerical Value 2" datatype="uint32" value="123"/>
        <info physicalunit="Â°C" name="system/CPU_Temperature" type="double" value="43.4"/>
      </infos>
    </osf>
    [BEGIN OF BINARY DATA]...
```

Here, the binary data will follow from byte position 30269 and will grow progressively with the time.
It contains the data records of the individual channels.

The optional info section is a suitable place for storage of all meta data.
It is organized into key-value-pairs using the mandatory attributes

- name
- value

If no \"datatype\" is specified, the corresponding \"value\" will be interpreted as a string.
The remaining parameters are optional!

## Structure of the OSF4 format

The OSF file consists mainly of the following blocks

1. MAGIC header
2. XML information block describing the stored binary data
3. binary data block

### MAGIC Header, OSF4

The Magic Header of the file contains exactly one line in ASCII format, terminated with LF.
UTF format BOMs or other encodings are not allowed at the beginning of the file.

Example:

    OSF4 173762\n

The integer indicates how many bytes follow in the following XML header.
Thus it can be extracted immediately when reading and be supplied to a
parser for further processing.

### XML meta information (start)

All META blocks (start, update, end) are UTF-8 encoded using **LF** Unix line endings (0x0A).
Decoding of XML texts containing **LF** (0x0A) breaks should not be a problem for PC
software, generally speaking.

### XML Prolog

The XML block containing the META information for each channel starts with the
typical XML declaration:

    <?xml version="1.0" encoding="UTF-8"?>

which is used to specify its version and encoding.
For OSF files this will always be UTF-8.

### XML document node *osf*

The document node **osf** specifies further information about the file format and the origin of the file.

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

The attributes of that node are:

- **version**: Versioning of the OSF-4 format, initially 1 [default: "1"].
- **created_utc**: System timestamp of file creation in ISO
    8601 compliant format. Will contain date and time in UTC format and
    optionally time zone information
- **creator**: A text which uniquely identifies the object which
    created the file. This can be e.g. a program name, a device
    device serial number or a UUID.
- **created_at_longitude**: Optional. Geographic longitude upon file creation, if it's known.
- **created_at_latitude**: Optional. Geographic latitude upon file creation, if it's known.
- **created_at_altitude**: Optional. Geographic altitude upon file creation, if it's known.
- **reason**: Reason for file creation. Possible values include:
	"BOOT" - file created upon system start
	"SEQUENCE" - file created upon splitting w.r.t. the file duration or its size
	"TRIGGERED" - file created upon trigger condition (generally, a rising trigger edge)
- **total_seq_no**: Absolute index of the file since system start, starting at 0.
- **triggered_seq_no**: Relative index of the file since last rising trigger edge, starting with 0.
- **namespacesep**: Namespace separator for hierarchical channel name arrangement [default: "."]
- **tag**: Tag (category) of the OSF file [default: "preview"]
- **comment**: User defined comment [default: ""]

### Listing of Channel Properties *channels*.

As the only currently specified subnode below *osf*, the list of channel properties is included.
In the future, however, additional information could be specified, e.g.
comments, calculation rules or filter settings could be included below *osf*.

    <channels count="181">
    ...
    </channels>

The attributes of the *channels* node have the following meaning:

- **count**: Number of channels listed as subnodes.

### Information about a channel *channel*.

\*\* Example \*\*

    <channel
      index="0"
      name="channel1"
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

The attributes of the *channel* node are:

- **index**: Indexing within this file for identification of individual binary data blocks.
    The index for the first channel will start at 0.
    It is monotonously increasing.
    The last index is therefore the channel number minus 1.

- **reference**: [optional] An arbitrary identifier or a
    UUID that uniquely identifies the object that generated the data.
    Depending upon the application context. [default: ""]

- **name**: Channel name with path, when applicable.
    This is the application related name of the data stream.

- **physicalunit**: \[optional\] Physical unit of the channel,
    usually in SI notation, i.e. with distinction of lower and upper case letters, sentence
    and uppercase letters, punctuation etc.
    Future software versions might also perform calculations upon physical unit information [default: ""]

- **datatype**: Data type of the channel. Besides standard data types notations for
    boolean, integer and floating point values, any other,
    application-specific identifiers for data types are also allowed.

- **cannode**: Only valid if *datatype*="*candata*". Index of the CAN, starting with *1*.

- **timeincrement**: [optional],Fixed time increment in
    nano-seconds for equidistantly stored data. Unless
    **timeincrement** is specified or \"0\" is specified, the data will be
    provided containg a timestamp. Depending on this entry,
    the binary data blocks structured differently. See binary block definition for more details.

- **channeltype**: Channel type of the channel. Here, the
    structure of a data block is specified in advance. Depending on
    this definition, additional description parameters
    are created.
    - *scalar*: Channel with one data value within its data blocks. Example:
        datatype=\"double\" returns a data track with one single value over time.
        Example datatype=\"gpsdata\" returns the geo position over time.
    - *vector*: Channel with n scalar values within its data blocks. The result is
        a one-dimensional value field with the specified data type over time.
        Example: FFT or one-dimensional classifications over time.
    - *matrix*: Channel with y[d1,d2] values over x containing n pairs of values within its
        data blocks. The x value is the absolute timestamp in nano-seconds specifed as a int64.
        Example: Rainflow classifier matrix over time
    - *binary*: Channel with arbitrary data blocks over time.
        Example JPEG files over time.

    [default: "scalar"]

- **sizeoflengthvalue**: Each data block can have a different
    length, which is prepended to each data block with the data type specified here.
    Possible values are:
    - *2*: 2-byte integer - uint16, will yield allowed data block lengths up to 64 kByte\.
        If the maximum block size is not sufficient to accommodate all data samples of the
        data stream, the data stream is divided into several sufficiently small blocks.
    - *4*: 4-byte integer - uint32, lengths up to 4 GByte (in theory)

    [default: "2"]

- **scale**: [optional] for integer data types (scalar, vector, matrix).
    Scales the stored integer value to the desired physical size.
    [default: "1.0"]

- **offset**: [optional] for integer data types (scalar, vector, matrix).
    Offsets the scaled integer value to the desired physical size.
    [default: "0.0"]

- **physicaldimension**: [optional for future extensions]
    English name of the physical dimension, e.g.
    "temperature", "force", "torque", "velocity", "pressure", ...
    [default: ""]

- **comment**: [optional] Comment
	[default: ""]

- **displayname**: [optional] Name of the channel when displayed.
	[default: ""]

- **uselogscale**: [optional] Use single-logarithmic representation, when displayed.
	[default: "false"]

- **mimetype**: [optional] MIME type of the channel content.
	[default: ""]

- **spectrumtype**: [optional] Spectrum type of the channel.
	Possible representations:
	- "amplitude" - representation of real function values (or amplitude of complex function values)
	- "realImag" - Cartesian representation of complex function values
	- "ampPhaseRad" - Polar representation of complex function values (phase in radians)
	- "ampPhaseDeg" - Polar representation of complex function values (phase in degree measure)

	[default: "amplitude"]


- **rows**: [optional] Number of rows of the matrix/vector-valued channel.
	[default: "1"]

- **row_caption**: [optional] Row description of the matrix/vector-valued channel.
	[default: ""]

- **row_physicalunit**: [optional] Physical unit of the row domain of the matrix/vector-valued channel.
	[default: ""]

- **row_min**: [optional] Row domain minimum of the matrix/vector-valued channel.
	[default: "0.0"]

- **row_inc**: [optional] Row domain increment of the matrix/vector-valued channel.
	[default: "0.0"]

- **row_max**: [optional] Row domain maximum of the matrix/vector-valued channel.
	[default: "0.0"]

- **row_align**: [optional] Support-point alignment of the row component of the value of a matrix/vector-valued channel.

	Possible representations:

	- "left" - left-justified representation
	- "center" - Centered representation
	- "right" - right-aligned representation

	[default: "center"]

- **row_labels**: [optional] to be discussed with JAK
	[default: ""]

- **columns**: [optional] Number of columns of the matrix/vector-valued channel.
	[default: "1"]

- **column_caption**: [optional] Column description of the matrix/vector-valued channel.
	[default: ""]

- **column_physicalunit**: [optional] Physical unit of the column domain of the matrix/vector-valued channel.
	[default: ""]

- **column_min**: [optional] Column domain minimum of the matrix/vector-valued channel.
	[default: "0.0"]

- **column_inc**: [optional] Column domain increment of the matrix/vector-valued channel.
	[default: "0.0"]

- **column_max**: \[optional] Column domain maximum of the matrix/vector-valued channel.
	[default: "0.0"]

- **row_align**: \[optional] Support-point alignment of the column component of the value of a matrix/vector-valued channel.

	Possible representations:

	- "left" - left-justified representation
	- "center" - Centered representation
	- "right" - right-aligned representation

	[default: "center"]

- **row_labels**: [optional] to be discussed with JAK
	[default: ""]

If measurement values are stored directly as (signed) integer values with a short bit length for data reduction,
they have to be converted to their physical representations using the attributes
*scale* and *offset*. Their resulting values are then defined as:

      physical = scale * binary + offset

#### Standard data types

- Standard data types are (Little-Endian byte order (Intel)):
    - *bool*: 1-byte, true (== 1) /false (== 0)
    - *int8*: 1-byte, signed
    - *int16*: 2-byte, signed
    - *int32*: 4-byte, signed
    - *int64*: 8-byte, signed, used mainly for representing timestamps
    - *uint8*: 1-byte, unsigned
    - *uint16*: 2-byte, unsigned
    - *uint32*: 4-byte, unsigned
    - *uint64*: 8-byte, unsigned
    - *float*: 4-byte floating point (single precision),
      [IEEE754](https://en.wikipedia.org/wiki/IEEE_754)
    - *double*: 8-byte floating point (double precision),
      [IEEE754](https://en.wikipedia.org/wiki/IEEE_754)
    - *complex/float*: (reserved for future applications)
      cartesic representation of complex numbers, each as float
    - *complex/double*: (reserved for future applications)
      cartesic representation of complex numbers, each as double
    - *string*: UTF-8 encoded string data without termination.
      The length is specified via the block description.
    - *candata*: Contains the following struct to describe a
      CAN message, extends the definition in *include/linux/can.h*
```
        struct can_frame {
            uint32 can_id; /* 32 bit CAN_ID + EFF/RTR/ERR flags */
            uint8 can_dlc; /* frame payload length in byte (0 .. 8) */
            uint8 data[8];
        }  __attribute__((aligned(8)));
```

    - *gpsdata*: Longitude, Latitude, Altitude - specified as the following struct
```
        struct gps_location {
            double longitude;
            double latitude;
            double altitude;
        };
```

### Binary Data Blocks

All binary data will be appended directly at the end of the XML header block.
Its starting position in bytes is specified within the OSF Magic Header entry, e.g.

`OSF4 173762`

Generally speaking, an OSF file will contain multiple data block.
Each data block will then describe 1 to N samples of a single channel.

The data stream of a channel can be represented using the following data blocks.
Each data block automatically points to the next data block by specifying its own size.
This allows for robustly finding consecutive data blocks even if their actual content is not specified
(e.g. an inferior OSF version specification is being used).
Upon immediate interruption of the writing process (e.g. by power failure or interruption of the data connection),
the data can be still be read until the end of the data stream/file.

The basic structure of the data format thus allows:

1. to simply skip information that is not required
2. to retrofit any data and channel types specific to the application
3. to ignore data blocks that are unknown
4. to interpret the data up until the last data block

#### Same beginning for all data blocks (container format)

The beginning of a binary data block is always defined using the following consecutive parts:

- **uint16** Channel index (like it was before in version 3).
- **sizeoflengthvalue** times sizeof(byte): Depending on the size of length of the channel
  (2 or 4, denoting a uint16 or uint32 value, respectively):
    Number of following bytes including the control byte,
    additional meta information and
    the actual data samples.
    - The next channel data block thus starts at
        the current block's starting position
        + 2 bytes (Channel Index)
        + sizeoflengthvalue bytes (Current Block's Length)
    - When the writing process is interrupted, the next data block's position might be beyond the end of the file.
        In this case, all data can be read as long as complete data blocks are available.
        Incomplete data blocks have to be discarded is this case.
- **uint8**, **control byte** determines the content of the subsequent
    meta information block in the data stream

By specifying the size of the block, the data block can be either unknown or not implemented (yet).
The channel attributes **channeltype** and **datatype** can be ignored in such a situation and the block can be skipped as a whole.
Otherwise, it can also be read as a whole.

In case of interpretation or data errors in a block, the data stream for the respective channel can be interrupted temporarily.
The interpretation of the OSF stream can be continued at the next data block.
Further data blocks for the interrupted channel have to be ignored until an absolute timestamp allows for correct interpretation of the data again.

There are basically two different types of channels
are distinguished:

- Channels with fixed time increment (equidistant channels).
- Channels with a time stamp for each data sample

#### Control byte and meta information in the data stream

The control byte is located at the same position for all channel and data types and determines
which meta information is inserted before the actual data of the data block.

In order to reduce the number of implementation variants, the
structure of the following data block is specified by a 7-bit ENUM and a control bit.
most-significant control bit (7th bit).

A set control bit will denote multiple (n) values/value-pairs within the data block where an unset control bit indicates a single value/value-pair.

The control byte excluding its most significant bit has the following meaning and the consecutively appended meta information:

- 0 *bcMetaData* Use this block type for internal use, only, e.g. special functions and file termination, it is not assigned to any channel.                      
  **uint32**: L := length of the following data (generally text) block.<br>
  [L+1] times **uint8**:  UTF-8 encoded text block with \0 termination.

- 1 *bcTrustedTimestamp* Absolute timestamp in nano-seconds since epoch
  **int64**: ns since Epoch<br>
  (remark: the previous data value is valid and constant until this time)
  [\"Trusted Timestamp\"](/development/fileformats/stream4/trusted)

- 2 *bcTimebaseRealign* adjustment of the timeline<br>
  **int64**: Absolute timestamp in nano-seconds since epoch.<br>
  **int64**: Shift of time base in nano-seconds,<br>
    \> 0: forward jump, gaping data<br>
    < 0: backward jump, overlapping data

- 3 *bcStatusEvent* Status Event<br>
  **int64**: Absolute timestamp in nano-seconds since epoch<br>
  **uint32**: Status word

- 4 *bcMessageEvent* Timestamped text entry<br>
  **int64**: Absolute timestamp in nano-seconds since epoch (applies ONLY to text message)
  **uint32**: L := length of the text message
  [L+1] times **uint8**: UTF-8 encoded text message with \0 termination.

- 5 *bcContinuedData* Append data with fixed sample rate (the most significant bit is always set)<br>
  **uint32**: N := number of samples<br>
  [N] times **Y**: Data according to channel description (time axis connects to previous data block.)

- 6 *bcStartData* First data block of data with fixed sample rate (the most significant bit is always set)<br>
  **int64**: Absolute timestamp in nano-seconds since epoch<br>
  **uint32**: N := number of samples<br>
  [N] times **Y**: Data according to channel description (time axis STARTS at this data block, e.g. for data stream with trigger control)

- 7 *bcContinuedRelStampData* Append data with relative timestamps<br>
  **uint32**: N := number of samples (if most significant bit is set, otherwise this does NOT exist and N:=1)
  **uint32**: relative distance to the previous data sample in nano-seconds
  [N] times **Y**: Data according to the channel description

- 8 *bcAbsTimeStampData* Append data with absolute timestamps (used also as the first data block with relative timestamped data)
  **uint32**: N := number of samples (if most significant bit is set, otherwise this does NOT exist and N:=1)
  **int64**: Absolute timestamp in nano-seconds since epoch
  [N] times **Y**: Data according to channel description

Restriction of block types with regard to channel information:

| Control byte | Equidistant data | Timestamped data |
|--------------|------------------|------------------|
| bcTrustedTimestamp | not allowed | allowed |
| bcTimebaseRealign | allowed | allowed |
| bcStatusEvent | N/A | N/A |
| bcMessage | N/A | N/A |
| bcContinuedData | allowed | not allowed |
| bcStartData | N/A | N/A |
| bcContinuedRelStampData | not allowed | allowed |
| bcAbsTimeStampData | N/A | N/A |

By synchronizing the time base to external sources like
GPS, DCF77 or NTP, e.g. for long time measurements in the data stream
time jumps can occur in any direction. The sequence of the measurement data
is therefore strictly monotonous with respect to the running time of the device,
but not w.r.t. the absolute time base.
Upon a time synchronization with time axis correction, in any case a
*bcTimebaseRealign* block is to be written.

With the following interpretation of the data, this information can be used for

- closing "gaps" by the insertion of certain error values
- correcting "overlaps" by cutting out data
- time stamp correction/recalculation of previous data

Several events can occur in one channel. For each
event a block *bcMessage* is generated with the UTC absolute time stamp value of the
event as well as an application specific text block.

With certain data reduction methods, the situation can arise
that a (timestamped) data sample remains valid for a long time.
Examples are Boolean channels in which only
changes are recorded or measured values that remain constant within a tolerance range
over long periods of time. For the representation of live data
the block *bcTrustedTimestamp* is inserted in the data stream in shorter intervals, typically at the
end of each transmitted time interval.
In a graphical representation one could draw a
constant curve until the given time without using a symbol for actual measuring data.,
but setting a different symbols for that measuring data. That interpretation is
optional.

#### Data with fixed time increment (equidistant)

For equidistant channel definition, a non-zero specification of the **timeincrement** attribute
denoting the equidistant time grid in nano-seconds is mandatory.

The data stream of an equidistant channel will then contain at least one *bcStartData* block
containing an absolute time specification of its first sample and a set of sample values
and mostly multiple *bcContinuedData* blocks containing additional sets of samples.
The resulting channel data (denoted as a "shot") is then attached in an adjacent way.

For multiple shots with larger time differences in between, multiple *bcStartData* blocks
are mandatory and the channel value is undefined between those shots.

The data blocks for timestamped information *bcTrustedTimestamp*,
*bcContinuedRelStampData*, *bcAbsTimeStampData*, *bcStartRelStampData*
must NOT be used in case of equidistant channel representation.

##### Examples of equidistant data blocks.

FIXME New to create

#### Data with timestamps

In the channel definition, a zero or missing specification of the **timeincrement**
attribute is required for channels with timestamped data.

The data stream of a timestamped channel will then contain various data blocks
for each record, depending on the block description, that record starting with

- either an **int64** absolute time stamp in nano-seconds since epoch **OR**
- or a **uint32** relative time stamp (roughly max. 4 seconds) denoting the interval to the preceeding data sample
  (if that maximum interval has been reached another absolutely timestamped data block is needed)

The data blocks for equidistant information *bcContinuedData*,
*bcStartData* must NOT be used in case of timestamped channel representation.

##### Examples for data with timestamp

FIXME New to be created

- Data samples according to data types and number of samples (t,y,t,y,t,y,...).
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
    - Example: data format=gpsdata; bit1=1; number of values=1;
        (1xunit64,3xdouble) 32 bytes to end of block
    - Example: Data format=candata; Bit1=1; Number of values=1; 1xuint64
        (8 bytes) + depending on 1st length byte - 6..13 bytes to end of block

### Special functions (Index \>= 0xFFFF)

Since it is extremely improbable (and not recommended) to have more than
65000 channels in one OSF file, the following index values
at the end of the value range are reserved for (future) special control functions:

- **0xFFFF** / **EndOFS**: Regular end of the OSF streaming file,
    final XML block

The structure of the data block for these entries follows the description for an
an XML option block.

- **uint16**: "channelindex" (== 0xFFFF).
- **uint32**: Length of the following option block (e.g. up to the
    beginning of the MAGIC-END tag)
- **uint8**: *bcMetaData* - control byte (== zero)
- **string**, XML block, UTF-8 without prologue
