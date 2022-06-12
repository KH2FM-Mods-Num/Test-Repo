import struct
import yaml
import os

def count(address):
    return struct.unpack('I',data[address:address+4])[0]

#Get Model Names
data = yaml.safe_load(open('objlist vanilla.yml'))
models = {}
for i in data.values():
    x = i['NeoMoveset']
    if x != 0 and not x in models:
        models[x] = i['ModelName']

sameoffsets = [[17, 18, 50], #Remove WI Donald
               [25, 26, 52], #Remove WI Goofy
               
               [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 53, 54, 57, 58, 61, 66], #P_EX100
               [11, 12, 13, 14, 15, 16, 67], #P_EX100_NM
               [17, 18], #P_EX020
               [25, 26], #P_EX030
               [35, 64, 65], #P_EH000
               [37, 38, 39, 40, 41, 42, 68], #P_EX100_TR
               [43, 44, 45, 46, 47, 48, 69], #P_EX100_WI
               ]
               
               

length = 0x118
wentpoint = bytearray()
wentsets  = bytearray()
for i in range(0x46):
    if i in models:
        name = models[i]
        if os.path.isfile('went/'+name+'.bin'):
            print('FOUND FILE: '+name)
            data = open('went/'+name+'.bin','rb').read()
            wentsets += data
            wentpoint += struct.pack('I',int(length/4))
            length += len(data)
            continue
    sameoffset = False
    for j in sameoffsets:
        if i in j:
            name = models[j[0]]
            print('SAME OFFSET: '+models[i]+' WITH '+name)
            wentpoint += wentpoint[4*j[0]:4*j[0]+4]
            sameoffset = True
            break
    if not sameoffset:
        print('NOT FOUND',str(i))
        wentpoint += bytearray(4)
    
#Sanity checks
if len(wentpoint) + len(wentsets) > 0xEF4:
    print('OFFSET ISSUES DETECTED!')
    raise Exception()
f = open('went.bin','wb')
f.write(wentpoint)
f.write(wentsets)
freebytes = 0xEF4 - len(wentpoint) - len(wentsets)
print(freebytes,'FREE BYTES AVAILABLE')
f.write(bytearray(freebytes))
f.close()
