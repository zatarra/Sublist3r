import json
import requests


#
#This plugin checks if the server is an Amazon S3 bucket.
#
DEBUG = 0

class SubPlugin():

    def __init__(self, subdomains_list):
        self.subdomains = subdomains_list


    def run(self):
        for d in self.subdomains.keys():
          print(d)
          try:
              r = requests.get('https://{}'.format(d), verify=False)
              if r.headers["Server"] == "AmazonS3":
                self.subdomains[d]["s3"] = True
              else:
                self.subdomains[d]["s3"] = False
          except Exception as ex:
              if DEBUG:
                  print("{}".format(ex.message))
              continue 

        return self.subdomains
