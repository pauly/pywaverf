#!/usr/bin/env python
"""
This module accesses the custom Lightwaverf extension in Pigpio

Pigpio must have been built with the Lightwave custom extension
Pigpiod must be running (sudo pigpiod)

"""

import time
import pigpio
import yaml
import sys
import lwrfCustom

# Pigpio custom extension calls for Lightwaverf
CUSTOM_LWRF           =7287
CUSTOM_LWRF_TX_INIT   =1
CUSTOM_LWRF_TX_BUSY   =2
CUSTOM_LWRF_TX_PUT    =3
CUSTOM_LWRF_TX_CANCEL =4
CUSTOM_LWRF_TX_DEBUG  =5
LWRF_MSGLEN           =10

TX_PIN = 25
TX_REPEAT = 5

class robot_butler():

  def __init__(self):
    """
    Initialise and load the config
    """
    with open('lightwaverf-config.yml', 'r') as stream:
      self.config = yaml.safe_load(stream)
    self.pi = pigpio.pi() # Connect to local Pi.
    self.tx = tx(self.pi, TX_PIN) # Specify Pi, tx gpio, and baud.

  def stop(self):
    self.tx.cancel()
    self.pi.stop()

  def parseCommand(self, args):
    """
    Interpret the command line
    """
    # if this then that
    if len(args) == 4:
      self.send(*args[1:])
    else:
      print('usage:', args[0], 'room device [on/off] [debug]' )

  def send(self, room, device, status = 'on', debug = False):
    """
    Send a command to a device
    """
    for r in range( len( self.config['room'] )):
      if self.config['room'][r]['name'] != room:
        continue
      for d in range( len( self.config['room'][r]['device'] )):
        if self.config['room'][r]['device'][d]['name'] != device:
          continue
        print('send', room, device, d)
        # Level      2 bit     Device setting
        # Device     1 bit     Device ID, relative to room and remote
        # Command    1 bit     On/Off/Mood
        # Remote ID  5 bit     Remote ID
        # Room       1 bit     Room ID, relative to device and remote
        # byte msg[] = { 0x00, 0x00, 0x02, 0x01, 0x0F, 0x00, 0x0D, 0x0C, 0x02, 0x08 }; // lounge light on as black remote
        analog = 0
        status = 0
        command = '{:02d}{:1}{:1}{:5}{:1}'.format(analog, d, status, '30FDA', r)
        print 'Transmit testing sending', command, TX_REPEAT, "times"
        self.tx.put(command, TX_REPEAT)

class tx():

  def __init__(self, pi, txgpio):
    """
    Initialise a transmitter with the pigpio and the transmit gpio.
    """
    self.pi = pi
    (count, data) = self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_TX_INIT, txgpio])

  def put(self, data, repeat=1):
    """
    Transmit a message repeat times
    0 is returned if message transmission has successfully started.
    Negative number indicates an error.
    """
    ret = 0
    if len(data) <> LWRF_MSGLEN:
      ret = -1
    else:
      argx = [CUSTOM_LWRF_TX_PUT, repeat]
      argx.extend(list(data))
      self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_TX_CANCEL])
      (count, data) = self.pi.custom_2(CUSTOM_LWRF, argx)
    return ret

  def ready(self):
    """
    Returns True if a new message may be transmitted.
    """
    (count, data) = self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_TX_BUSY])
    if (count == 0):
      return True
    else:
      return False

  def cancel(self):
    """
    Cancels the wireless transmitter, aborting any message
    in progress.
    """
    self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_TX_CANCEL])

if __name__ == "__main__":

  instance = robot_butler()
  instance.parseCommand(sys.argv)
  instance.stop()
