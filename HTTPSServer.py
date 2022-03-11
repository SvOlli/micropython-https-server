# written by SvOlli as public domain software
# do what you want to, I don't care about any license
# but I'd apprechiate a short "thank you" mail to:
# svolli.svolli.de
# (lame scraper protection: replace first '.' with '@')
# also remember: provided "as is", no warrenties at all

import usocket as socket
import gc
import ussl

class HTTPSServer:
    def __init__(self):
        self.debug = 0
        self.reqHeader = {}
        self.request = ""
        self.htmlHeader = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
 "http://www.w3.org/TR/html4/loose.dtd">
<html lang='en'>
<head>
<title>Micropython HTTPS</title>
<meta http-equiv="content-type" content="Mime-Type; charset=utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
"""
        self.htmlFooter = """
</body>
</html>
"""
        self.cert = ""
        with open('example.crt','r') as f:
            self.cert += f.read()
        self.key = ""
        with open('example.key','r') as f:
            self.key += f.read()

    def getHeader(self,key):
        if key in self.reqHeader:
            return self.reqHeader[key]
        else:
            return None

    def genHTML(self,auth=False):
        html = self.htmlHeader
        html += '<table border="1">\n<tr>\n<th colspan="2">%s</th>\n</tr>\n' % (self.request)
        for key in self.reqHeader:
            html += '<tr>\n<td>%s</td><td>%s</td>\n</tr>\n' % (key, self.reqHeader[key])
        html += '<tr><th colspan="2">'
        if auth:
            html += 'session authenticated'
        else:
            html += '<a href="/auth">click here and authenticate with root/root</a>'
        html += '</th></tr>\n</table>\n'
        html += self.htmlFooter
        return html

    def sendHeader(self, conn, code, conttype='text/html'):
        if code == 200:
            conn.write('HTTP/1.1 200 OK\r\n')
        elif code == 401:
            conn.write('HTTP/1.1 401 Unauthorized\r\n')
            conn.write('WWW-Authenticate: Basic realm="Secret"\r\n')
        elif code == 404:
            conn.write('HTTP/1.1 404 Not Found\r\n')
        elif code == 405:
            conn.write('HTTP/1.1 405 Method Not Allowed\r\n')
        else:
            conn.write('HTTP/1.1 500 Internal Error\r\n')
        conn.write('Content-Type: %s\r\n' % (conttype))
        conn.write('Connection: close\r\n\r\n')

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 443))
        sock.listen(3)
        gc.collect()
        mem_threshold = gc.mem_free() - 20480
        if self.debug:
            print("memory threshold for garbage collection: %d" % (mem_threshold))

        print('listening')
        while True:
            try:
                if self.debug:
                    print("free:", gc.mem_free())
                if gc.mem_free() < mem_threshold:
                    gc.collect()
                # this call is blocking
                rawconn, addr = sock.accept()
                conn = ussl.wrap_socket(rawconn, key=self.key, cert=self.cert, server_side=True)
                conn.setblocking(False)
                if self.debug:
                    print('Received HTTPS GET connection request from %s' % str(addr))
                request = conn.read(2048)
                # remove "b'"-wrapper and convert to list of strings
                request = str(request)[2:-1].split('\\r\\n')
                self.reqHeader = {}
                self.request = request[0]
                # prepare data for self.getHeader(key)
                for r in request:
                    sep = r.find(': ')
                    if sep > 0:
                        self.reqHeader[r[:sep]] = r[sep+2:]
                if self.debug:
                    print(request)
                # error message for POST and other requests
                if self.request.find('GET ') != 0:
                    self.sendHeader(conn, 405)
                    conn.write(self.genHTML())
                # serve a favicon if available
                if self.request.find(' /favicon.ico ') > 0:
                    self.sendHeader(conn, 200, 'image/x-icon')
                    try:
                        with open('favicon.ico','r') as f:
                            conn.write(f.read())
                    except OSError as e:
                        pass
                # page "/auth" is an example for authentication
                elif request[0].find(' /auth') > 0:
                    auth = False
                    # generate password with 'echo -n user:passwd | base64'
                    if self.getHeader('Authorization') == 'Basic cm9vdDpyb290':
                        auth = True
                    if auth:
                        self.sendHeader(conn, 200)
                    else:
                        self.sendHeader(conn, 401)
                    conn.write(self.genHTML(auth = auth))
                else:
                    self.sendHeader(conn, 200)
                    conn.write(self.genHTML())
                conn.close()
            except OSError as e:
                if self.debug:
                    print('OSError, connection closed')
                    print(e)
                rawconn.close()
