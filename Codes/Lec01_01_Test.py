
# 파이썬 연습 - 이건 코멘트

'''
# 변수를 사용하자
a = 3   # 처음으로 변수에 값이 저장될 때 선언이 알아서 이루어짐
b = 2   # 마찬가지

c = a + b**3 ; # 세미콜론은 있든지 없든지...

print(c) # print는 내장함수


a = '나는 정말 이상한 변수' # 변수에 다른 자료형이 들어가면 새롭게 선언됨
b = '나도 나도'

c = a + b
print(c)

a = 123434323
b = 234233423
c = a * b ** 100
print(c)

################## 프로그램의 흐름 제어 #################

age = int (input('나이를 입력하세요: '))
print(age , '세')

# 만약 18세 미만이면 출입금지를 출력하고
# 18세 이상이면 어떤 음료를 마실 것인지 묻는다

if age < 18 :
    print('출입 금지입니다')
elif age < 21:
    print('신분증을 보여주세요')
else :
    beverage = input('어떤 음료를 주문하시겠습니까? ')
    print('네, 알겠습니다.', beverage, '를 준비하겠습니다.')

### 반복 - for / while

for i in range(1, 10, 2) :
    print(i)

for i in [3, 4, 8, 9, 'hello'] :
    print(i)

'''

from logging.handlers import WatchedFileHandler


presidents = ['이승만', '윤보선', '박정희', '최규하', '전두환', '노태우', '김영삼', '김대중', '노무현', '이명박', '박근혜', '문재인', '윤석열']

print(presidents)

#for president in presidents:
#    print(president)


i = 0
while i<5  :
    print(presidents[i])
    i += 1



    













