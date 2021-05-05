#!/usr/bin/env python
#
# Example producer of queue message
#
# pip3 install -r requirements.txt
#
import argparse
import sys
import os
import queuewriter
from palendromicoddnumber import PalendromeicOddNumber



example_usage = '''====EXAMPLE USAGE=====

Connect to remote rabbitmq host
--user=guest --password=guest --host=192.168.1.200

Specify exchange, automatically sets routing-key to blank
--exchange=myexchange
'''



def parseArguments():
  ap = argparse.ArgumentParser(description="RabbitMQ producer",
                               epilog=example_usage,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
  ap.add_argument('--user',default="guest",help="username e.g. 'guest'")
  ap.add_argument('--password',default="guest",help="password e.g. 'pass'")
  ap.add_argument('--host',default="amqp://guest:guest@rabbitmq/",help="rabbitMQ host, defaults to localhost")
  ap.add_argument('--port',type=int,default=5672,help="rabbitMQ port, defaults to 5672")
  ap.add_argument('--exchange',default="",help="name of exchange to use, empty means default")
  ap.add_argument('--queue',default="testqueue",help="name of default queue, defaults to 'testqueue'")
  ap.add_argument('--key',default="testqueue",help="routing key, defaults to 'testqueue'")
  ap.add_argument('--maxValue',default=99999999999,help="maximum number to consider")
  ap.add_argument('--minValue',default=1,help="minimum number to consider")
  ap.add_argument('--verbose',default=False,help="Verbose mode [default is false]")
  args = ap.parse_args()
  return args

args = parseArguments()
writer = queuewriter.QueueWriter(args.user, args.password, args.host, args.port, args.exchange, args.queue, args.key, bool(args.verbose))

def write(producer):
     # publish message
    startValue = int(args.minValue)
    if startValue % 2 == 0:
      startValue += 1 

    maxValue = int(args.maxValue)

    palendrome = PalendromeicOddNumber("3","","")

    print("Incrementing")
    length = palendrome._length
    while(palendrome.odd_increment() <= startValue):
      if(len(palendrome.toString()) > length):
        print("Still incrementing at %d"%palendrome.toInt())
        length = len(palendrome.toString())
    

    print("***Starting prime candidate production at %d and going to %d"%(palendrome.toInt(), maxValue))
    while palendrome.odd_increment() < maxValue:
      if(palendrome._length % 2 != 0 and palendrome.toString()[0] != "5"):
        producer.enqueueMessage(palendrome.toInt())

    # close connection
    producer.connection.close()
    sys.exit(0)

write(writer)
# connect to RabbitMQ
