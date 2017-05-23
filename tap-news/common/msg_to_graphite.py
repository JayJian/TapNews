#!/user/bin/env python

import argparse
import socket
import time
import yaml
import system_log_client

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

CARBON_SERVER = cfg['graphite_carbon']['carbon_server']
CARBON_PORT = cfg['graphite_carbon']['carbon_port']

def main(args):
    timestamp = int(time.time())
    message = '%s %s %d\n' % (args[0], args[1], timestamp)
    # print 'Message sent to system monitor: Graphite!'
    system_log_client.logger.info("Message sent to system monitor: Graphite!")
    sock = socket.socket()
    sock.connect((CARBON_SERVER,CARBON_PORT))
    sock.sendall(message)
    sock.close()

if __name__ == '__main__':
    main()
