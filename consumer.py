#!/usr/bin/env python
#
# Example consumer of queue messages
#
# pip3 install -r requirements.txt
#
import argparse
import sys
import os
import pika
import signal
import time
import math
import staticfilewriter
from queuewriter import QueueWriter
from millerrabin import MRPrimeTester
from aks_primality import AKSPrimalityTest
from aprcl_primality import APRCLPrimality


example_usage = '''====EXAMPLE USAGE=====

Connect to remote rabbitmq host
--user=guest --password=guest --host=192.168.1.200

Specify exchange and queue name
--exchange=myexchange --queue=myqueue
'''


def parseArguments():
  ap = argparse.ArgumentParser(description="RabbitMQ producer",
                               epilog=example_usage,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
  ap.add_argument('--user',default="guest",help="username e.g. 'guest'")
  ap.add_argument('--password',default="guest",help="password e.g. 'pass'")
  ap.add_argument('--host',default="localhost",help="rabbitMQ host, defaults to localhost")
  ap.add_argument('--port',type=int,default=5672,help="rabbitMQ port, defaults to 5672")
  ap.add_argument('--exchange',default="",help="name of exchange to use, empty means default")
  ap.add_argument('--outputqueue', default="outputqueue",help="name of the OUTPUT queue for the consumer, defaults to 'outputqueue'")
  ap.add_argument('--inputqueue',default="raw-numbers",help="name of INPUT queue, defaults to 'raw-numbers'")
  ap.add_argument('--key',default="output-key",help="routing key for output")
  ap.add_argument('--test',default="exhaustive",help="test for primeness [exhaustive or fermat]")
  ap.add_argument('--qos',default=1,help="maximum number of primes to prefetch [default is 1]")
  ap.add_argument('--verbose',default=False,help="Verbose mode [defaults to False]")
  args = ap.parse_args()
  return args

args = parseArguments()

def exhaustivePrimeTest(candidateInt: int, verbose:bool = False):
  for i in range(2,int(math.sqrt(candidateInt)+1)):
    if candidateInt % i == 0:
      if verbose: print("%d was not prime."%candidateInt)
      return False
  return True

def aksPrimeTest(candidateInt: int, verbose:bool = False):
  returnValue = AKSPrimalityTest.isPrime(candidateInt)
  if not returnValue and verbose:
    print("%d was not prime."%candidateInt)
  return returnValue

def aprclPrimeTest(candidateInt: int, verbose:bool = False):
  returnValue = APRCLPrimality.isPrime(candidateInt)
  if not returnValue and verbose:
    print("%d was not prime."%candidateInt)
  return returnValue


def fermatPrimeTest(candidateInt: int, verbose:bool = False):
  return MRPrimeTester.isPrime(candidateInt, 1)

def fileWriterIntercept(candidateInt: int, verbose:bool = False):
  fileWriter = staticfilewriter.StaticFileWriter()
  if verbose: print("Attempting to write %d"%candidateInt)
  fileWriter.appendLine(str(candidateInt))
  return False

class GenericConsumer:
  def __init__(self, username, password, host, port, inputqueue, exchange, outputqueue, key, qos, verbose, callback_function):
    self._username = username
    self._password = password
    self._host = host
    self._port = port
    self._queue = inputqueue
    self._exchange = exchange
    self._key = key
    self._callback_function = callback_function
    self._writer = None
    self._qos = qos
    self._verbose = verbose
    if exchange != "":
      self._writer = QueueWriter(username, password, host, port, exchange, outputqueue, key, self._verbose)
    credentials = pika.PlainCredentials(self._username, self._password )
    connection = pika.BlockingConnection(pika.ConnectionParameters(self._host, self._port, '/', credentials ))
    channel = connection.channel()

    channel.basic_qos(prefetch_count=self._qos)

    def generic_callback(channel, method, properties, body):
      candidateString = body.decode('UTF-8')
      if self._verbose: print("Got %s from %s"%(candidateString, self._queue))
      candidateInt = int(candidateString)
      if self._callback_function(candidateInt, self._verbose):
        if self._writer is not None:
          if self._verbose: print("Attempting to enqueue %d consumer..."%candidateInt)
          self._writer.enqueueMessage(candidateInt)
        else:
          print("%d reached the end of the routing sieve."%candidateInt)

      channel.basic_ack(delivery_tag = method.delivery_tag)

    while True:
      try:
        channel.basic_consume(queue=self._queue, on_message_callback=generic_callback)
      except:
        print("Connection error.  Backing off for 5 seconds...")
        time.sleep(5)
      break

    # capture CTRL-C
    def signal_handler(signal,frame):
      print("\nCTRL-C handler, cleaning up rabbitmq connection and quitting")
      connection.close()
      sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("Waiting for messages, CTRL-C to quit...")
    print("")
    channel.start_consuming()

args = parseArguments()

tests = {
  "exhaustive": exhaustivePrimeTest,
  "aks": aksPrimeTest,
  "fermat": fermatPrimeTest,
  "aprcl": aprclPrimeTest,
  "writetofile": fileWriterIntercept
}

GenericConsumer(args.user, args.password, args.host, args.port, args.inputqueue, args.exchange, args.outputqueue, args.key, int(args.qos), bool(args.verbose), tests[args.test])
