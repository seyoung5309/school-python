import random

print('0 이상 1 미만 실수 값 : ', random.random())
print('2.5 이상 10.0 미만 실수 값 : ', random.uniform(2.5, 10.0))
print('0 이상 10 미만 정수 값 : ', random.randrange(10))
print('1 이상 7 미만, 즈악 값이 2인 정수값 : ', random.randrange(1, 7, 2))
print()
print('리스트에서 1개 값 꺼내오기')
season = ['봄', '여름', '가을', '겨울'];
print('season 리스트 : ', season)
print('random.choice(season)')
print()
list_a = [ '가', '나', '다', '라', '마' ]
print('리스트 순서를 섞는다.')
print('섞기 전 list_a : ', list_a)
random.shuffle(list_a)
print('섞은 후 list_a : ', list_a)
print()
print('리스트에서 중복되지 않게 3개 값 꺼내오기')
sample = ['1번', '2번 ', '3번', '4번', '5번', '6번', '7번', '8번', '9번', '10번']
print('샘플 대상 = ', sample)
print('선택된 값 = ', random.sample(sample, 3))
print('random.sample(sample, 3) : ', random.sample(sample, 3))