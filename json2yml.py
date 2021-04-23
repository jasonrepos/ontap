#!/usr/bin/python3.8
import os, sys, json, re
from ruamel.yaml import YAML

def tr(s):
    #s = re.sub(r"(\"\\\"|\\\"\")", r'"', s) # remove the "\" from "\"{{ lookup and at the end 'win_ansible_user']) }}\""
    s = re.sub(r"\'\'", r"'" , s) # remove the double single quotes from ''hashi_vault''
    s = re.sub(r"(\'\"|\"\')", r'"' , s) # remove '" or "' from the begining and end of ansible_password section
    s = re.sub(r"\'(\d*)\'", r"\1" , s) # remove the single quotes from '0:' and '1:'
    return s

yaml = YAML(typ='safe')
yaml.default_flow_style = False
for root, dirs, files in os.walk("./"):
    for file in files:
        if file.endswith(".json"):
            dir = root.split(os.path.sep)[-1]
            if dir != "terraform":
                with open(root + '/' + file, 'r') as stream:
                    try:
                        filename = os.path.splitext(file)[0]
                        with open(root + '/' + filename + '.yml', 'w') as outfile:
                            #yaml.dump(json.load(stream), outfile)
                            yaml.encoding = None
                            yaml.dump(yaml.load(stream), outfile, transform=tr)
                            print('Yaml file created: ' + root + '/' + filename + '.yml')
                            os.remove(root + '/' + file)
                    except:
                        print("There is an issue...")
