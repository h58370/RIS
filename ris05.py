import pyupbit
import pandas
import datetime
import time

# RSI계산
def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")

#변수 설정
op_mode = False
hold = False
low = False
high = False
price = pyupbit.get_current_price("KRW-etc")

#객체 생성 #로그인
f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()
upbit = pyupbit.Upbit(access, secret)

#매수가 조회
etc_balance = upbit.get_balance("KRW-etc")

# RSI갱신
while True:
    data = pyupbit.get_ohlcv(ticker="KRW-etc", interval="minute5")
    now_rsi = rsi(data, 14).iloc[-1]
    op_mode = True

#매초 조건 확인후 매수 시도 28이하 하락 후 rsi 30이상 회복
    if op_mode is True and now_rsi <= 28:  # rsi 28 하락
        low = True
    if op_mode is True and hold is False and low is True and now_rsi <= 30: #rsi 30회복
        #매수
        krw_balance = upbit.get_balance("KRW")
        upbit.buy_market_order("KRW-etc", krw_balance * 0.995)
        hold = True
        low = False

          #매도 시도 rsi 70이상 상승 후 68이하로 하락
    if op_mode is True and hold is True and now_rsi >=65: # rsi 65이상 상승
        high = True
    if op_mode is True and hold is True and high is True and now_rsi <=63: #rsi 63이하 하락 매도
        etc_balance = upbit.get_balance("KRW-etc")
        upbit.sell_market_order("KRW-etc", etc_balance)
        hold = False
        high = False

            # rsi 70이상 진입 매도
    if op_mode is True and hold is True and now_rsi >=70:   #70이상 매도 
        etc_balance = upbit.get_balance("KRW-etc")
        upbit.sell_market_order("KRW-etc", etc_balance)
        hold = False
    
         #스탑로스 (2%)
    if op_mode is True and  hold is True and price <= etc_balance*0.9800:       #스탑로스 2
        if op_mode is True and hold is True:
            etc_balance = upbit.get_balance("KRW-etc")
            upbit.sell_market_order("KRW-etc", etc_balance)
            hold = False

    now = datetime.datetime.now()
    stoploss = etc_balance*0.9800
 # 상태 출력
    print(f"현재시간: {now} rsi: {now_rsi} 저점 {low} 고점 {high} 현재가 {price} 보유상태 {hold} 동작상태 {op_mode} 매수가 {etc_balance} 스탑로스 {stoploss}")
    
    time.sleep(1)