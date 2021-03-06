##!/usr/bin/env python
# Simple HTTP Server With Upload.

import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re
import tensorflow as tf
import cv2
import eval_model as em
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

img_dim = 50
class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):    
    # Simple HTTP request handler with POST commands.

    def do_POST(self):
        """Serve a POST request."""
        y_ = [[0.0, 0.0]]
        y_, r, info = self.deal_post_data()
        print y_, r, info, "by: ", self.client_address
        f = StringIO()

        if r:
            res = ""
            if y_[0][0] >= y_[0][1]:
                res = "Nao foi detectada mancha maligna."
            else:
                res = "Procure um especialista."
            f.write("Sucesso! Resultado: "+res)
        else:
            f.write("Failed")

        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def deal_post_data(self):
        print self.headers
        boundary = self.headers.plisttext.split("=")[1]
        #print 'Boundary %s' %boundary
        remainbytes = int(self.headers['content-length'])
        #print "Remain Bytes %s" %remainbytes
        # 1
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return ([[0.0,0.0]], False, "Content NOT begin with boundary")
        # 2
        line = self.rfile.readline()
        remainbytes -= len(line)
        #fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        fn = re.findall(r'IMG_.*\.jpg',line)
        if not fn:
            return ([[0.0,0.0]], False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        # 3, 4
        while line.strip():
            line = self.rfile.readline()
            remainbytes -= len(line)
        #line = self.rfile.readline()
        #remainbytes -= len(line)
        #
        try:
            out = open(fn, 'wb')
        except IOError:
            return ([[0.0,0.0]], False, "Can't create file to write, do you have permission to write?")

        #if line.strip():
        #    preline = line
        #else:
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                img = cv2.imread(fn,0)
                img = cv2.resize(img,(img_dim,img_dim))
                img = img/255.0
                t_x = []
                t_x.append(img)
                y_ = em.eval(t_x)
                return (y_, True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return ([[0.0,0.0]], False, "Unexpect Ends of data.")

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

def test(HandlerClass = SimpleHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)

if __name__ == '__main__':
    test()

