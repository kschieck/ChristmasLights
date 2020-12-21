from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
import time
from subprocess import Popen
import json
import os
import signal

# TODO change IP address or get it dynamically

server_ip = '192.168.1.236'

current_subprocess = None

class MyServer(SimpleHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        if self.path == '/options':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            json_data = json.dumps([f for f in os.listdir("./data")])
            self.wfile.write(bytes(json_data, encoding="ASCII"))
            return
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # Parse the request body
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len).decode("utf-8")
        body_obj = json.loads(post_body)
        
        command = 'sudo python3 lights_player.py'

        if 'name' in body_obj:
            name_safe = body_obj["name"].replace('"', '')
            command += ' --name="' + name_safe + '"'

        if 'no_sound' in body_obj and body_obj['no_sound']:
            command += ' --no-sound'

        print(command)

        # start the script (kill past instance)
        global current_subprocess
        if current_subprocess != None:
            # Kill the child process
            os.killpg(os.getpgid(current_subprocess.pid), signal.SIGTERM)
        current_subprocess = Popen([command], shell=True, preexec_fn=os.setpgrp)
        self.do_GET()

def run(server_class=HTTPServer, handler_class=MyServer):
    global server_ip
    server_address = (server_ip, 8000)
    httpd = server_class(server_address, handler_class)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % server_address)


if __name__ == '__main__':
    run()