import struct
import yaml

def count(address):
    return struct.unpack('I',data[address:address+4])[0]

#Get Model Names
data = yaml.safe_load(open('objlist vanilla.yml'))
models = {}
for i in data.values():
    x = i['NeoMoveset']
    if x != 0 and not x in models:
        models[x] = i['ModelName']

data = open('went vanilla.bin','rb').read()
offsets = []
f = open('went test.txt','w')
for i in range(0x46):
    offset = count(4*i)*4
    amount = count(offset)
    if not i in models:
        continue
    elif offset in offsets:
        continue
    elif offset == 0:
        continue
    g = open('went/'+models[i]+'.bin','wb')
    g.write(data[offset:offset+amount*4])
    g.close()
    offsets.append(offset)

f.close()
