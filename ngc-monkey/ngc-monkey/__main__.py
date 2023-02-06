import logging

from . import server


logging.basicConfig(level="INFO")
server.app.run(port=5000, host='0.0.0.0', debug=True)
