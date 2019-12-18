'''
문제 3.
숫자를 입력 받아 짝수/홀수를 구분하는 코드를 작성해주세요 :)
'''

number = int(input('숫자를 입력하세요: '))
# 아래에 코드를 작성해 주세요.

#python에서 fi문의 조건의
# 1 은 True를 의미한다
# 0 은 False를 의미한다
if (number%2 == 1) :
    print(f"{number}는 홀수입니다")
else :
    print(f"{number}는 짝수입니다")