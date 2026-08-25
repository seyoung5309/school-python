import sys

print("실행 파일명: ", sys.argv[0])
for i, arg in enumerate(sys.argv):
    print(f"인자 {i}: {arg}")
sys.exit()
for i in range(1, 100000000000000000000000000000):
    print("exit() 함수로 인해 실행되지 않음")