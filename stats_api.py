import argparse
import requests

parser = argparse.ArgumentParser(description='Make a request to the stats API')
parser.add_argument('--blogid', type=str, required=True,
                    help='Blog Id')
parser.add_argument('--accesstoken', type=str, required=True,
                    help='Access Token')

args = parser.parse_args()

BLOG_ID = args.blogid
ACCESS_TOKEN = args.accesstoken
UNITS = 'day' # or 'week' or 'month' or 'year'
QUANTITY = 365

response = requests.get(
  'https://public-api.wordpress.com/rest/v1.1/sites/' + BLOG_ID + '/stats/visits?quantity=' + str(QUANTITY) + '&unit=' + UNITS,
  headers = {
    'Authorization': 'Bearer ' + ACCESS_TOKEN
  }
)
print(response.json())
