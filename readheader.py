# Import the email modules we'll need
from email.parser import BytesParser, Parser, FeedParser
from email.policy import default
import re
import requests
import json
import webbrowser

def extractIPs(fileContent):
    ipv4_extract_pattern = "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    ipv4s = re.findall(ipv4_extract_pattern, fileContent)
    ipv6_extract_pattern = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
    ipv6s = re.findall(ipv6_extract_pattern, fileContent)
    return ipv4s, ipv6s

filename = "hello from outlook.eml"

# If the e-mail headers are in a file, uncomment these two lines:
with open(filename, 'rb') as fp:
    headers = BytesParser(policy=default).parse(fp)

#  Now the header items can be accessed as a dictionary:
print('To: {}'.format(headers['to']))
print('From: {}'.format(headers['from']))
print('Subject: {}'.format(headers['subject']))

# You can also access the parts of the addresses:
#print('Recipient username: {}'.format(headers['to'].addresses[0].username))
#print('Sender name: {}'.format(headers['from'].addresses[0].display_name))
#print(headers)
headers_string = str(headers)
#print(headers_string)
IPV4s, IPV6s= extractIPs(headers_string) # extract IPv4 and IPv6 adresses
#print(headers_string)

foundadresses = []
# for i in range(len(IPV6s)): 
#     ip_address = IPV6s[i][0]
#     print(ip_address)
#     request_url = 'https://geolocation-db.com/jsonp/' + ip_address
#     response = requests.get(request_url)
#     result = response.content.decode()
#     result = result.split("(")[1].strip(")")
#     result  = json.loads(result)
#     result_latitude = result['latitude']
#     if result_latitude == "Not found":
#         continue
#     result_longitude = result['longitude']

#     if [result_latitude, result_longitude] in foundadresses:
#         continue
#     foundadresses.append([result_latitude, result_longitude])
    
#     url="http://www.google.com/maps/place/" + str(result_latitude) + "," + str(result_longitude)

#     webbrowser.open_new_tab(url)


# for i in range(len(IPV4s)):
#     ip_address = IPV4s[i]
#     print(ip_address)
#     request_url = 'https://geolocation-db.com/jsonp/' + ip_address
#     response = requests.get(request_url)
#     result = response.content.decode()
#     result = result.split("(")[1].strip(")")
#     result  = json.loads(result)
#     result_latitude = result['latitude']
#     if result_latitude == "Not found":
#         continue
#     result_longitude = result['longitude']
   
#     if [result_latitude, result_longitude] in foundadresses:
#         continue
#     foundadresses.append([result_latitude, result_longitude])
    
#     url="http://www.google.com/maps/place/" + str(result_latitude) + "," + str(result_longitude)
#     webbrowser.open_new_tab(url)

#print(foundadresses)

if "SCL:" in headers_string:
    location = headers_string.index("SCL:")
    #print(headers_string[location])
    if headers_string[location+4]==" " :
        if(headers_string[location+5]=="-" ):
            print(f"Nije spam, SCL: -{headers_string[location+6]}")
        else:
            print(f"SCL: {headers_string[location+5]}")
    else:
        if(headers_string[location+4]=="-" ):
            print(f"Nije spam, SCL: {headers_string[location+5]}")
        else:
            print(f"SCL: {headers_string[location+4]}")