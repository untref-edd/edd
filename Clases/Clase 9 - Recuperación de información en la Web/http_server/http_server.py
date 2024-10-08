import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

log_level = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s | %(levelname)8s: %(message)s")

PORT = 80


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        match (self.path):
            case "/":
                self.send_response(200)
                response = {"message": "Recibido"}
            case "/error":
                self.send_response(500)
                response = {"message": "Error interno"}
            case _:
                self.send_response(404)
                response = {"message": "Recurso no encontrado"}

        response = json.dumps(response).encode("utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        logging.info(f"Headers:\n{str(self.headers).strip()}")
        logging.info(f"Recibido:\n{body.decode("utf-8")}")

        match (self.path):
            case "/":
                self.send_response(200)
                response = {"message": "Recibido"}
            case _:
                self.send_response(404)
                response = {"message": "Recurso no encontrado"}

        response = json.dumps(response).encode("utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


    def log_message(self, format, *args):
        logging.info(format % args)


httpd = HTTPServer(("", PORT), RequestHandler)
logging.info(f"Iniciando el servidor HTTP en el puerto {PORT}")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    logging.info("Hasta luego")
except Exception as ex:
    print("")
    logging.error("Error inesperado: %s", ex)
finally:
    httpd.server_close()
