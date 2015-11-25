#!/usr/bin/env python
"""
Control your lightwaverf devices by name
A python port of https://rubygems.org/gems/lightwaverf
"""

import time
import pigpio
import yaml
import sys
import time

# Pigpio custom extension calls for Lightwaverf
CUSTOM_LWRF           =7287
CUSTOM_LWRF_TX_INIT   =1
CUSTOM_LWRF_TX_BUSY   =2
CUSTOM_LWRF_TX_PUT    =3
CUSTOM_LWRF_TX_CANCEL =4
CUSTOM_LWRF_TX_DEBUG  =5
LWRF_MSGLEN           =10

TX_PIN = 25
TX_REPEAT = 10

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
    time.sleep(0.5)
    self.tx.cancel()
    self.pi.stop()

  def parseCommand(self, args):
    """
    Interpret the command line
    """
    
    if args[1] == 'help':
      return self.help(*args[1:])
    if args[1] == 'configure':
      return self.configure(*args[1:])
    if args[1] == 'sequence':
      return self.sequence(*args[1:])
    if args[1] == 'mood':
      return self.mood(*args[1:])
    if args[1] == 'energy':
      return self.energy(*args[1:])
    if args[1] == 'update_timers':
      return self.updateTimers(*args[1:])
    if args[1] == 'timer':
      return self.runTimers(*args[1:])
    if args[1] == 'run_timers':
      return self.runTimers(*args[1:])
    if args[1] == 'update':
      return self.updateConfig(*args[1:])
    if args[1] == 'summarise':
      return self.summarise(*args[1:])
    if args[1] == 'web':
      return self.buildWebPage(*args[1:])
    if len(args) >= 4:
      return self.send(*args[1:])
    print('usage:', args[0], 'room device [on/off] [debug]')

  def send(self, room, device, status = 'on', debug = False):
    """
    Convert a room name + device name to ids, and send
    """
    for r in range( len( self.config['room'] )):
      if self.config['room'][r]['name'] != room:
        continue
      for d in range( len( self.config['room'][r]['device'] )):
        if self.config['room'][r]['device'][d]['name'] != device:
          continue
        # Level      2 bit     Device setting
        # Device     1 bit     Device ID, relative to room and remote
        # Command    1 bit     On/Off/Mood
        # Remote ID  5 bit     Remote ID
        # Room       1 bit     Room ID, relative to device and remote

        # print( 'dining light on   1F 0 1 30FDA 1' )
        # print( 'dining light off  00 0 0 30FD0 1' )
        # print( 'dining all off    40 1 0 30FDA 1' )

        analog = 0x1f 
        digital = 1
        if status == 'off':
          analog = 0
          digital = 0

        command = '{:02X}{:1X}{:1X}{:5}{:1X}'.format(analog, d, digital, '30FDA', r)
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

  import robotButler

  instance = robot_butler()
  instance.parseCommand(sys.argv)
  instance.stop()
