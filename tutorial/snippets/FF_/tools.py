#intToIp4 = lambda x: '.'.join([str(x/(256**i)%256) for i in range(3,-1,-1)])
def intToIp4(num: int) -> str:
    '''
    param: ip formate in DB
    return: ip4 
    '''
    s = []

    for i in range(4):
        s.append(str(int(num %256)))
        num /= 256

    return '.'.join(s[::-1])

#ip4ToInt = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])
def ip4ToInt(ip4: str) -> int:
    '''
    param: ip formate in ip4
    return: ip_int
    '''
    ip_int = 0
    
    for j, i in enumerate(ip4.split('.')[::-1]):
        #print(f'i: {i}, j: {j}')
        ip_int += 256**j*int(i)

    #for i, j in zip((ip4.split('.')[::-1]), [0, 1, 2, 3]):
    #    ip_int += 256**j*int(i)
    
    return ip_int

import hashlib
def md5(param : bytes, password: bytes) -> str:
    '''
    param: param for md, 4.0: b'f4a30481422765de945833d10352ea18'
    return: password in DB
    '''
    m = hashlib.md5()
    m.update(password)
    sr = m.hexdigest()

    # for i in range(3):
    # sr= hashlib.md5(sr.encode()).hexdigest()

    rx = hashlib.md5(sr.encode()+param).hexdigest()

    return rx

if __name__ == '__main__':
    r = md5(b'login_salt', b'1234qwer')
    print(r)