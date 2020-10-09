- 데이터를 조회하는 3가지 방법
  - 셀렉션 - 행 단위로 조회하는 셀렉션
  - 프로젝션 -  열 단위로 조회하는 프로젝션
  - 조인 - 두 개 이상의 데이틀을 사용하여 조회하는 조인



### SELECT, FROM

#### 기본형

```sql
SELECT [조회할 열1 이름], [조회할 열2 이름], ... [조회할 열N 이름]
FROM [조회할 테이블 이름];
```

#### DISTNCT 해당 열의 중복 데이터를삭제

```SQL
SELECT DISTINCT DEPTNO FROM EMP;
```

>  2개 이상 셀렉션하는 행에서 한 열이 중복이더라도 해당 행의 다른 열이 중복이 아닌 경우 출력된다

#### 열과 연산식

```SQL
SELECT ENAME, SAL, SAL*12+COMM, COMM
FROM EMP;
```

- 테이블의 칼럼을 이용하여 연산식을 이용하여 새로운 칼럼을 만들어 출력할 수 있다
- 하지만 테이블의 컬럼명이 "SAL*12+COM"으로 나타나기에 별칭을 사용해줄 수 있다
- 명칭은 4가지 방식이 존재
  - SAL*12+COM ANNSAL
  - SAL*12+COM "ANNSAL"
  - SAL*12+COM AS ANNSAL (이 방식을 권장)
  - SAL*12+COM AS "ANNSAL"

### ORDER BY

- 기본식
```sql
SELECT [조회할 열1 이름], [조회할 열2 이름], ... [조회할 열N 이름]
FROM [조회할 테이블 이름]
ORDER BY [정렬하려는 열 이름][정렬 옵션];
```
- 정렬옵션 = ASC(내림차순, DEFAULT), DESC(내림차순)
#### 각 열에 내림차순 오름차순 동시 사용하기
```sql
SELECT *
FROM EMP
ORDER BY DEPTNO ASC, SAL DESC;
```
- ORDEY BY 절은 일반적으로 사용하지 않는 것을 권장한다.
- 데이터를 특정 기준에 맞출때에 소모되는 자원이 있기 때문이다.

### WHERE
- 기본식
```sql
SELECT [조회할 열1 이름], [조회할 열2 이름], ... [조회할 열N 이름]
FROM [조회할 테이블 이름]
WHERE [조회할 행을 선별하기 위한 조건식];
```
#### AND, OR
- WHERE절에서는 조건식을 여러개 지정하는데 이때 사용하는 것이 논리연산자 AND, OR이다
```sql
SELECT *
FROM EMP
WHERE DEPTNO = 30
AND JOB = 'SALESMAN';
```
> WHERE절에서 비교하는 데이터가 문자열일 경우 작은따음표로 묶어줘야한다. 앞뒤에 공백이 있으면 공백도 문자로 인식하기 때문에 주의해야한다.

#### 산술 연산자
- 산술 연산자는 +, -, *, / 를 이용한다
```sql
SELECT *
FROM EMP
WHERE SAL * 12 = 36000;
```
#### 비교 연산자
- 대소관계를 나타내기 위해 사용된다.
```sql
SELECT *
FROM EMP
WHERE SAL >= 3000;
```
- 대소 비교 연산자는 숫자가 아닌 문자열일 때도 사용할 수 있다
```sql
SELECT *
FROM EMP
WHERE ENAME >= 'F';
```
- 사원 이름의 첫 문자가 F와 같거나 G, ..., Z까지의 사람을 출력한다.
```sql
SELECT *
FROM EMP
WHERE ENAME <= 'FORZ';
```
- FORZ 문자열보다 알파벳 순서로 앞에 있는 행을 출력하게 된다
- 만약 ENAME컬럼에 FORD라는 데이터가 있다면 출력된다.

#### 등가 비교 연산자
- 연산자 양쪽 항목이 같은 값인지 검사하는 연산자이다
- 종류는
	- = : 같을 경우 true, 다를 경우 false
	- !=, <>, ^= : 다를 경우 true, 같을 경우 false

#### 논리 부정 연산자
- false를 true로 true를 false로 반환 시키는 연산자이다
```sql
SELECT *
FROM EMP
WHERE NOT SAL = 3000;
```
- 급여가 3000인 사람을 제외하고 출력하는 SQL문이 된다

#### IN 연산자
- 출력하고 싶은 열의 조건이 여러가지일 경우 OR 연산자로 여러 조걱식을 묶어 주는 것도 방버이지만, 조건이 늘어날수록 조건식이 많아지기에 IN 연산자를 이용하여 특정 열에 해당하는 조건을 여러 개 지정할 수 있다.
```sql
SELECT [조회할 열1 이름], [조회할 열2 이름], ... [조회할 열N 이름]
FROM [조회할 테이블 이름]
WHERE [열 이름] IN (데이터1, 데이터2, ..., 데이터N);
```
- 다음 두 SQL문은 같은 결과를 출력한다.
```SQL
SELECT *
FROM EMP
WHERE JOB = 'MANAGER' 
    OR JOB = 'SALESMAN'
    OR JOB = 'CLERK';
```
```SQL
SELECT *
FROM EMP
WHERE JOB IN ('MANAGER', 'SALESMAN', 'CLERK');
```

- 만약 해당 경우에 반대되는 경우를 찾을 경우 NOT을 사용하도록 한다.

```SQL
WHERE JOB NOT IN ('MANAGER', 'SALESMAN', 'CLERK');
```

#### BETWEEN A AND B 연산자
- 한 열 값이 2000 이상 3000이하인 경우를 조회할 경우 AND연산자를 다음과 같이 구할 수 있다

```SQL
SELECT *
FROM EMP
WHERE SAL >= 2000
    AND SAL <= 3000;
```
- 특정 열 값의 최소, 최고 범위를 지정하여 출력하는 경우라면 BETWEEN A AND B 연산자를 사용하면 더 간단하게 표현할 수 있다.
```SQL
SELECT *
FROM EMP
WHERE SAL BETWEEN 2000 AND 3000;
```
- 만약 해당 결과를 제외한 것을 조회하고 싶은 경우 NOT 연산자를 사용한다

```SQL
WHERE SAL NOT BETWEEN 2000 AND 3000;
```

#### LIKE 연산자

- LIKE연산자는 문자열이 포함된 데이터를 조회할때 사용한다.
- S로 시작하는 칼럼을 찾고자 한다면 다음과 같이 사용할 수 있다
```SQL
SELECT *
FROM EMP
WHERE ENAME LIKE 'S%';
```
- % 기호는 와일드 카드라고 한다.
- 와일드카드는 특정 문자 또는 문자열을 대체하거나 문자열 데이터의 패턴을 표기하는 특수문자이다.
- 또한 %말고도  _기호도 사용할 수 있다
- _ : 어떤 값이든 상관없이 한 개의 문자 데이터를 의미
- % : 길이와 상관없이 모든 문자 데이터를 의미
- 다음과 같이 SQL을 작성하면 두번째 문자는 S이고 S문자 앞에는 한 문자, 뒤에는 상관없이 모두 가능
```SQL
SELECT *
FROM EMP
WHERE ENAME LIKE '_S%';
```
- 마찬가지로 해당 조건을 제외한 결과를 조회하고 싶다면 NOT연산자를 사용한다

```SQL
WHERE ENAME NOT LIKE '_S%';
```
#### IS NULL
- 특정 열 또는 연산의 결과 값이 NULL인지 여부를 확인하려면 IS NULL연산자를 사용한다.
- 다음 SQL문을 실행하면 COMM열의 값이 NULL인 결과를 반환한다.
```SQL
SELECT *
FROM EMP
WHERE COMM IS NULL;
```
- 마찬가지로 해당 결과를 제외한 것을 조회하려면 NOT연산자를 사용한다.
```SQL
SELECT *
FROM EMP
WHERE COMM IS NOT NULL;
```
### 집합 연산자
- SQL문에서는 SELECT문ㅇ을 통해 데이터를 조회한 결과를 하나의 잡합과 같이 다룰 수 있는 집한 연산자를 사용할 수 있다.
```SQL
SELECT EMPNO, ENAME, SAL, DEPTNO
	FROM EMP
	WHERE DEPTNO = 10
UNION
SELECT EMPNO, ENAME, SAL, DEPTNO
	FROM EMP
	WHERE DEPTNO = 20;
```
- 주의할 점은 집한 연산자로 두 개의 SELECT문의 결과 값을 연결할 때 각 SELECT문이 출력하려는 열 개수와 각 열의 자료형이 순서별로 일치해야한다는 것이다.
- 집합 연산자는 4가지 종류가 있다ㅣ
	- UNION : 연결된 SELECT문의 결과 값을 합집합으로 묶어 주고 중복 데이터는 제거된다
	- UNION ALL : 연결된 SELECT문의 결과 값을 합집합으루 묶고 중복 데이터도 츨력한다
	- MINUS : 먼저 작성한 SELECT문의 결과 값에서 다음 SELECT문의 결과 값을 차집합 처리한다.
	- INTERSECT : 먼저 작성한 SELECT문과 다음 SELECT문의 결과 값이 같은 데이터만 출력한다. (교집합)

### 연산자 우선순위
- 높음
	*, /
	+, -
	=, !=, ^=, <>, >, >=, <, <=
	IS NULL, LIKE, IN
	BETWEEN A AND B
	NOT
	AND
	OR
- 낮음

