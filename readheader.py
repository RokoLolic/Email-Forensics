# Import the email modules we'll need
from email.parser import BytesParser, Parser, FeedParser
from email.policy import default
import re
import requests
import json
import webbrowser

# This fuction reads a string and uses regex to find all Ipv4 and Ipv6 adresses. 
# It returns 2 arrays: one for ipv4 and other for ipv6 adresses

def extractIPs(fileContent):
    ipv4_extract_pattern = "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    ipv4s = re.findall(ipv4_extract_pattern, fileContent)
    ipv6_extract_pattern = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
    ipv6s = re.findall(ipv6_extract_pattern, fileContent)
    return ipv4s, ipv6s

# Change the name of filename for different files. Emails have .eml extension
filename = "spam.eml" 

# Opens a file, reads it and extracts the header
with open(filename, 'rb') as fp:
    headers = BytesParser(policy=default).parse(fp)

# Read basic data from header
print('To: {}'.format(headers['to']))
print('From: {}'.format(headers['from']))
print('Subject: {}'.format(headers['subject']))

# Converts headers from raw bytes into a string
headers_string = str(headers)

# Extracts Ipv4 and Ipv6 adresses from header using extractIPs function
IPV4s, IPV6s= extractIPs(headers_string) 

# initializes array for geagraphical adresses in  format of 
# [[latitude1, longitude1], [latitude2, longitude2] ... ]
foundadresses = []
for i in range(len(IPV6s)): 
    # regex gives an odd array featuring ipv6 adress and a bunch of empty characters 
    # so i am only using first element which is IPv6 adress itself
    ip_address = IPV6s[i][0]
    print(ip_address)
    # where to send request to get geolocation json
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
    # perform get request to recieve geolocation json
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result  = json.loads(result)

    # extracts latitude and longitude from json 
    result_latitude = result['latitude']
    #skips current iteraton of loop if no latitude (private adress)
    if result_latitude == "Not found":
        continue
    result_longitude = result['longitude']
    # skips current iteratin of loop if repeat adress
    if [result_latitude, result_longitude] in foundadresses:
        continue
    # adds [latitude, longitude] array to foundadresses
    foundadresses.append([result_latitude, result_longitude])
    
    # opens a new tab of google maps of adress
    url="http://www.google.com/maps/place/" + str(result_latitude) + "," + str(result_longitude)

    webbrowser.open_new_tab(url)


# Same as IPV6 adresses
for i in range(len(IPV4s)):
    ip_address = IPV4s[i]
    print(ip_address)
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result  = json.loads(result)
    result_latitude = result['latitude']
    if result_latitude == "Not found":
        continue
    result_longitude = result['longitude']
   
    if [result_latitude, result_longitude] in foundadresses:
        continue
    foundadresses.append([result_latitude, result_longitude])
    
    url="http://www.google.com/maps/place/" + str(result_latitude) + "," + str(result_longitude)
    webbrowser.open_new_tab(url)

# checks Spam Confidence Level, higher number means more likely spam
# SCL -1, 0 not spam
if "SCL:" in headers_string:
    #gdje se spominje SCL: u headeru
    location = headers_string.index("SCL:")
    # Sometimes it is formated as "SCL: number" this skips the blank space
    if headers_string[location+4]==" " :
        #If SCL is -1
        if(headers_string[location+5]=="-" ):
            print(f"Nije spam, SCL: -{headers_string[location+6]}")
        else:
            print(f"SCL: {headers_string[location+5]}")
    # Other time it's formated as "SCL:number"
    else:
        #If SCL is -1
        if(headers_string[location+4]=="-" ):
            print(f"Nije spam, SCL: {headers_string[location+5]}")
        else:
            print(f"SCL: {headers_string[location+4]}")