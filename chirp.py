#!/usr/bin/env python

import smbus, time, sys

class Chirp:
  def __init__(self, bus=1, address=0x20):
    self.bus_num = bus
    self.bus = smbus.SMBus(bus)
    self.address = address

  def read(self):
    ok = False
    val = None
    count = 0
    while not ok:
      try:
        # sometime reading raises an IOError, i don't know why.
        val = self.bus.read_byte(self.address)
        ok = True
      except IOError:
        time.sleep(0.1)
        count = count + 1
        if count > 5:
          raise
        pass
    return val

  def write(self, reg):
    count = 0
    ok = False
    while not ok:
      try:
        # sometime writing raises an IOError, i don't know why.
        self.bus.write_byte(self.address, reg)
        ok = True
      except IOError:
        time.sleep(0.1)
        count = count + 1
        if count > 5:
          raise
    
  def get_reg(self, reg):
    self.write(reg)
    time.sleep(0.1)

    b1 = self.read()
    b2 = self.read()

    # if the chrip has no data it sends
    # 0xff, use this to re-sync in case we loose values.
    t = self.read()
    while t != 0xff:
      t = self.read()
    return (b1 << 8) + b2
    
  def cap_sense(self):
    return self.get_reg(0)

  def temp(self):
    return self.get_reg(5)

  def light(self):
    self.write(3)
    time.sleep(1.5)
    return self.get_reg(4)

  def __repr__(self):
    return "<Chirp sensor on bus %d, addr %d>" % (self.bus_num, self.address)

if __name__ == "__main__":
  addr = 0x20
  if len(sys.argv) == 2:
    if sys.argv[1].startswith("0x"):
      addr = int(sys.argv[1], 16)
    else:
      addr = int(sys.argv[1])
  chirp = Chirp(1, addr)

  while True:
    print "cap", chirp.cap_sense()
    print "temp", chirp.temp()
    print "light", chirp.light()
    time.sleep(1)
    print
