#!/usr/bin/env python
#
#
#

import sys, time
from socket import socket, gethostname
from chirp import Chirp


server = "bogwoppit.lan.pointless.net"
port = 2003


sock = socket()
try:
  sock.connect( (server, port) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':server, 'port':port }
  sys.exit(1)

addr = 0x51
hostname = gethostname()

chirp = Chirp(1, addr)

delay = 30

while True:
  lines = []
  #We're gonna report all three loadavg values
  lines.append("chirp.%s.%x.cap_sense %s %d" % (hostname, addr, chirp.cap_sense(), int(time.time()) ))
  lines.append("chirp.%s.%x.temp %s %d" %      (hostname, addr, chirp.temp(),      int(time.time()) ))
  lines.append("chirp.%s.%x.light %s %d" %     (hostname, addr, chirp.light(),     int(time.time()) ))
  message = '\n'.join(lines) + '\n' #all lines must end in a newline
  print "sending message\n"
  print message
  try:
    sock.sendall(message)
  except Exception, e:
    print e
    sock.close()
    sock = socket()
    try:
      sock.connect( (server, port) )
    except Exception, e:
      print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':server, 'port':port }
    else:
      sock.sendall(message)

  sys.stdout.flush()
  time.sleep(delay)
