## Introduction
ADSB2JSON connects to your dump1090 instance on an external server (or localhost).  Data from the raw messages is transformed by ADSB2JSON to a JSON format which is exposed on a TCP port.  The user can connect to the ADSB2JSON TCP port using telnet, or similar, to see a JSON version of the ADSB messages.

## Requires dump1090
The use of this software requires dump1090, which can be downloaded from a variety of websites.  I recommend sending your data to PlaneFinder and downloading the PlaneFinder client because FlightAware is evil and PlaneFinder will give you a free premium subscription for offering up data.  See https://planefinder.net/sharing/.

## Installation and Prerequisites
This code has been tested on Ubuntu 16.04 with Python 3.7, but should work with anything moderately newer as well.  Lower versions YMMV.

Assuming you have a vanilla minimal install, the following must be installed:

`sudo apt-get install python3-setuptools librtlsdr git-core`

Then install pip
`sudo easy_install3 pip`

Then clone the install
`git clone https://github.com/BrentIO/ADSB2JSON.git`

## Configuration
Edit the config.json file and place it in the same directory as adsb2json.py.  A sample is included with the git.  If no configuration file is specified, config.json will be used.  If that file is not found, the script will fail.

*serverName* is the IP address or DNS name of your dump1090 instance.

*serverPort* is the port dump1090 is exporting to.  Recommend 30002, which outputs raw messages.  Usage of other inputs is supported by pyModeS, but hasn't been tested for compatibility or message completeness.

*serverType* must match the output from *serverPort* above.  When using serverPort 30002, use serverType = *raw*.

*listenAddress* is the IP address of the device which will be running this script.  This is usually going to be 0.0.0.0 (bind to all addresses) unless you have multiple network interfaces and want to only bind to a specific IP address.

*listenPort* is the port on the device which will output the transformed JSON data.

*latitude* is the devices latitude in decimal form.  The latitude/longitude used in the example is for the White House in Washington, DC USA.

*longitude* as above, but longitude.

*debug* this can be set to false or completely omitted.  It should be set to True only if you're actually debugging as it will output unsupported messages.  Do not use debug=true for a production installation.

## Launch
`python adsb2json.py`

TO DO: Create an init.d script to automatically launch and control the process.

## Connecting
`telnet 127.0.0.1 7740`

Assuming the adsb2json.py file and dump1090 is running on your local machine, this should immediately start outputting ADS-B messages of various types to your window.

## Credit
This was forked from https://github.com/junzis/pyModeS, which did all of the heavy lifting.  Many thanks for their massive help.
