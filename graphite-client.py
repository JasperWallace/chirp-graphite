#!/usr/bin/env python
#
#
#
from __future__ import print_function

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

def check_chirp(arg):
    arg = arg.split(':')
    if len(arg) != 3:
        msg = "%s wrong format" % arg
        raise argparse.ArgumentTypeError(msg)
    bus, addr, name = arg
    out = {}
    try:
        out['bus'] = int(bus)
    except Exception, e:
        raise argparse.ArgumentTypeError("bus should be an int, not %s : %s" % (bus, e))
    try:
        if addr.startswith("0x"):
            addr = int(addr, 16)
        else:
            addr = int(addr)
        out['addr'] = addr
    except:
        raise argparse.ArgumentTypeError("addr should be an int, not %s" % (addr))
    out['name'] = name
    return out

parser.add_argument('chirps', metavar='C', type=check_chirp, nargs='+',
    action='append',
    help='a list of chirps to talk to in the form bus:addr:name, e.g. 1:0x49:tomatoes')

args = parser.parse_args()

if args.server:
  server = args.server

if args.port:
  port = args.port

cargs = args.chirps[0]

print(server, port)

delay = 30

client = graphiteclient.GraphiteClient(server, port, delay)
client.verbose = True

chirps = []
for c in cargs:
    print(c)
    chirps.append({'chirp': Chirp(c['bus'], c['addr']), 'name': c['name']})

while True:
    for c in chirps:
        client.poke("chirp.%s.cap_sense" % (c['name']), c['chirp'].cap_sense())
        client.poke("chirp.%s.temp"      % (c['name']), c['chirp'].temp())
        client.poke("chirp.%s.light"     % (c['name']), c['chirp'].light())

    sys.stdout.flush()
    time.sleep(delay)
