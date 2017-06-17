#!/usr/bin/env python
#
#
#

import sys, time, argparse, graphiteclient
from chirp import Chirp

server = "bogwoppit.lan.pointless.net"
port = 2003

parser = argparse.ArgumentParser(description='send chirp stats to graphite.')

parser.add_argument('--server', type=str,
  help='The graphite server hostname')

parser.add_argument('--port',
  type=int,
  help='The graphite server port (defaults to 2003)')

bus = 0
parser.add_argument('--bus',
  type=int,
  help='The i2c bus to use')

addr = 0x52
parser.add_argument('--address',
  type=str,
  help='The device address on the i2c bus')
#
parser.add_argument('--overrideaddress',
  type=str,
  help='Override the address used in the graphite metric')

args = parser.parse_args()

if args.server:
  server = args.server

if args.port:
  port = args.port

if args.bus:
  bus = args.bus

if args.address:
  if args.address.startswith("0x"):
    addr = int(args.address, 16)
  else:
    addr = int(args.address)

override = addr

if args.overrideaddress:
  if args.overrideaddress.startswith("0x"):
    override = int(args.overrideaddress, 16)
  else:
    override = int(args.overrideaddress)

print server, port, bus, "0x%02x" % (addr),  "0x%02x" % (override)

delay = 30

chirp = Chirp(bus, addr)
client = graphiteclient.GraphiteClient(server, port, delay)
client.verbose = True

while True:
  client.poke("chirp.%s" + ".%x.cap_sense" % (override), chirp.cap_sense())
  client.poke("chirp.%s" + ".%x.temp"      % (override), chirp.temp())
  client.poke("chirp.%s" + ".%x.light"     % (override), chirp.light())

  sys.stdout.flush()
  time.sleep(delay)
