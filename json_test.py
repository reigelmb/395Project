import json

# Opening JSON file
with open('example.json', 'r') as f:
    json_object = json.load(f)



hell = json_object["Decisions"]["DEC1"]['pointer1'] #pointer to dec2
if (json_object["Decisions"]["DEC2"]['text1'] == json_object['Decisions'][hell]['text1']):
    print("yes")

curr = 'DEC1'
while True:
    print(json_object["Decisions"][curr]['text1'])
    print(json_object["Decisions"][curr]['text2'])

    button = input("Type 1 or 2: ")
    #switch current spot
    if (button == '1'):
        curr = json_object["Decisions"][curr]['pointer1']
    if (button == '2'):
        curr = json_object["Decisions"][curr]['pointer2']
