from website import create_app #ist die def aus __init__
#pip install flask-login, pip isntall flask-sqlalchemy
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import sys

import logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

app = create_app()



if __name__ == "__main__":
    host = "0.0.0.0"
    port = 80
    http_server = HTTPServer(WSGIContainer(app))
    http_server.debug=True
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port))
    http_server.listen(port)
    IOLoop.instance().start()

# if __name__ =="__main__":
#     http_server = "192.168.2.220"
#     app.run(host=http_server, port=80, debug=True)