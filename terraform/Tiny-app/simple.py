#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import datetime

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # Create response with timestamp and client IP
            timestamp = datetime.datetime.utcnow().isoformat() + "Z"
            ip = self.client_address[0]
            response = {
                "timestamp": timestamp,
                "ip": ip
            }
            response_bytes = json.dumps(response).encode('utf-8')
            # Send 200 OK response with headers
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)
        else:
            # Handle unknown paths
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    print("Starting SimpleTimeService on port 8080")
    server_address = ('', 8080)
    with HTTPServer(server_address, MyHandler) as httpd:
        httpd.serve_forever()
