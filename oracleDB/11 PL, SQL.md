# PL/SQL

- PL, SQL은 SQL만으로는 구현이 어렵거나 불가능한 작업을 수행하기 위해 오라클에서 제공하는 프로그래밍 언어이다.
- 변수, 조건처리, 반복처리 등 다른 프로그래밍 언어에서도 제공하는 다양한 기능을 제공한다.

## PL/SQL 구조

### 블록이란?

- PL/SQL은 DB 관련 특정 작업을 수행하는 명령어와 실행에 필요한 여러 요소를 정의하는 명령어 등으로 구성되며, 이러한 명령어를 모아 둔 PL/SQL 프로그램의 기본 단위를 블록이라고 한다.
- DECLARE : 선택, 실행에 사용될 변수, 상수, 커서등을 선언
- BEGIN : 필수 조건문, 반복문, SELECT, DML, 함수 등을 정의
- EXCEPTION : 선택, PL/SQL 실행 도중 발생하는 오류를 해결하는 문장

- 위 귀성을 기반으로 PL/SQL블록의 기본 형식은 다음과 같다.

```SQL
DECLARE
	[실행에 필요한 여러 요소 선언];
BEGIN
	[작업을 위해 실제 실행하는 명령어];
EXCEPTION
	[PL/SQL 수행 도중 발생하는 오류 처리];
END;
```

- 선언부와 예외 처리부는 생략 가능하지만 실행부는 반드시 존재햐아한다.
- 필요에 따라 PL/SQL 블록안에 다른 블록이 포함될 수 있다.

### HELLO, PL/SQL 출력하기

- PL/SQL문을 이용하여 간단한 형태의 문장을 화면에 출력할 수 있다.
- 실행 결과를 화면에 출력하기 위해 SERVEROUTPUT 환경 변수 값을 ON으로 변경해준다.
- PUT_LINE은 화면 출력을 위해 오라클에서 기본으로 제공한다.

```SQL
SET SERVEROUTPUT ON;
BEGIN
	DBMS_OUTPUT.PUT_LINE('HELLO, PL/SQL');
END;
/
```

- 위 PL/SQL 문의 실행 결과를 참고하여 PL/SQL문을 작성하고 실행하기 위해 다음 사항을 기억해야한다.
  - PL/SQL 블록을 구성하는 DECLARE, BEGIN, EXCEPTION 키워드에는 세미콜론을 사용하지 않는다.
  - PL/SQL 블록의 각 부분애ㅔ서 실행해야 하는 문장 끝에서 세미콜론을 사용한다.
  - PL./SQL문 내부에서 한 줄 주석과 여러 줄 주석을 사용할 수 있다
  - PL/SQL문 작성을 마치고 실행하기 위해 마지막에 슬래시를 사용한다.

### PL/SQL 주석

- PL/SQL 주석은 코드에 포함되어 있지만 실행되지 않는 문장을 뜻한다.
- 일반적으로 특정 기호를 사용하여 코드 설명 또는 이력등을 남겨 놓거나 일시적으로 실행되지 않기를 원하는 코드를 삭제하지 않고 남겨 두는 용도로 주석 영역을 지정한다.
- 한 줄 주석 : --, 현재 줄만 주석 처리된다.
- 여러 줄 주석 : /*    */, 기호 사이에 모든 줄이 주석 처리돈다.

## 변수와 상수

### 변수 선언과 값 대입하기

- 변수는 데이터를 일시적으로 저장하는 요소로 이름과 저장할 자료형을 지정하여 선언부에서 작성한다.
- 선언부에서 작성한 변수는 실행부에서 활용된다.

#### 기본 변수 선언과 사용

- 변수를 선언하는 기본 형식은 다음과 같다.

```SQL
변수이름 자료형 := 값 또는 값이 도출되는 여러 표현식;
```

- 변수이름 : 데이터를 저장할 변수 이름을 지정한다.
- 자료형 : 선언한 변수에 저장할 데이터의 자료형을 지정한다.
- 선언한 변수에 값을 할당하기 위해 := 를 사용한다.

- PL/SQL문에서 자료형을 지정하는 방법은 테이블 생성 방식과 비슷하다.

```SQL
DECLARE
	V_EMPNO NUMBER(4) := 7788;
	V_ENAME VARCHAR2(10);
BEGIN
	V_ENAME := 'SCOTT';
	DBMS_OUTPUT.PUT_LINE('V_EMPNO : ' || V_EMPNO);
	DBMS_OUTPUT.PUT_LINE('V_ENAME : ' || V_ENAME);
END;
/
```

#### 상수 정의하기

- 저장한 값이 필요에 따라 변하는 변수와 달리 상수는 한번 저장한 값이 프로그램이 종료될 때까지 유지되는 저장 요소이다.

```sql
변수이름 CONSTANT 자료형 := 값 또는 값이 도출되는 여러 표현식;
```

```SQL
DECLARE
	V_TAX CONSTANT NUMBER(1) := 3;
BEGIN
	DBMS_OUTPUT.PUT_LINE('V_TAX : ' || V_TAX);
END;
/
```

#### 변수의 기본값 지정하기

- DEFAULT 키워드는 변수에 저장할 기본값을 지정한다.

```SQL
변수이름 자료형 DEFAULT 값 또는 값이 도출되는 여러 표현식;
```

```SQL
DECLARE
	V_DEPTNO NUMBER(2) DEFAULT 10;
BEGIN
	DBMS_OUTPUT.PUT_LINE('V_DEPTNO : ' || V_DEPTNO);
END;
/
```

#### 변수에 NULL 값 저장 막기

- 특정 변수에 NULL이 저장되지 않게 하려면 NOT NULL 키워드를 사용한다.
- PL/SQL 에서 선언한 변수는 특정 값을 할당하지 않으면 NULL 값이 기본으로 할당된다.

```SQL
변수이름 자료형 NOT NULL := or DEFAULT 값 또는 값이 도출되는 여러 표현식;
```

```SQL
DECLARE
	V_DEPTNO NUMBER(2) NOT NULL := 10;
BEGIN
	DBMS_OUTPUT.PUT_LINE('V_DEPTNO : ' || V_DEPTNO);
END;
/
```

### 변수의 자료형

- 변수에 저장할 데이터가 어떤 종료인지를 특정 짓기 위해 사용하는 자료형은 크게 스칼라, 복합, 참조, LOB로 구분된다.

#### 스칼라

  - 스칼라형은 숫자, 문자열, 날짜 등과 같이 오라클에서 기본으로 정의해 놓은 자료형으로 내부 구성 요소가 없는 단일 값을 의미한다.

  - NUMBER, CHAR, VARCHAR2, DATE, BOOLEAN

#### 참조형

- 참조형은 오라클 DB에 존재하는 특정 테이블 열의 자료형이나 하나의 행 구조를 참조하는 자료형이다.

- 열을 참조할 때 %TYPE, 행을 참조할 때 %ROWTYPE을 사용한다.

- %TYPE의 사용법은 다음과 같다

  ```SQL
  변수이름 테이블이름.열이름%TYPE;
  ```

  ```SQL
  DECLARE
  	V_DEPTNO DEPT.DEPTNO%TYPE := 90;
  BEGIN
  	DBMS_OUTPUT.PUT_LINE('V_DEPTNO : ' || V_DEPTNO);
  END;
  /
  ```

- 특정 테이블에서 하나의 열이 아닌 행 구조 전체를 참조할 때 %ROWTYPE을 사용한다.

```SQL
변수이름 테이블이름 이름%ROWTYPE;
```

- 다음은 %ROWTYPE을 활용하여 변수를 선언하고 있다.
- V_DEPTNO_ROW 변수가 DEPT테이블의 행 구조를 참고하도록 선언하였다.
- 즉 V_DEPTNO_ROW 변수는 내부에 DEPTNO, DNAME, LOC 필드를 가진다

```SQL
DECLARE
	V_DEPT_ROW DEPT%ROWTYPE;
BEGIN
	SELECT DEPTNO, DNAME, LOC INTO V_DEPT_ROW
	FROM DEPT
	WHERE DEPTNO = 40;
	DBMS_OUTPUT.PUT_LINE('DEPTNO : ' || V_DEPT_ROW.DEPTNO);
	DBMS_OUTPUT.PUT_LINE('DNAME : ' || V_DEPT_ROW.DNAME);
	DBMS_OUTPUT.PUT_LINE('LOC : ' || V_DEPT_ROW.LOC);
END;
/
```

#### 복합형, LOB형

- 스칼라형과 참조형 외에도 PL/SQL에서는 복합영과 LOB형을 사용할 수 있다.
- 이 중 봅합형은 여러 종류 및 개수의 데이터를 저장하기 위해 사용자가 직접 정의하는 자료형으로 컬렉션, 레코드로 구분된다.

## 조건 제어문

- 특정 조건식을 통해 상황에 따라 실행할 내용을 달리하는 방식의 명령어를 조건문이라고 한다.
- PL/SQL에서는 IF문과 CASE문을 사용할 수 있다.

### IF조건문

- PL/SQL에서 제공하는 IF조건문은 다음과 같이 3가지 방식을 사용할 수 있다
  - IF-THEN : 특정 조건을 만족하는 경우 작업 수행
  - IF-THEN-ELSE : 특정 조건을 만족하는 경우와 반대의 경우에 각각 지정한 작업수행
  - IF-THEN-ELSIF : 여러 조건에 따라 각각 지정한 작업 수행

#### IF-THEN

- 여러 프로그래밍 언어에서 사용하는 단일 IF문과 같은 역할을 하는 IF-THEN 문은 다음과 같이 사용한다.

```SQL
IF 조건식 THEN
	수행할 명령어;
END IF;
```

```SQL
DECLARE
	V_NUMBER NUMBER := 13;
BEGIN
	IF MOD(V_NUMBER, 2) = 1 THEN
		DBMS_OUTPUT.PUT_LINE('V_NUMBER은 홀수입니다');
	END IF;
END;
/
```

- 만약 위 예제에 짝수가 대입되면 아무런 결과가 출력되지 않는다.

#### IF-THEN-ELSE

- IF-TEHN-ELSE 문은 지정한 조건식의 결과 값이 TRUE일 경우에 실행할 명령어와 조건식의 결과값이 TRUE가 아닌 반대경우를 실행할 명령어를 각각 지정할 수 있다.

```SQL
IF 조건식 THEN
	수행할 명령어;
ELSE
	수행할 명령어
END IF;
```

- 다음 경우를 이용하여 짝수, 홀수를 구별할 수 있는 조건식을 만들 수 있다.

```SQL
DECLARE
	V_NUMBER NUMBER := 14;
BEGIN
	IF MOD(V_NUMBER, 2) = 1 THEN
		DBMS_OUTPUT.PUT_LINE('V_NUMBER은 홀수입니다');
	ELSE
		DBMS_OUTPUT.PUT_LINE('V_NUMBER은 짝수입니다');
	END IF;
END;
/
```

#### IF-THEN-ELSIF

- 결과 값이 TRUE인지 아닌지 여부에 따라 두가지 상황을 구현할 수 있는 IF-THEN-ELSE문과 달리 IF-THEN-ELSIF문은 여러 종류의 조건을 지정하여 각 조건을 만족하는 경우마다 다른 작업의 수행을 지정하는 것이 가능하다.

```SQL
IF 조건식 THEN
	수행할 명령어;
ELSIF 조건식
	수행할 명령어
ELSIF 조건식
	수행할 명령어
....
ELSE
	수행할 명렁어	
END IF;
```

- PL/SQL문은 점수에 따라 학점을 주기 위해 여러 조선식을 지정한다.
- 위에서부터 다음으로 조건식을 하나씩 실행하여 TRUE가 되는 영역의 작업이 수행될 것이다.

```SQL
DECLARE
	V_SCORE NUMBER := 87;
BEGIN
	IF V_SCORE >= 90 THEN
		DBMS_OUTPUT.PUT_LINE('A학점');
	ELSIF V_SCORE >= 80 THEN
		DBMS_OUTPUT.PUT_LINE('B학점');
	ELSIF V_SCORE >= 70 THEN
		DBMS_OUTPUT.PUT_LINE('C학점');
	ELSIF V_SCORE >= 60 THEN
		DBMS_OUTPUT.PUT_LINE('D학점');
	ELSE
		DBMS_OUTPUT.PUT_LINE('F학점');
	END IF;
END;
/
```

## CASE 조건문

- CASE조건문도 IF조건문과 마찬가지로 조건식의 결과 값에 따라 여러 가지 수행 작업을 지정할 수 있다.
- IF-THEN-ELSIF문과 같이 조건식의 결과 값이 여러 가지일 때 CAS 조건문을 좀 더 단순하게 표현할 수 있다.
- 단순 CASE 문 : 비교 기준이 되는 조건의 값이 여러 가지일 때 해당 값만 명시하여 작업 수행
- 검색 CASE 문 : 특정한 비교 기준 없이 여러 조건식을 나열하여 조선식에 맞는 작업 수행

#### 단순 CASE문

- 단순 CASE문은 비교기준이 되는 변수 또는 식을 명시한다.

```SQL
CASE 비교기준
	WHEN 값1 THEN
		수항할 명령어;
	WHEN 값2 THEN
		수항할 명령어;
	....
	ELSE
		수행할 명령어;
END CASE;
```

- 위에서 만든 학점을 출력하는 조건문을 CASE문으로 구현할 수 있다

```SQL
DECLARE
	V_SCORE NUMBER := 87;
BEGIN
	CASE TRUNC(V_SCORE/10)
		WHEN 10 THEN DBMS_OUTPUT.PUT_LINE('A학점');
		WHEN 9 THEN DBMS_OUTPUT.PUT_LINE('A학점');
		WHEN 8 THEN DBMS_OUTPUT.PUT_LINE('B학점');
		WHEN 7 THEN DBMS_OUTPUT.PUT_LINE('C학점');
		WHEN 6 THEN DBMS_OUTPUT.PUT_LINE('D학점');
		ELSE DBMS_OUTPUT.PUT_LINE('F학점');
	END CASE;
END;
/
```

#### 검색 CASE

- 검색 CASE문은 비교 기준을 명시하지않고 각각의 WHEN 절에서 조건식을 명시한 후 해당 조건을 만족할 때 수행할 작업을 정해 준다.

```SQL
CASE 
	WHEN 조건식 THEN
		수항할 명령어;
	WHEN 조건식 THEN
		수항할 명령어;
	....
	ELSE
		수행할 명령어;
END CASE;
```

- 학점 출력을 하기 위해 CASE문을 다음과 같이 만들 수 있다.

```SQL
DECLARE
	V_SCORE NUMBER := 87;
BEGIN
	CASE 
		WHEN V_SCORE >= 90 THEN DBMS_OUTPUT.PUT_LINE('A학점');
		WHEN V_SCORE >= 80 THEN DBMS_OUTPUT.PUT_LINE('B학점');
		WHEN V_SCORE >= 70 THEN DBMS_OUTPUT.PUT_LINE('C학점');
		WHEN V_SCORE >= 60 THEN DBMS_OUTPUT.PUT_LINE('D학점');
		ELSE DBMS_OUTPUT.PUT_LINE('F학점');
	END CASE;
END;
/
```

## 반복 제어문

- 반복문은 특정 작업을 반복하여 수행하고자 할 때 사용한다.
- PL/SQL 에서는 네가지 반복문을 제공한다.
  - LOOP : 기본 반복문
  - WHILE LOOP : 특정 조건식의 결과를 통해 반복 수행
  - FOR LOOP : 반복 횟수를 정하여 반복 수행
  - CUSOR FOR LOOP : 커서를 활용한 반복 수행
- 위에서 나열한 반복문 외에도 반복 수행을 중단시키거나 특정 반복 주기를 건너뛰는 다음 명령어도 있디
  - EXIT : 수행 중인 반복 종료
  - EXIT-WHEN : 반복 종료를 위한 조선식을 지정하고 만족하면 반복 종료
  - CONTINUE : 수행 중인 반복의 현재 주기를 건너뜀
  - CONTINUE-WHEN : 특정 조건식을 지정하고 조건식을 만족함녀 현재 반복 주기를 건너뜀

### LOOP

- LOOP문은 간단한 반복문이다

```SQL
LOOP
	반복 수행 작업;
END LOOP;
```

- 단 종료 시점이나 조건식을 명시해주지 않을 경우 무한루프에 빠지게 된다.
- EXIT 명령어를 사용하여 무한루프에 빠지지 않게 해준다.
- LOOP문을 이용하여 반복을 통해 값을 증가시킬 수 있다

```SQL
DECLARE
	V_NUM NUMBER := 0;
BEGIN
	LOOP
		DBMS_OUTPUT.PUT_LINE('현재 V_NUM : ' || V_NUM);
		V_NUM := V_NUM + 1;
		EXIT WHEN V_NUM > 4;
	END LOOP;
END;
/                          
```

### WHILE LOOP

- WHILE LOOP 문은 반복 수행 여부를 결정하는 조건식을 먼저 지정한 후 조선식의 결과 값이 TRUE일 떄 조건을 반복하고 FALSE가 되면 반복을 끝낸다.

```SQL
WHILE 조선식 LOOP
	수행작업;
END LOOP;
```

- 마찬가지로 0에서 4까지 증가하는 예제를 WHILE LOOP문으로 사용할 수 있다.

```SQL
DECLARE
	V_NUM NUMBER := 0;
BEGIN
	WHILE(V_NUM < 4) LOOP
		DBMS_OUTPUT.PUT_LINE('현재 V_NUM : ' || V_NUM);
		V_NUM := V_NUM + 1;
	END LOOP;
END;
/                          
```

### FOR LOOP

- FOR LOOP문은 반복의 횟수를 지정할 수 있는 반복문으로 다음과 같은 형태로 작성된다.
- 지정한 시작값부터 1씩 증가하여 종료갑셍 이를 때까지 작업을 반복 수행한다.
- FOR키워드 다음에 작성한 I는 반복 수행 중의 시작 값과 종료 값 사이의 현재 숫자가 저장되는 특수한 변수로 카운터라고 한다.
- 카운터는 선언부에 정의하지 않고 FOR LOOP문에서 바로 정의하여 사용한다.

```SQL
FOR I IN 시작값..종료값 LOOP
	수행작업;
END LOOP;
```

```SQL
BEGIN
	FOR I IN 0..4 LOOP
		DBMS_OUTPUT.PUT_LINE('현재 I 값 : ' || I);
	END LOOP;
END;
/
```

- 시작 값에서 종료 값을 역순으로 반복하고 싶다면 REVERSE키워드를 사용한다.

```SQL
FOR I IN REVERSE 시작값..종료값 LOOP
	수행작업;
END LOOP;
```

###  CONTINUE, CONTINUE-WHEN

- CONTINUE문은 반복 수행 중 CONTINUE가 실행되면 현재 반복주기에 수행해야 할 남은 작업을 건너뛰고 다음 반복 주기로 넘어가는 효과가 있다
- 위의 FOR-LOOP에서 사용한 예제에 CONTINUE를 이용하여 출력되는 경우를 제어할 수 있다.

```SQL
BEGIN
	FOR I IN 0..4 LOOP
		CONTINUE WHEN MOD(I , 2) = 1;
		DBMS_OUTPUT.PUT_LINE('현재 I 값 : ' || I);
	END LOOP;
END;
/
```

- I값을 2로 나눌 경우 나머지가1인 겨웅 즉 홀수일 때 CONTINUE문으로 다음 명령인 DBMS_OUTPUT.PUT_LINE이 실행되지 않고 다음 반복주기로 넘어가게 된다.