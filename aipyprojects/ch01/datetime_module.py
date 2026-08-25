from datetime import datetime

today = datetime.now()
print('현재 날짜, 시각 데이터: ', today)
print('today = datetime.now() : ', today)
print('연, 월, 일 : ', today.year, today.month, today.day)
print('시, 분, 초 : ', today.hour, today.minute, today.second)
print('요일 : ', today.weekday())
dday = datetime(2027, 1, 1, 0, 0, 0)
print('지정한 d-day : ', dday)
print('지나온 시간 (today - dday) : ', today - dday)