import os
import logging
import time
import datetime
import re

import json
import socketserver
import threading

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    """
    Class that handle a single threaded connection
    """

    def parse_input(self, input):
        regexp = re.compile("^\[(\d{2}\/\d{2}\/\d{4}\s\d{2}:\d{2})\]\s(.*)$")
        res = regexp.match(input)
        if res is not None:
            dt = datetime.datetime.strptime(res.group(1), '%d/%m/%Y %I:%M')
            epoch = time.mktime(dt.timetuple())
            return {"timestamp": str(int(epoch)), "message": res.group(2)}
        else:
            # input format is wrong
            return {"error": "format error", "message": "Wrong format, expected: [DD/MM/YYYY HH:MM] MESSAGE BODY"}


    def handle(self):
        try:
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger()
            data = self.request[0].strip()
            logger.info("Handling request from %s", self.client_address)
            sck = self.request[1]
            sck.sendto(json.dumps(self.parse_input(data)), self.client_address)
        finally:
            # close connection
            sck.sendto("", self.client_address)


class Server(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    address = os.environ.get("LISTEN_ADDRESS", "0.0.0.0")
    port = os.environ.get("LISTEN_PORT", 1234)
    server = Server((address, port), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    try:
        server_thread.start()
        logger.info("Server started at %s port %s" % (address, str(port)))
        while True:
            logger.debug("Waiting for connection")
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        logger.debug("\nServer interrupted ... shutting down")
        server.shutdown()
        server.server_close()
        exit()
