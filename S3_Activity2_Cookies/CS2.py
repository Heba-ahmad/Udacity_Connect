#!/usr/bin/env python3
#
# Udacian activity to practice get and post http
#

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from Activity2 import Dateofbirth
from http import cookies
from html import escape as html_escape
memory = []
form = '''<!DOCTYPE html>
  <title>Date Of Birth Activity</title>
    <p>
  {}
    </p>
  <form method="POST">
    <form method="POST">
    <label>When were you born?
    <input type="date" name="user_date">
    </label>
    <br>
    <button type="submit">Tell me!</button>
  </form>
'''

class DateofbirthHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        data = self.rfile.read(length).decode()
        name = parse_qs(data)["user_date"][0]
        users_input= Dateofbirth(name)
        memory.append(users_input.print_dob())
        # Create cookie.
        c = cookies.SimpleCookie()
        c['user_date'] = name
        c['user_date']['domain'] = 'localhost'
        c['user_date']['max-age'] = 70
        c["user_date"]["httponly"] = True
        self.send_response(303)
        self.send_header('Location', '/')
        self.send_header('Set-Cookie', c['user_date'].OutputString())
        self.end_headers()
    def do_GET(self):
        message= "Hey there!"
        if 'cookie' in self.headers:
            try:
                c = cookies.SimpleCookie(self.headers['cookie'])
                name = c['user_date'].value
                message = "Hey there, you were born in " + html_escape(name)
            except (KeyError, cookies.CookieError) as e:
                message = "I'm not sure! tell me when were you born again?"
                print(e)
        elif "user_date" == "":
            message = "I'm not sure! tell me when were you born again?"
            print(message)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf=8')
        self.end_headers()
        mesg= form.format(message)
        self.wfile.write(mesg.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, DateofbirthHandler)
    httpd.serve_forever()
