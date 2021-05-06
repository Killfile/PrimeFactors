import pika
import time

class QueueWriter:
  def __init__(self,user,password,host,port,exchange, queue, key, verbose):
    self._user = user
    self._password = password
    self._host = host
    self._port = port
    self._exchange = exchange
    self._queue = queue
    self._key = key
    self._verbose = bool(verbose)
    self.connect()

  def connect(self):
    # connect to RabbitMQ
    credentials = pika.PlainCredentials(self._user, self._password )
    while True:
      try:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host,credentials=credentials ))
      except:
        print("Connection error.  Waiting 5 seconds...")
        time.sleep(5)
      break
    
    self.channel = self.connection.channel()

    # create queue if it does not exist
    self.channel.queue_declare(queue=self._queue, auto_delete=False)
    print("using queue: {}".format(self._queue))

    # create exchange if requested
    if len(self._exchange):
      self.channel.exchange_declare(exchange=self._exchange,exchange_type='direct')
      print("declared exchange '{}'".format(self._exchange))
      self.channel.queue_bind(exchange=self._exchange,queue=self._queue,routing_key=self._key)
      print("bound queue {} to exchange {} with key {}".format(self._queue,self._exchange,self._key))
    else:
      print("using default rabbitMQ exchange")
    
  def enqueueMessage(self, i):
    if self._verbose: print("Enqueuing %d with key %s"%(i, self._key))
    while True:
      try:
        self.channel.basic_publish(exchange=self._exchange, routing_key=self._key, body=str(i))
      except:
        print("Encountered an error... trying again")
        time.sleep(5)
      break