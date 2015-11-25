# pywaverf
A port of my https://github.com/pauly/lightwaverf repo to python

LightWaveRF wifi link communication for command line home automation, google calendar timing of your electrics, energy monitoring, etc http://www.clarkeology.com/wiki/lightwaverf 

 Interact with lightwaverf sockets and switches from code or the command line - no need for wifi link.
 Control your lights, heating, sockets, sprinkler etc.
 Also use ical calendar, for timers, log energy usage, and build a website.

## hardware

You need:
 * a [raspberry PI](https://www.raspberrypi.org), any model
 * a [434 mhz transmitter](http://rover.ebay.com/rover/1/710-53481-19255-0/1?type=4&campid=5335822550&toolid=10001&customid=23714&mpre=http%3A//www.ebay.co.uk/itm/RASPBERRY-PI-2-Model-B-1GB-RAM-Quad-Core-CPU-/261698200759%3Fhash%3Ditem3cee6da4b7:g:c3gAAOSw-vlVnWYt 434 mhz transmitter) - costs peanuts on ebay, though I got mine from https://www.coolcomponents.co.uk/rf-link-transmitter-434mhz-812.html
 * some [female to female jumper wires](http://rover.ebay.com/rover/1/710-53481-19255-0/1?type=4&campid=5335822550&toolid=10001&customid=23714&mpre=http%3A//www.ebay.co.uk/itm/40-Pcs-Dupont-Jumper-Wire-M-M-M-F-F-F-Cable-Pi-Pic-Breadboard-For-Arduino-sb-/111651703549%3Fvar%3D%26hash%3Ditem19fef5cafd:m:m3sOQpdhEMxD_INQbk7Cl9g) also peanuts

Check the datasheet for the transmitter component, it should have four pins. Also [search for a GPIO diagram](https://www.google.co.uk/search?q=raspberry+pi+gpio).
 * Pin 1 on the transmitter is ground, so connect this with a jumper wire to ground on the pi (if you're looking down on the pi, and the gpio is to the top right, then the tenth pin down on the right is ground).
 * Pin 2 on the transmitter is the signal, connect that to GPIO24, the 9th pin down on the right.
 * Pin 3 on the transmitter is 3.3v so connect that to the first pin down on the left of your pi.
 * Pin 4 on the transmitter is for an arial - connect a 13cm length of wire to this for best results.

## software

To install:
```
Make install
```

## references / links

[*] http://abyz.co.uk/rpi/pigpio
[*] https://github.com/roberttidey/LightwaveRF.git

More to come...
