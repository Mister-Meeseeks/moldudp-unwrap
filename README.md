# moldudp-unwrap
Simple python library for extracting messages from a MoldUDP byte stream

## Purpose

Serves as a simple utility and/or library to unpack raw messages from MoldUDP64 packets. Converts the binary MoldUDP64 stream to a stream of (size-prepended) binary messages. Underlying protocol (most likely ITCH) must be handled downstream.

## QuickStart

No installation is required besides cloning the repo. After cloning, test basic functionality by parsing the MoldUDP64 headers of sample data:

```
cd moldudp-unwrap/
./bin/moldudp --header <tests/mold.sample.dat
```

This prints packet header data from the sample file.

## Install

To install an executable binary to the system path, run:

```
cd moldudp-unwrap/
./install.sh
```

This installs a symbolic link to the ```bin/``` executable. You can now call ```moldudp``` from any working directory. By default install target is ```/usr/local/bin/```. If you want a different install target call:

```./install.sh [install target]```

## Usage

### Unpacking raw messages

Use the ```moldudp``` executable to convert a MoldUDP64 binary source to a binary stream of (length-prefixed) messages. Simply invoke the script. Pass a MoldUDP64 binary source to ```stdin``` and message output exits at ```stdout```

```
cd moldudp-unwrap/bin/
./moldudp <[moldUdp input] >[msg output]
```

```[moldudp input]``` - Either the path to a file or a pipe containing containing MoldUDP64 binary packet stream

```[msg output]``` - Either a writable file path or a pipe meant to receive a raw message binary stream

### Parsing packet headers

Packet header information can be read and printed using the ```moldudp``` executable with a ```--header``` flag. Simply follow the QuickStart example above, and substitute your own input file or pipe.

### Multicasting packets

Program can also be used to read the binary stream from stdin and multicast packets in order. Can be used to test live network clients with historical data. Invole the ```moldudp``` executable with ```--multicast [IpAddr]:[Port]``` where IpAddr is the IP address of the multicast group and Port is the port number of the group.

### Python libraries

Internal libraries can be used in other python applications. Add repo's ```src/``` directory to ```PYTHON_PATH```. Then include a ```import moldudp_unwrap.consume``` directive. See ```src/moldudp_unwrap/consume.py``` for function descriptions.

## Externals

### MoldUDP Protocol

Documentation for the protocol can be found at

http://business.nasdaq.com/Docs/moldudp64_tcm5044-18016.pdf

### Processing NASDAQ ITCH

Most likely you're interested in MoldUDP because it's the transport protocol used for NASDAQ ITCH market data. If so, you'll probably need an ITCH parser. For open-source projects my recommendation would be:

https://github.com/Amay22/NASDAQ-ITCH-5.0-Parser

## Requirements

- Python >=3.0
