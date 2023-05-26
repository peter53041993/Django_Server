import hmac, base64, struct, hashlib, time, pyotp, qrcode
'''
算法參考: https://stackoverflow.com/questions/8529265/google-authenticator-implementation-in-python
'''
def generateSecretKey():
    return pyotp.random_base32()

def generateQRcode(secret_key, user, app_name):
    outh = pyotp.totp.TOTP(secret_key).provisioning_uri(name=user, issuer_name=app_name)
    img = qrcode.make(outh)
    img.save(f'{app_name}_{user}.png')


def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)

if __name__ == '__main__':
    # print(get_totp_token('EBCJEVZGH4QHJ47JSSGUCXOVTUHTAZL3'))
    # print(pyotp.TOTP('EBCJEVZGH4QHJ47JSSGUCXOVTUHTAZL3').now())
    # print(pyotp.TOTP('EBCJEVZGH4QHJ47JSSGUCXOVTUHTAZL3', interval=30).now())

    key = generateSecretKey()
    print(key)
    outh = pyotp.totp.TOTP(key).provisioning_uri(name='alice@google.com', issuer_name='Secure App')
    print(outh)
    img = qrcode.make(outh)
    # img.save('qrcode_1.png')
    print(img)
    
