# python 101

## 1. 저장

### 1) 숫자

> 변수 타입 선언이 없어도 자동적으로 설정됨

```python
a = 7
b = 3

print(a)
print(a+b)
print(a-b)
print(a*b)
print(a / b)
print(a // b)
print(a % b)
'''
결과
7
10
4
21
2.3333333333333335
2
1
'''
```

### 2) 글자

> String 타입의 변수로 지정하지 않아도 자동적으로 타입을 결정해줌

#### 글자 합체

```python
hphk = "happy" +" "+ "hacking"
print(hphk)
'''
결과
happy hacking
'''
```

#### 글자 삽입

> f" {} " 은 최신방법
>
> format 형은 구식방법

```python
name = "vvvvvvoin"
age = 25

text = "안녕하세요. 제 이름은 {}입니다. 나이는 {}살 입니다".format(name, age)
print(text)

f_text = f"안녕하세요. 제 이름은 {name}입니다. 나이는 {age}살 입니다"
print(f_text)

'''
결과
안녕하세요. 제 이름은 vvvvvvoin입니다. 나이는 25살 입니다
안녕하세요. 제 이름은 vvvvvvoin입니다. 나이는 25살 입니다
'''
```

#### 글자 자르기

> [a : b]  a부터 시작해서 b만큼
>
> a 값이 음수면 역순으로

```python
text_name = text[:15]
print(text_name)

text_age = text[15:]
print(text_age)

text_split = text.split()
print(text_split)

'''
결과
안녕하세요. 제 이름은 vv
vvvvoin입니다. 나이는 25살 입니다
['안녕하세요.', '제', '이름은', 'vvvvvvoin입 
니다.', '나이는', '25살', '입니다']
'''
```

### 3) 참/거짓

> 주로 주건문에서 사용됩니다

```python
참 = True
거짓 = False

if 참 : 
    print("이것은 참입니다")

if not 거짓 :
    print("이것은 거짓입니다")
    
'''
결과
이것은 참입니다
이것은 거짓입니다
'''
```


## 2. 조건
> `if`문에서 조건이 True가 아니면 elif의 단계적으로 참/거짓을 판별
>
> `print`문에서 부등호로 True/False 판별할 수 있음

```python
dust = 120

print (dust > 150)
print (dust > 100)

if dust > 150:
    print("매우 나쁨")
elif dust > 100:
    print("나쁨")
elif dust >80:
    print("조금 좋음")
else :
    print("좋음")
'''
결과
False
True
나쁨
'''
```


## 3. 반복

```python
menus = ["순남시래기", "양자강", "20층", "버거킹"]

for menu in menus:
    print(menu)
    
for i in range(4):
    print(menus[i])
'''
결과
순남시래기
양자강
20층
버거킹

순남시래기
양자강
20층
버거킹
'''
```

## 명령어

type() : 타입을 보여줌

split(' ') : ' '안의 문자로 list를 분리해줌(()안에 공백시 blank 제거)

range() : 리스트의 시작, 끝 index 지정

sorted() : 작은 크기순으로 정렬시켜줌

X.sort(reverse=True) : X 변수의 리스트를 내림차순으로 정렬시킴

random(range(), x) : range()범위에 임의의 숫자 x개를 뽑음