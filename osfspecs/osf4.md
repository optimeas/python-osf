# optiMEAS Streaming Format Version 4

Keywords: OSF, OSF4

Documentation Version: 1.1
Last change date: 10.2023

## Changes

- Doc Layout reworked
- Tranlation to english

## Übersicht

In Messsystemen entstehen Daten verschiedenster Datentypen und Aufzeichnungsformate aus unterschiedlichsten Quellen. Angefangen bei physikalischen Messgrößen wie Drück, Schwingungen oder Temperaturen, über elektrische Größen, bis hin zu beliebigen binären Datenblöcken wie zum Beispiel Bildern. Diese Größen entstehen über einer Zeitachse. Entweder in festen Zeitintervallen oder Abtastraten, oder je nach dem wie sie sich verändern, mit individuellen Zeitstempeln.
Um diese Daten mit großer Zuverlässigkeit permanent speichern zu können, wird der Datenstrom mit Hilfe eines \"Streaming\" Formats in OSF-Dateien (optimeas -Streaming-Format) geschrieben.

Jede Datei beginnt mit einem Magic-Header, der das OSF-Format und den
Beginn des Binären Datenstroms markiert. Es folgt ein XML Block zur
Beschreibung der Kanäle, Datentypen und Aufzeichnungsformate.

Unterstützt werden:

- Standard Datentypen, wie momentan bool, double, float, int64, int32,
  int16, int8, string (Attribut \"datatype\")
- Skalierte Integer-Werte, um z.B. bei hohen abtastraten Speicher zu
  sparen (Skalierung via Attribut \"scale\")
- Erweiterte Datenformate mit anwendungsspezifischen Inhalten
  statischer oder dynamischer Länge
- Aufzeichnung zeitgestempelter oder äquidistanter Datensätze
- Aufzeichnung als Einzelwert, Liste von N-Werten (Vektor) oder
  Matrizen
- Beliebige Markierungen innerhalb des Datenstroms
- Wiederholte Resynchronisation auf die Zeitbasis,
- Binärdaten sind immer im Little Endian-Format (Intel) abgelegt
- Die Zeitbasis für alle Zeitangaben sind Nanosekunden (ns) seit
  Epoch, in Form eines int64_t Wertes

Weitere Informationen zu:

==== Beispiel einer OSF Datei ====

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
      <infos>
        <info name="Some UTF-8 String Value" datatype="string" value="This is a comment"/>
        <info name="Some Byte Array Value" datatype="bytearray" value="SGVsbG8sAFdvcmxkIQ=="/>
        <info name="Some Numerical Value" datatype="float" value="-42.1"/>
        <info name="Some Numerical Value 2" datatype="uint32" value="123"/>
        <info physicalunit="°C" name="system/CPU_Temperatur" type="double" value="43.4"/>
      </infos>
    </osf>
    [BEGIN OF BINARY DATA]...
```

Ab Position 30269 folgen binäre Daten, die mit der Zeit forschreitend
Datensätze der einzelnen Kanäle enthalten.

Der Info-Bereich ist optimal. Dort können Meta-Informationen in der
Datei zu den Messdaten gespeichert werden.

Folgende Einträge müssen vorhanden sein:

- name
- value

Ist kein Datentyp angegeben, wird \"string\" verwendet. Die restlichen
Paramter sind optional!

## Struktur des OSF4 Formats

Die OSF Datei besteht im Wesentlichen aus den folgenden Blöcken

1. MAGIC Header
2. XML Informationsblock zur Beschreibung der gespeicherten Daten
3. Binärer Datenblock
4. XML Abschlussblock (optional) zum schnellen Zugriff auf
   Informationen in den Daten
5. MAGIC Trailer (optional)

### MAGIC Header, OSF4

Der Magic Header der Datei enthält genau eine Zeile im ASCII Format, die
mit LF abgeschlossen ist. BOMs vom UTF-Format oder andere Kodierungen
sind am Anfang der Datei nicht enthalten.

Beispiel:

OSF4 173762\n

Die Integerzahl gibt an, wie viele Bytes im folgenden XML Header folgen.
Damit kann dieser beim Lesen sofort ausgeschnitten werden und einem
Parser zur Verarbeitung zugeführt werden.

### XML Metainformationen (Start)

Alle META-Blöcke (Start, Update, Ende) sind in UTF-8 mit **LF**
Unix-Zeilenenden (0x0A) kodiert. Die Dekodierung eines XML Texts mit
**LF** (0x0A) Umbrüchen sollte im Allgemeinen kein Problem für eine PC
Software darstellen.

### XML Prolog

Der XML-Block mit den META-Informationen zu jedem Kanal beginnt mit dem
typischen XML-Prolog:

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

mit dem XML Version und encoding festgelegt werden. Für OSF Files ist
dies immer UTF-8.

### XML Dokument-Knoten **osf**

Der Dokumentenknoten **osf** gibt weitere Informationen zum Dateiformat
und zum Ursprung der Datei.

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

Die Attribute des Knotens haben folgende Bedeutung:

- **version**: Versionierung des OSF-4 Formats, hier zunächst 1 [default: "1"]
- **created_utc**: System-Zeitstempel beim Erzeugen der Datei im ISO
    8601 konformen Format. Enthält Datum und Uhrzeit im UTC Format plus
    optional die Zeitzoneninformation
- **creator**: Ein Text, der das Objekt eindeutig identifiziert, das
    die Datei erzeugt hat. Das kann z.B. ein Programmname, eine
    Geräteseriennummer oder eine UUID sein.
- **created_at_longitude**: Optional. Geografische Länge beim Erzeugen
    der Datei. Sofern beim Erzeugen der Datei die Position bekannt ist,
    wird diese eingetragen.
- **created_at_latitude**: Optional. Geografische Breite beim Erzeugen
    der Datei. Sofern beim Erzeugen der Datei die Position bekannt ist,
    wird diese eingetragen.
- **created_at_altitude**: Optional. Geografische Höhe beim Erzeugen
    der Datei. Sofern beim Erzeugen der Datei die Position bekannt ist,
    wird diese eingetragen.
- **reason**: Grund für die Erstellung der Datei. Mögliche Werte:
 "BOOT" - Systemstart
 "SEQUENCE" - Aufteilung bezüglich Dateigröße oder zeitlicher Dateilänge
 "TRIGGERED" - Trigger-Bedingung erfüllt (steigende Flanke des Triggers)
- **total_seq_no**: Absoluter Index der Datei seit Systemstart
 beginnend mit 0.
- **triggered_seq_no**: Relativer Index der Datei seit letzter
 steigender Flanke des Triggers beginnend mit 0.
- **namespacesep**: Namespace Separator zur hierarchischen Anordnung
 der Kanalnamen. [default: "."]
- **tag**: Tag (Kategorie) des OSF Files [default: "preview"]
- **comment**: Benutzerdefinierter Kommentar

### Auflistung der Kanäle **channels**

Als derzeit einziger Unterknoten in *osf* ist die Liste der Kanäle
enthalten. Zukünftig könnten noch weitere Informationen, z.B.
Kommentare, Berechnungsvorschriften oder Filtereintellungen enthalten
sein.

```xml
    <channels count="181">
    ...
    </channels>
```

Die Attribute des Knotens haben folgende Bedeutung:

- **count**: Anzahl der aufgeführten Kanäle.

### Angaben zu einem Kanal **channel**

**Beispiel**

```xml
    <channel 
      index="0" 
      name="Kanal1" 
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
   
   <!-- für matrixwertige und vektorwertige Kanäle -->
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

Die Attribute des Knotens haben folgende Bedeutung:

- **index**: Indizierung innerhalb dieser Datei zur Identifikation
    einzelner Datensätze. Der Index beginnt für den ersten Kanal immer
    bei 0. Er ist monoton steigend. Der letzte Index ist somit die
    Kanalzahl minus 1.

- **reference**: \[optional\] Ein beliebiger Bezeichner oder eine
    UUID, die das Objekt eindeutig identifiziert, das die Daten erzeugt
    hat. Wird anwendungsspezifisch eingesetzt

- **name**: Kanalname ggf. mit Pfad. Ist die anwendungsbezogene
    Bezeichnung des Datenstroms.

- **physicalunit**: \[optional\] Anzeigeeinheit des Kanals,
    üblicherweise in SI-Notation, also mit Untescheidung von Klein- und
    Großbuchstaben, Vosatzzeichen etc., in zukünftigen SW-Versionen wird
    auf Basis dieser Einheitenbezeichnung auch Umgerechnet. [default: ""]

- **datatype**: Datentyp des Kanals. Neben Standardtypen für
    Boolesche-, Ganzzahl- und Fließkomma-Werte sind beliebige andere,
    applikationsspezifische Bezeichner für Datentypen zulässig.

- **cannode**: Nur gültig wenn datatype=candata ist. Nummer des CAN
    Knotes. Beginnend mit 1 wird hier die Nummer des CAN Knotens
    angegeben von dem die Daten erzeugt werden.

- **timeincrement**: \[optional\], Festes Zeitinkrement in
    Nanosekunden für äquidistant abgelegte Daten. Sofern
    **timeincrement** nicht angegeben oder \"0\" ist, werden die Daten
    mit einem Zeitstempel versehen. Abhängig von diesem Eintrag, werden
    die Datenblöcke für Daten mit festem Zeitinkrement und Daten mit
    Zeitstempel unterschiedlich aufgebaut. Siehe Blockdefinition.

- **channeltype**: Kanaltyp des Kanals. Hier wird der strukturelle
    Aufbau eines Datenblocks bereits vorab festgelegt. Abhängig von
    dieser Definition werden jeweils zusätzliche Beschreibungsparameter
    Attribut angelegt.
  - *scalar*: Kanal mit einem Datenpunkt pro Wert. Beispiel:
        datatype=\"double\" liefert eine Datenspur mit einem Wert über
        der Zeit. Beispiel datatype=\"gpsdata\" liefert die Geoposition
        über der Zeit.
  - *vector*: Kanal mit n Skalarwerten im Datenblock. Es entsteht
        ein eindimensionales Wertefeld mit dem angegebenen Datentyp über
        der Zeit. Beispiel: FFT oder eindimensionale Klassierungen über
        der Zeit.
  - *matrix*: Kanal mit y\[d1,d2\] Werte über x. n Wertepaare im
        Datenblock. Der x-Wert ist die absolute Zeit in Nanosekunden als
        int64. Beispiel: Rainflow-Klassiermatrix über der Zeit
  - *binary*: Kanal mit beliebigen Datenblöcken über der Zeit.
        Beispiel JPEG Dateien über der Zeit.
    [default: "scalar"]

- **sizeoflengthvalue**: \[erforderlich\], Jeder Datenblock hat
    unterschiedliche Länge, die mit dem hier spezifizierten Datentyp
    jedem Datenblock vorangestellt ist. Mögliche Werte sind:
  - *2*: 2-Byte integer - uint16, Längen bis 64 kByte\
        Genügt die maximale Blockgröße nicht, um alle Datensamples des
        Datenstroms aufzunehmen, wird der Datenstrom in mehrere,
        ausreichend kleine Blöcke geteilt.
  - *4*: 4-Byte integer - uint32, Längen bis 4 GByte (theoretisch)
    [default: "2"]

- **scale**: \[optional\] bei Integerdatentypen (scalar, vector,
    matrix). Skalierung des gespeicherten Integer-Wertes auf die
    gewünschte physikalische Größe
    [default: "1.0"]

- **offset**: \[optional\] bei Integerdatentypen (scalar, vector,
    matrix). Offset des skalierten Integer-Wertes auf die gewünschte
    physikalische Größe
    [default: "0.0"]

- **physicaldimension**: \[optional für zukünftige Erweiterungen\]
    engl. Bezeichnung der physikalischen Dimension, z.B.
    \"temperature\", \"force\", \"torque\", \"velocity\", \"pressure\",
    \...
    [default: ""]

- **comment**: \[optional\] Kommentar
 [default: ""]

- **displayname**: \[optional\] Name des Kanals in der Darstellung
 [default: ""]

- **uselogscale**: \[optional\] Einfach-logarithmische Darstellung verwenden
 [default: "false"]

- **mimetype**: \[optional\] MIME-Type des Kanalinhalts
 [default: ""]

- **spectrumtype**: \[optional\] Spektrumtyp des Kanals
 [default: "amplitude"]
 Mögliche Darstellungen:
  - \"amplitude\" - Darstellung reeller Funktionswerte (bzw. der Amplitude komplexer Funktionswerte)
  - \"realImag\" - Kartesische Darstellung komplexer Funktionswerte
  - \"ampPhaseRad\" - Polare Darstellung komplexer Funktionswerte (Phase im Bogenmaß)
  - \"ampPhaseDeg\" - Polare Darstellung komplexer Funktionswerte (Phase im Gradmaß)

- **rows**: \[optional\] Zeilenanzahl des matrix-/vektorwertigen Kanals
 [default: "1"]

- **row_caption**: \[optional\] Zeilenbeschreibung des matrix-/vektorwertigen Kanals
 [default: ""]

- **row_physicalunit**: \[optional\] Physikalische Einheit der Zeile des matrix-/vektorwertigen Kanals
 [default: ""]

- **row_min**: \[optional\] Minimale Stützstelle der Zeile des matrix-/vektorwertigen Kanals
 [default: "0.0"]

- **row_inc**: \[optional\] Stützstellen-Inkrement der Zeile des matrix-/vektorwertigen Kanals
 [default: "0.0"]

- **row_max**: \[optional\] Maximale Stützstelle der Zeile des matrix-/vektorwertigen Kanals
 [default: "0.0"]

- **row_align**: \[optional\] Visuelle Orientierung der Zeilenkomponente des Wertes eines matrix-/vektorwertigen Kanals
 [default: "center"]
 Mögliche Darstellungen:
  - \"left\" - Linkbündige Darstellung
  - \"center\" - Zentrierte Darstellung
  - \"right\" - Rechtsbündige Darstellung

- **row_labels**: \[optional\] zu klären mit JAK
 [default: ""]

- **columns**: \[optional\] Spaltenanzahl des matrix-/vektorwertigen Kanals
 [default: "1"]

- **column_caption**: \[optional\] Spaltenbeschreibung des matrix-/vektorwertigen Kanals
 [default: ""]

- **column_physicalunit**: \[optional\] Physikalische Einheit der Spalte des matrix-/vektorwertigen Kanals
 [default: ""]

- **column_min**: \[optional\] Minimale Stützstelle der Spalte des matrix-/vektorwertigen Kanals
 [default: "0.0"]

- **column_inc**: \[optional\] Stützstellen-Inkrement der Spalte des matrix-/vektorwertigen Kanals
 [default: "0.0"]

- **column_max**: \[optional\] Maximale Stützstelle der Spalte des matrix-/vektorwertigen Kanals
 [default: "0.0"]

- **row_align**: \[optional\] Visuelle Orientierung der Spaltenkomponente des Wertes eines matrix-/vektorwertigen Kanals
 [default: "center"]
 Mögliche Darstellungen:
  - \"left\" - Linkbündige Darstellung
  - \"center\" - Zentrierte Darstellung
  - \"right\" - Rechtsbündige Darstellung

- **row_labels**: \[optional\]  <!---zu klären mit JAK -->
 [default: ""]

Werden zur Datenreduktion Messwerte direkt als (signed) Integer Wert mit
kurzer Bitlänge gespeichert, müssen diese mittels der Attribute *scale*
und *offset* in die physikalische Größe umgewandelt werden. Es gilt:

physical = scale * binary + offset

#### Standarddatentypen

- Standarddatentypen sind (Encoding: Little-Endian (Intel)):
  - *bool*: 1-byte, true (== 1) /false (== 0)
  - *int8*: 1-byte, mit Vorzeichen
  - *int16*: 2-byte, mit Vorzeichen
  - *int32*: 4-byte, mit Vorzeichen
  - *int64*: 8-byte, mit Vorzeichen
  - *int64*: 8-byte, mit Vorzeichen - verwendet für Timestamp
  - *float*: 4-byte Fließkomma (single precision), [IEEE
        754](https://de.wikipedia.org/wiki/IEEE_754)
  - *double*: 8-byte Fließkomma (double precision), [IEEE
        754](https://de.wikipedia.org/wiki/IEEE_754)
  - *complex\<float\>*: (reserviert für zukünftige Anwendungen)
        real/imag Darstellung komplexer Zahlen, jeweils als float
  - *complex\<double\>*: (reserviert für zukünftige Anwendungen)
        real/imag Darstellung komplexer Zahlen, jeweils als double
  - *string*: UTF-8 kodierte Zeichen ohne Stringterminierung. Die
        Länge wird durch die Blockbeschreibung vorgegeben.
  - *candata*: Enhält folgenden struct zur Beschreibung einer
        CAN-Botschaft, erweitert die Definition in       
    ```C
        include/linux/can.h 
        struct can_frame {
            uint32 can_id;  /* 32 bit CAN_ID + EFF/RTR/ERR flags */
            uint8  can_dlc; /* frame payload length in byte (0 .. 8) */
            uint8  data[8];
        }  __attribute__((aligned(8)));
    ```

  - *gpsdata*: Longitude, Latitude, Altitude - jeweils als double-Wert ensprechend folgendem struct: 
    ```C
        struct gps_location {
            double longitude;
            double latitude;
            double altitude;
        };
    ```

[//]: # (*FIXME STH überarbeiten!*)
<!--- 

**gpsinfo:**: Verschiedene Informationen zum GPS Empfang ensprechend folgendem C-struct:

```C
    struct gps_info {
      uint8 satcount;   // Anzahl Satelliten
      uint8 qos;        // Quality of Service
      uint64 time;      // GPS-Zeit
    };
```

Weitere Informationen über die Definition von [Vectoren und Matrizen ist hier zu finden] (/entwicklung/fileformats/stream4/vector)
-->

### Binärer Datenblock

Der binäre Datenblock beginnt direkt im Anschluss an die XML
Kopfinformation. Die Position in der Datei wird im MAGIC HEADER
angegeben: `OSF4 173762\n
`

Grundsätzlich ist die Datei in einzelne Datenblöcke gegliedert. Jeder
Datenblock beschreibt eine Folge von 1 bis N Datensamples eines Kanals.
Der Datenstrom des Kanals kann in folgenden Blöcken fortgesetzt werden.
Jeder Datenblock zeigt durch Angabe seine Größe automatisch auf den
nächsten folgenden Datenblock. Dies erlaubt es, dass selbst beim
unmittelbaren Abbruch des Schreibvorgangs (z.B. durch Stromausfall oder
Unterbrechung der Datenverbindung) die Daten bis zum Ende des
Datenstroms/Datei lesbar bleiben.

Der grundsätzliche Aufbau des Datenformates erlaubt es somit:

1. nicht benötigte Informationen einfach zu überspringen
2. beliebige Daten- und Kanaltypen anwendungsspezifisch nachzurüsten
3. nicht bekannte Datenblöcke zu ignorieren
4. die Daten bis zum letzten Datenblock interpretieren zu können

#### Gleicher Einstieg für alle Datenblöcke

Der Beginn eines binären Datenblocks ist wie folgt definiert:

- **uint16**, Kanalindex (wie in Version 3 auch)
- **\<sizeoflengthvalue\>**: In der Kanalbeschreibung des Headers
    definiert. Abhängig von der Definition der Größe des Datenwortes für
    die Längenangabe des nachfolgenden Blockes 2-4 Byte (uint16,uint32):
    Anzahl der nachfolgenden Bytes für Steuerbyte, Metainformation und
    die eigentlichen Datensamples.
  - Der nächste Kanaldatenblock beginnt somit bei
        \<start\>+2+\<sizeoflengthvalue\>+\<Größe des Datenblocks in
        Byte\>
  - Sollte das Schreiben der Datei vorzeitig abgebrochen worden
        sein, liegt das Ende des Datenblocks jenseits vom Dateiende. In
        diesem Fall kann bis zum Dateiende weiter gelesen werden, sofern
        jeweils ein vollständiges Datensample dekodiert werden kann. Ein
        unvollständiges Datensample wird verworfen.
- **uint8**, **Steuerbyte**, bestimmt den Inhalt des nachfolgenden
    Metainformationsblocks im Datenstrom

Durch die Angabe der Größe des Blocks kann der Datenblock bei Fehlern
oder unbekanntem oder (noch) nicht implementiertem **channeltype** bzw.
**datatype** übersprungen werden oder auch zum Interpretieren in einem
Stück eingelesen werden.

Bei Interpretations- oder Datenfehlern in einem Block kann, unter Angabe
einer entsprechenden Fehlermeldung, der Datenstrom für den jeweiligen
Kanal zunächst unterbrochen werden. Die Interpretation des OSF Streams
kann mit dem nächsten Block fortgesetzt werden. Weitere Datenblöcke zu
dem Kanal können ignoriert werden, bis ein absoluter Zeitstempel die
korrekte Interpretation der Daten wieder erlaubt.

Es werden grundsätzlich zwei verschiedene Arten von Kanälen
unterschieden:

- Kanäle mit festem Zeitinkrement (äquidistant)
- Kanäle mit Zeitstempel an jedem Datensample

#### Steuerbyte und Metainformationen im Datenstrom

Das Steuerbyte ist für alle Kanal- und Datentypen gleich und bestimmt,
welche Metainformationen noch vor den eigentlichen Daten des Blocks
eingefügt werden.

Um die Anzahl der Implementierungsvarianten zu reduzieren, wird der
Aufbau des nachfolgenden Datenblocks über einen 7-bit ENUM und ein
Steuerbit angegeben.

Das Steuerbit 7 zeigt an, ob in dem Datenblock 1- oder
n-Werte/Wertepaare enthalten sind.

Der Aufbau des Steuerbytes **blockContent** als Werte-Aufzählung ist wie
folgt:

| Wert | Enum | Bedeutung | Datenblock       |
| ---- |------| ----------| -----------------|
| 0    | *bcMetaData* | Einsatz dieses Blocktyps nur für internen Gebrauch, z.B. Sonderfunktionen und Dateiabschluss, keinem Kanal zugeordnet.| **uint32**: L := Länge des Textblocks<br/>**uin8\[L+1\]**: UTF-8 kodierter Textblock mit \'0\' Terminierung.|
| 1    | *bcTrustedTimestamp* | Absoluter Zeitstempel in \"ns since Epoch\",<br/>der vorherige Datenwert ist bis zu diesem Zeitpunkt gültig und konstant<br> <!--- [\"Trusted Timestamp\"](/entwicklung/fileformats/stream4/trusted) Link muss gefixt werden oder Beschreibung in das Dokument packen! --> | **int64**: ns since Epoch |
| 2    | *bcTimebaseRealign* | Anpassung der Zeitachse | **int64**: Absoluter Zeitstempel in \"ns since Epoch\"<br/>**int64**: Verschiebung des Zeitbasis in ns.<br/><br/>\> 0: Vorwärts Sprung, lückende Daten<br/><br/> \< 0: Rückwärts Sprung, überlappende Daten |
| 3    | *bcStatusEvent* |Status Event | **int64**: Absoluter Zeitstempel in \"ns since Epoch\"<br>**uint32**: Status-Word|
| 4    | *bcMessageEvent* | Zeitgestempelter Texteintrag|**int64**: Absoluter Zeitstempel in \"ns since Epoch\", gilt NUR für Textmeldung.<br>**uint32**: L := Länge der Textmeldung.<br>**uin8\[L+1\]**: UTF-8 Kodierte Textmeldung it \'\\0\' Terminierung.|
| 5    | *bcContinuedData* | Daten mit fester Abtastrate anhängen| wenn Option Bit 7 gesetzt:<br>**uint32**: N := Anzahl der Samples,<br>\... sonst N := 1<br>**Nx**:<br>**Y**: Daten gemäß Kanalbeschreibung (Zeitachse schließt an vorherigen Datenblock an.)|
| 6    | *bcStartData* |Erster Datenblock mit Daten fester Abtastrate im Stream| **int64**: Absoluter Zeitstempel in \"ns since Epoch\"<br>wenn Option Bit 7 gesetzt:<br>**uint32**: N := Anzahl der Samples,<br>\... sonst N := 1<br> **Nx**:<br>**Y**: Daten gemäß Kanalbeschreibung (Zeitachse beginnt in diesem Datenblock, z.B. für Datenstrom mit Trigger-Steuerung)|
| 7    | *bcContinuedRelStampData* |Daten anhängen mit relativem Zeitstempel| wenn Option Bit 7 gesetzt:<br>**uint32**: N := Anzahl der Samples,<br>\... sonst N := 1<br>**Nx**:<br>**uint32**: relativer Abstand zum vorherigen Datensample in ns<br>**Y**: Daten gemäß Kanalbeschreibung.|
| 8    | *bcAbsTimeStampData* | Daten anhängen mit absolutem Zeitstempel. Kann auch der erste Datenblock mit relativen Zeitstempeln sein.| wenn Option Bit 7 gesetzt:<br>**uint32**: N := Anzahl der Samples,<br>\... sonst N := 1<br>**Nx**:<br>**int64**: Absoluter Zeitstempel in \"ns since Epoch\"<br>**Y**: Daten gemäß Kanalbeschreibung|

Einschränkung der Blockarten im Hinblick auf die Kanalinformation:

| ENUM-Typ      | Äquidistante Daten | Zeitgestempelte Daten |
| ------------- |-------------| -----|
| bcTrustedTimestamp     | nicht erlaubt | erlaubt
| bcTimebaseRealign      | erlaubt | erlaubt |
| bcStatusEvent          | N/A | N/A |
| bcMessage              | N/A | N/A |
| bcContinuedData        | erlaubt | nicht erlaubt |
| bcContinuedRelStampData | nicht erlaubt | erlaubt|
| bcAbsTimeStampData | N/A | N/A |

Durch die Synchronisation der Zeitbasis auf externe Quellen wie z.B.
GPS, DCF77 oder NTP, können z.B. bei Langzeitmessungen im Datenstrom
Zeitsprünge in beliebiger Richtung auftreten. Die Folge der Messdaten
ist somit in Bezug auf die Laufzeit des Gerätes zwar streng monoton,
nicht jedoch die Zuordnung zur absoluten Zeitbasis. Bei einer
Zeitsynchronsiation mit Korrektur der Zeitachse wird auf jeden Fall ein
*bcTimebaseRealign*-Block geschrieben. Bei der nachfolgenden
Interpretation der Daten können mit diesen Informationen

- \"Lücken\" durch das Einsetzen von bestimmten Fehlerwerten
    geschlossen werden
- \"Überlappungen\" durch das herausschneiden von Daten behoben werden
    oder
- Zeitstempel vorangehender Daten korrigiert / neu berechnet werden.

Es können mehrere Ereignisse in einem Kanal auftreten. Für jedes
Ereignis wird ein Block *bcMessage* mit dem UTC-Absolutzeitwert des
Ereignisses sowie einem anwendungsspezifischen Text-Blocks kodiert.

Bei bestimmten Datenreduktionsverfahren kann die Situation eintreten,
dass ein (zeitgestempeltes) Datensample über lange Zeit hinaus
Gültigkeit behält. Beispiele sind Boolsche-Kanäle, bei denen nur
Änderungen aufgezeichnet werden oder Messwerte, die über lange Zeiträume
in einem Toleranzband konstant bleiben. Zur Darstellung von Life-Daten
wird der Block *bcTrustedTimestamp* in kürzeren Abständen in den
Datenstrom eingebaut, typischerweise zum Ende jedes übertragenen
Zeitintervalls. In einer grafischen Darstellung könnte man eine
konstante Kurve bis zum angegebenen Zeitpunkt weiter zeichnen ohne dabei
aber ein Symbol für einen Messpunkt zu setzen. Die Interpretation ist
optional. Bei Schreiben in eine Datei wird *bcTrustedTimestamp* vor dem
Dateiabschluss für die entsprechenden Kanäle eingebaut.

#### Daten mit festem Zeitinkrement (äquidistant)

In der Kanaldefinition ist für Kanäle mit festem Zeitinkrement die
Angabe des **timeincrement** mit einem Wert [ungleich Null]{.ul} in
nano-Sekunden (ns) zwingend.

Der Datenstrom des Kanals enthält nach der Kopf- und Metainformation als
erstes einen *bcStartData*-Block. Die Datensätze sind in *bcStartData*-
oder *bcContinuedData*-Blöcken abgelegt und starten entweder mit dem
gegebenen Zeitstempel z.B: nach einem Trigger-Ereignis neu (\"Segment\")
oder schließen an den bereits übertragenen Datenstrom an.

Die Blöcke für zeitgestempelte Informationen *bcTrustedTimestamp*,
*bcContinuedRelStampData*, *bcAbsTimeStampData*, *bcStartRelStampData*
dürfen bei äquidistanter Abtastung nicht verwendet werden.

<!--- 

##### Beispiele für äquidistante Datenblöcke

FIXME Neu zu erstellen

-->

#### Daten mit Zeitstempel

In der Kanaldefinition ist für Kanäle mit zeitgestempelten Datensätzen
die Angabe des **timeincrement** nicht enthalten oder Null.

Der Datenstrom des Kanals enthält nach der Kopf- und Metainformation für
jeden Datensatz je nach Blockbeschreibung

- optional einen **int64** Wert als Zeitmarke für den nächsten
    Relativwert
- zwingend an jedem Datensatz
  - einen **int64** Absolut-Zeitstempel in ns since Epoch **ODER**
  - einen **uint32** Wert als relativer Zeitabstand (max. 4
        Sekunden) zum vorangehen Datensample

Die Blöcke für äquidistante Informationen *bcContinuedData*,
*bcStartData* dürfen bei äquidistanter Abtastung nicht verwendet werden.

##### Beispiele für Daten mit Zeitstempel

[//]: # (FIXME Neu zu erstellen)

- Datensamples gemäß Datentypen und Anzahl Samples (t,y,t,y,t,y\...)
  - Für jedes Datenpaar: **uint32** als relative Zeit zum letzten
        Datensample oder zum letzten absoluten Zeitstempel. Der
        Datenwert dann entsprechend Kanaldefinition und **datatype**
  - Beispiel: Datenformat=double; Bit0=1; Anzahl Werte=1; (1xuint64,
        1xdouble) 16 Byte bis Blockende
  - Beispiel: Datenformat=double; Bit0=0; Anzahl Werte=1; (1xuint32,
        1xdouble) 12 Byte bis Blockende
  - Beispiel: Datenformat=int32; Bit1=0; valueorder=multiplex;
        Anzahl Werte=20; (20x (uint32, int32)) 160 Byte bis Blockende
  - Beispiel: Datenformat=int32; Bit1=1; valueorder=multiplex;
        Anzahl Werte=20; (20x (uint64, int32)) 168 Byte bis Blockende
  - Beispiel: Datenformat=int32; Bit1=0; valueorder=linear; Anzahl
        Werte=20; (20xuint32, 20xint32) 160 Byte bis Blockende
  - Beispiel: Datenformat=int32; Bit1=1; valueorder=linear; Anzahl
        Werte=20; (20xuint64, 20xint32) 240 Byte bis Blockende
  - Beispiel: Datenformat=gpsdata; Bit1=1; Anzahl Werte=1;
        (1xunit64,3xdouble) 32 Byte bis Blockende
  - Beispiel: Datenformat=candata; Bit1=1; Anzahl Werte=1; 1xuint64
        (8 Byte) + abhängig vom 1. Längenbyte - 6..13 Byte bis Blockende

### Sonderfunktionen (Index \>= 0xFFFF)

Da es extrem unwahrscheinlich ist (bzw. nicht sehr geschickt ist), mehr
als 65000 Kanäle in einer OSF Datei abzulegen, sind folgende Index-Werte
am Ende des Wertebereichs für besondere Steuerfunktionen reserviert:

- **0xFFFF** / **EndOFS**: Reguläres Ende der OSF Streaming Datei,
    abschließender XML Block

Der Aufbau des Datenblocks für diese Einträge folgt der Beschreibung für
einen XML-Optionsblock.

- **uint16**: \"Kanalindex\" (== 0xFFFF)
- **uint32**: Länge des nachfolgenden Optionsblocks (z.B. bis zum
    Anfang des MAGIC-END-Tags)
- **uint8**: *bcMetaData* - Steuerbyte (== Null)
- **string**, XML-Block, UTF-8 ohne Prolog

Diese Block ist optional und muss nicht zwingend in einer Osf-Datei enthalten sein!

### Aufbau des abschliessenden Frames

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

- **finalized_utc**: Zeitpunkt (Systemzeit), zu dem die Datei
    geschlossen wurde
- **reason**: Grund für das Dateiende, z.B:
  - *maxFileLen_kB*: Schließen der Datei wurde beim Erreichen der
        maximalen Dateigröße (Speicher) ausgelöst
  - *maxFileLen_s*: Schließen der Datei wurde beim Erreichen der
        maximalen Dateilänge (Zeit) ausgelöst
  - *fileStartGrid_min*: Schließen der Datei wurde beim Erreichen
        des nächsten Zeitrasterpunktes (z.B. um jeweils :00, :15, :30
        und :45 einer Stunde) ausgelöst.
  - *triggerEnd*: Schließen der Datei wurde mit Ende einer
        Trigger-Periode ausgelöst (ein Ereignis pro Datei)
  - \...: weitere applikationsspezifische Hinweise.
  - *shutDown*: OsfWriter Objekt wurde bei offener Datei gelöscht,
        in diesem Fall könnten die Kanalangaben unvollständig sein.

#### \<channels\>

- **count**: Anzahl der Kanäle beim Schließen der Datei

#### \<channel\>

- **index**: Kanalindex
- **first_ns**: hochauflösender ns-Zeitstempel des ersten Datensamples, UTC Nano-Seconds since Epoch (1970)
- **samples**: Anzahl der tatsächlich enthaltenen Datensamples
- **last_ns**: hochauflösender ns-Zeitstempel des letzten Datensamples, UTC Nano-Seconds since Epoch (1970)

### MAGIC Trailer, OSF_STREAM_END

Der abschließende Trailer ist immer 40 Byte lang

```json
OSF_STREAM_END 321316454==============
```

Dahinter folgen \'=\'-Zeichen, um auf die 40 Bytes aufzufüllen.

Die angegebene Zahl entspricht der Seek-Position in der Datei, an der
der abschließende XML-Datenblock mit statistischen Informationen
beginnt, also genau der 0xFFFF Steuercode als nächstes zu lesen wäre.