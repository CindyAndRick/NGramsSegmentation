import re

def splitText(text):
    return re.findall("[\u4e00-\u9fa5]+", text)

def readText(path, limit = 500):
    count = 0
    res = ""
    print('reading {} data...'.format(limit))
    with open(path, 'r', encoding='utf-8') as f:
        while(True):
            line = f.readline()
            if not line or count > limit:
                break
            count += 1
            if not count % 1000:
                print("{:5}/{}".format(count, limit))
            res += (line.split('\x07')[-1])
        f.close()
    print('read data done')
    return res

            