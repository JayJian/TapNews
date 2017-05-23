import pyjsonrpc
import operations
import os
import sys
import yaml

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

SERVER_HOST = cfg['services']['host']
SERVER_PORT = cfg['services']['rpc_port']

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import msg_to_graphite

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ Test method """
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        return a + b

    """ Get news summaries for a user """
    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        args = ['tap-news.services.rpcRequest','1']
        msg_to_graphite.main(args)
        return operations.getNewsSummariesForUser(user_id, page_num)

    """ Log user news clicks """
    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id):
        args = ['tap-news.services.rpcRequest','1']
        msg_to_graphite.main(args)
        return operations.logNewsClickForUser(user_id, news_id)

# Threading HTTP Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()
