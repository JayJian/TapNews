from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://lpxgjkmt:xvCbuMX-h7G6BGehoF_A3WWaLslUNp8g@donkey.rmq.cloudamqp.com/lpxgjkmt"
TEST_QUEUE_NAME = "test"

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)
    sentMsg = {'test': 'demo'}
    client.sendMessage(sentMsg)
    client.sleep(10)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print "Test is passed!"

if __name__ =="__main__":
    test_basic()
