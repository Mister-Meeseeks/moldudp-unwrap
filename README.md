# moldudp-unwrap
Simple python library for extracting messages from a MoldUDP byte stream

## Purpose

Serves as a simple utility and/or library to unpack raw messages from MoldUDP64 packets. Converts the binary MoldUDP64 stream to a stream of (size-prepended) binary messages. Underlying protocol (most likely ITCH) must be handled downstream.

## QuickStart

No installation is required besides cloning the repo. After cloning, test basic functionality by parsing the MoldUDP64 headers of sample data:

```
cd moldudp-unwrap/
./bin/parse_headers <tests/mold.sample.dat
```

This prints packet header data from the sample file.

## Unpacking raw messages

Use the ```packets_to_messages``` executable to convert a MoldUDP64 binary source to a binary stream of (length-prefixed) messages. Simply invoke the script. Pass a MoldUDP64 binary source to ```stdin``` and message output exits at ```stdout```

```
cd moldudp-unwrap/bin/
./packets_to_msgs <[moldUdp input] >[msg output]
```

```[moldudp input]``` - Either the path to a file or a pipe containing containing MoldUDP64 binary packet stream

```[msg output]``` - Either a writable file path or a pipe mean to receive a raw message binary stream

## Parsing packet headers

Packet header information can be read and printed using the ```parse_headers``` executable. Simply follow the QuickStart example, and substitute your own input file or pipe.

## Python libraries

Internal libraries can be used in other python applications. Add repo's ```src/``` directory to ```PYTHON_PATH```. Then include a ```import moldudp_unwrap.consume``` directive. See ```src/moldudp_unwrap/consume.py``` for function descriptions.

## Requirements

- Python 2
