import json
import pika

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    # send a message
    def sendMessage(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key = self.queue_name,
                                   body = json.dumps(message))
        print "[X] Sent message to %s: %s" % (self.queue_name, message)
        return

    # receive a message
    def getMessage(self):
        #there are three attributes needed, method_frame to check whether receiving the message
        #header_frame is needed, we could leave it null
        #body the message body
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        #check whether receive the message
        if method_frame is not None:
            print "[O] Received message from %s: %s" % (self.queue_name, body)
            #to confirm the server has received the message, if not, the message will still be in the queue
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            print "No message returned"
            return None

    #sleep method, avoid using python sleep, since we need the CloudAMQPClient to be active
    def sleep(self, seconds):
        self.connection.sleep(seconds)
