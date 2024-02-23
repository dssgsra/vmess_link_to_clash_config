import base64
import sys
import yaml

vmessLink = sys.argv[1]
# print(vmessLink[8:])
decodeVmessLink = base64.b64decode(vmessLink[8:])
decodeVmessLink = decodeVmessLink.decode('utf-8')
decodeVmessLink = eval(decodeVmessLink)
# print(decodeVmessLink,type(decodeVmessLink))


with open("template.yaml", encoding="utf-8") as file:
    file_data = file.read()

yamlObject = yaml.load(file_data, yaml.FullLoader)
print("before----------------------------------------")
print(yamlObject["proxies"])
print(yamlObject["proxy-groups"])

proxies = yamlObject["proxies"][0]
proxies["name"] = decodeVmessLink["ps"]
proxies["type"] = "vmess"
proxies["server"] = decodeVmessLink["add"]
proxies["port"] = int(decodeVmessLink["port"])
proxies["uuid"] = decodeVmessLink["id"]
proxies["alterId"] = int(decodeVmessLink["aid"])
proxies["cipher"] = decodeVmessLink["scy"]
proxies["tls"] = True
proxies["network"] = decodeVmessLink["net"]
proxies["h2-opts"] = {}
proxies["h2-opts"]["path"] = decodeVmessLink["path"]
proxies["h2-opts"]["host"] = []
proxies["h2-opts"]["host"].append(decodeVmessLink["host"])

yamlObject["proxies"][0] = proxies
proxy_groups = yamlObject["proxy-groups"][0]
proxy_groups["proxies"][0] = proxies["name"]
yamlObject["proxy-groups"][0] = proxy_groups
print("after----------------------------------------")
print(yamlObject["proxies"])
print(yamlObject["proxy-groups"])

with open("from_vmess.yaml", "w", encoding="utf-8") as file:
    yaml.dump(yamlObject, file, encoding="utf-8")
print("Success!")
