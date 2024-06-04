from haralyzer import HarParser
import json 
from pwn import write
import re

with open("www.tradingview.com.har", "r") as har_file:
    har_data = json.load(har_file)
    # for item in har_data:
    #     print(item)
    
        

# Instantiate the HarParser class with the dictionary representation
har_parser = HarParser(har_data)


entries = har_parser.har_data

# print(entries.keys())

print(len(entries['entries']))
file_no = 1
for entry in entries['entries']:
    
    # print(i.keys())
    try:
        if "profit" in entry['response']['content']['text'].lower():
            # print(entry['request'])
            write(f'request-{file_no}', entry['request'])
            write(f'response-{file_no}', entry['response']['content']['text'])
            print(entry['request'])
            
            # input()
        file_no += 1
    except:
        pass

#index = re.findall('rofit',entries)

# print(har_parser.har_data)

# write('stuff', str(har_parser.har_data))

# print(entries.keys())
# print(entries['entries'][0])
# for entry in entries['entries']:
#     if "Volty" in entry:
#         print(entry)
#         input()

#print(index)
# print(index)
# print(entries)