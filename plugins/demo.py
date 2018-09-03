import json
import requests




class SubPlugin():

    def __init__(self, subdomains_list):
        self.subdomains = subdomains_list


    def run(self):
        for d in self.subdomains.keys():
          if  len(self.subdomains[d]["ports"]) > 0:
              # Let's fingerprint ports using http requests
              for p in self.subdomains[d]["ports"]:
                  try:
                    if "responses" not in self.subdomains[d]:
                        self.subdomains[d]["responses"] = {}
                    self.subdomains[d]["responses"][p] = requests.get("http://{}".format(self.subdomains[d]["ip"])).text
                  except Exception as ex:
                    print("ERROR {}".format(ex.message))
                    pass

        return self.subdomains
