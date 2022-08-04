import pyupbit
import pandas
import datetime
import time

#객체 생성 #로그인
access = 'Ku2ltFhSY6xao3lJbTDf9ne3knIwlVVcjFYiUOFA'
secret = 'xqxXG5bTzMJgVzm8hORQQeqwwQME0yZ9lVqCOMzI'
upbit = pyupbit.Upbit(access, secret)

etc_balance = upbit.get_balance("btc-PCI")

print (etc_balance)