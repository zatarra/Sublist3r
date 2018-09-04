import json
import requests
import socket
import re

#
#This plugin uses shodan to gather information regarding open ports
#

DEBUG = 1

class SubPlugin():
    def __init__(self, subdomains_list):
        self.regex = r'content="Ports open:(.*?)"'
        self.shodan = "https://www.shodan.io/host/"
        self.subdomains = subdomains_list


    def run(self):
        tmpPorts = {}
        for d in self.subdomains.keys():
          try:
              if not self.subdomains[d]["ip"]:
                try:
                  self.subdomains[d]["ip"] = socket.getbyhostname(d)  
                except:
                  continue
              if self.subdomains[d]["ip"] != "0.0.0.0":
                if self.subdomains[d]["ip"] in tmpPorts:
                    self.subdomains[d]["shodan"] = tmpPorts[self.subdomains[d]["ip"]]
                    continue

                r = requests.get("{}{}".format(self.shodan, self.subdomains[d]["ip"]))
                if r.status_code == 200:
                  text = r.text
                  open_ports = [int(x.strip()) for x in (re.findall(self.regex, text, re.M)[0]).split(",")]
                  tmpPorts[self.subdomains[d]["ip"]] = open_ports
                  self.subdomains[d]["shodan"] = open_ports
          except Exception as ex:
             import traceback
             traceback.print_exc()
             if DEBUG:
               print("An exception occured: {}".format(ex.message))
             

        return self.subdomains
