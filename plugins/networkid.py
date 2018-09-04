import json
import requests
import ipwhois
import socket

#
#Simple plugin to get network ids. Be careful when passing large lists as it may get you temporarily blocked.
#To the process more efficient we first add the unique ip addresses to a list and only then we resolve their asn's 
#

class SubPlugin():

    def __init__(self, subdomains_list):
        self.subdomains = subdomains_list


    def run(self):
        ip_list = []

        for d in self.subdomains.keys():
          if not self.subdomains[d]["ip"]:
            try:
              self.subdomains[d]["ip"] = socket.gethostbyname(subdomain)
            except Exception as e:
              self.subdomains[d]["ip"] == "0.0.0.0"
              continue
          if self.subdomains[d]["ip"] not in ip_list and self.subdomains[d]["ip"] != "0.0.0.0":
            # If the IP address is shown as 0.0.0.0 then it could not be resolved.
            ip_list.append(self.subdomains[d]["ip"])           

        #Now go over the list and resolve all the IPs 
        for i in ip_list:
          try:
             ip = ipwhois.IPWhois(i).lookup_whois()
             for d in self.subdomains.keys():
               if self.subdomains[d]["ip"] == d:
                 self.subdomains[d]["network"] = {"description":ip["asn_description"], 
                                           "cidr":ip["asn_cidr"], 
                                           "country":ip["asn_country_code"]}

          except ipwhois.exceptions.IPDefinedError:
            ''' Private IP? '''
            self.subdomains[d]["private"] = True
          except:
            continue
    

        return self.subdomains
