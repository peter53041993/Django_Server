from MySQLdb import connections
from superdatagenerator import Super2000Data
import pandas as pd
import cx_Oracle
import super_betcontent
from tools import intToIp4, ip4ToInt, md5

ip4 = '61.220.138.45'
ipint = 2130706433

print(ip4ToInt(ip4))
print(intToIp4(ipint))

Super2000Data().saleSwitch(0, 'N')




