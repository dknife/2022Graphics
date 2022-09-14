
import math

def myFunction() :
    print('hahaha')

for i in range(10):
    myFunction()


def 빗변계산(밑변, 높이) :
    # 빗변을 계산하여 반환하자
    빗변 = math.sqrt(밑변**2 + 높이**2)
    return 빗변


result = 빗변계산(3, 4)
print(result)

while True: # 무한 루프
    밑변 = float (input('밑변은 얼마입니까?: '))
    높이 = float (input('높이는 얼마입니까?: '))

    if 밑변 < 0 or 높이 < 0 :
        print('종료합니다.')
        break
    
    빗변 = 빗변계산(밑변, 높이)
    print('이 삼각형의 빗변은 ', 빗변, '입니다.')



