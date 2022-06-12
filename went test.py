import struct
import yaml

def count(address):
    return struct.unpack('I',data[address:address+4])[0]

def note(string):
    string = '0x'+hex(string)[2:].upper().zfill(3)
    return string

#Get Model Names
data = yaml.safe_load(open('objlist vanilla.yml'))
model = []
models = {}
for i in data.values():
    x = i['NeoMoveset']
    if x != 0:
        model.append(i['ObjectId'])
        if x in models:
            models[x].append([i['ObjectId'],i['ModelName']])
        else:
            models[x] = [[i['ObjectId'],i['ModelName']]]
model.sort()

data = open('went vanilla.bin','rb').read()
offsets = []
f = open('went test.txt','w')
for i in range(0x46):
    offset = count(4*i)*4
    amount = count(offset)
    if not i in models:
        models[i] = ''
    print(note(i),note(offset),amount,models[i])
    if offset in offsets:
        continue
    offsets.append(offset)

f.close()
