import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
import requests

parser = argparse.ArgumentParser(description='Set up Wordpress OAuth2 server')
parser.add_argument('--clientid', type=str, required=True,
                    help='Client Id')
parser.add_argument('--clientsecret', type=str, required=True,
                    help='Client Secret')
parser.add_argument('--publicurl', type=str, default="http://localhost:8976",
                    help='Publicly accessible URL of server')

args = parser.parse_args()

CLIENT_ID = args.clientid
CLIENT_SECRET = args.clientsecret
PUBLIC_URL = args.publicurl 

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)

        print(path)

        if (path == '/auth'):
            self.handle_auth()
        elif (path == '/callback'):
            self.handle_callback(query['code'][0])
        else:
            self.send_response(404)
            self.end_headers()

    def handle_auth(self):
        # A day may come when I upgrade to Python 3.6, when we foresake 3.5, and can use f-strings, but it is not this day.
        url = "https://public-api.wordpress.com/oauth2/authorize/?client_id="+CLIENT_ID+"&redirect_uri="+PUBLIC_URL+"/callback&response_type=code"
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()
      
    def handle_callback(self, code):
        data = {
            'client_id': CLIENT_ID,
            'redirect_uri': PUBLIC_URL+"/callback",
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
        response = requests.post('https://public-api.wordpress.com/oauth2/token', data = data)
        json = response.json()
        self.send_response(200)
        self.end_headers()

        print('API data')
        print('--------')
        print('Blog ID: '+ json['blog_id'])
        print('Access Token: ' + json['access_token'])
        print('--------')

PORT = 8976
httpd = HTTPServer(('localhost', PORT), Server)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()