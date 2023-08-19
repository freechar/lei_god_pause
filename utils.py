import hashlib 
import base64
from cryptography.fernet import Fernet
your_string = "1145141919810"

# 将字符串转换为字节串并进行 SHA-256 哈希
hash_object = hashlib.sha256(your_string.encode('utf-8'))
hash_bytes = hash_object.digest()

# 对字节串进行 Base64 编码
key = base64.urlsafe_b64encode(hash_bytes)
# 填充到 32 字节长度
while len(key) < 32:
    key += b'a'
    
cipher_suite = Fernet(key)

def passwdDecrypt(password):
    return cipher_suite.decrypt(password).decode('utf-8')

def passwdEncrypt(password):
    return cipher_suite.encrypt(password.encode('utf-8'))


def genearteMD5(password):
    '''
    创建md5对象
    '''
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
    hl.update(password.encode(encoding='utf-8'))
    password = hl.hexdigest()
    return password