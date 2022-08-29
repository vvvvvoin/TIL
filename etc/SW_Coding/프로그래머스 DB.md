# 프로그러매스 DB문제 (ORACLE)

## LV1

### 최댓값 구하기

- `ANIMAL_INS` 테이블에서 가낭 늦게 들어온 동물을 구하는 문제이다.
- MAX함수를 이용해 가장 큰값, 오래된 값하나를 출력하게 된다.

```sql
SELECT MAX(DATETIME)
FROM ANIMAL_INS;
```

### 모든 레코드 조회하기

- 특정 컬럼을 기준으로 오름차순으로 정렬하여 전체 데이터를 출력하는 문제이다.

```SQL
SELECT *
FROM ANIMAL_INS
ORDER BY ANIMAL_ID;
```

### 역순 정렬하기

- 특정 컬럼을 기준으로 내림차순으로 `NAME`, `DATETIME` 컬럼을 출력하는 문제이다.

```SQL
SELECT NAME, DATETIME
FROM ANIMAL_INS
ORDER BY ANIMAL_ID DESC;
```

> 오름차순이 DEFAULT이고 명시적으로 ASC로 사용할 수 있다.

### 아픈 동물 찾기

- `INTAKE_CONDITION` 컬럼에 `Sick`인 데이터를 `ANIMAL_ID`로 내림차순으로 `ANIMAL_ID`와 `NAME`을 출력하는 문제이다.

```SQL
SELECT ANIMAL_ID, NAME
FROM ANIMAL_INS
WHERE INTAKE_CONDITION = 'Sick'
ORDER BY ANIMAL_ID;
```

### 어린 동물 찾기

- `INTAKE_CONDITION`컬럼의 값이 `Aged`가 아닌 데이터를 `ANIMAL_ID`를 기준으로 `ANIMAL_ID, NAME`을 출력하는 문제이다.

```SQL
SELECT ANIMAL_ID, NAME
FROM ANIMAL_INS
WHERE INTAKE_CONDITION ^= 'Aged'
ORDER BY ANIMAL_ID;
```

> 등가 연산자 중 다를 경우 TRUE를 반환하는 연산자는 !=, <>, ^= 가 있다.

### 동물의 아이디와 이름

- `ANIMAL_INS`테이블에서 모든 동물의 아이디와 이름을 `ANIMAL_ID`순으로 출력하는 문제이다.

```SQL
SELECT ANIMAL_ID, NAME
FROM ANIMAL_INS
ORDER BY ANIMAL_ID;
```

### 이름이 없는 동물의 아이디

- 테이블에서 `NAME`컬럼 값이 `NULL`인 동물의 ID를 출력하는 문제이다.

```SQL
SELECT ANIMAL_ID
FROM ANIMAL_INS
WHERE NAME IS NULL
ORDER BY ANIMAL_ID;
```

### 여러 기준으로 정렬하기

- `NAME`순으로 데이터를 조회하는데 이름이 같은 경우 보호를 나중에 시작한 동물을 먼저 보여줘야한다.

```SQL
SELECT ANIMAL_ID, NAME, DATETIME
FROM ANIMAL_INS
ORDER BY NAME ASC, DATETIME DESC;
```

### 상위 N개 레코드

- 테이블에서 가장 먼저 들어온 동물의 `NAME`을 출력하는 문제이다.

```SQL
---01
SELECT NAME
FROM ANIMAL_INS
WHERE DATETIME = (
    SELECT MIN(DATETIME) 
    FROM ANIMAL_INS
);
---02
SELECT NAME
FROM (
    SELECT *
    FROM ANIMAL_INS
    ORDER BY DATETIME ASC
)
WHERE ROWNUM <= 1;
```

- 1번은 서브쿼리로 `DATETIME`이 가장 작은 값을 찾아 조건문과 비교해서 TRUE인 행의 `NAME`을 출력했다.
- 2번은 서브쿼리로 오름차순으로 정렬된 `ANIMAL_INS`테이블에서 최상단에 위친 값하나의 `NAME`을 출력했다.

### 이름이 있는 동물의 아이디

- `NAME`이 `NULL`이 아닌 동물의 아이디를 조회하는 문제이다.

```SQL
SELECT ANIMAL_ID
FROM ANIMAL_INS
WHERE NAME IS NOT NULL
ORDER BY ANIMAL_ID;
```

## LV2

### 최솟값 구하기

- `DATETIME`이 가장 작은 값을 출력하는 문제이다.

```SQL
SELECT MIN(DATETIME)
FROM ANIMAL_INS;
```

### 동물 수 구하기

- 테이블 전체에 몇 마리의 동물이 있는지 출력하는 문제이다.

```SQL
SELECT COUNT(ANIMAL_ID)
FROM ANIMAL_INS;
```

### 중복 제거하기

- 테이블에서 `NAME`의 수를 출력하는데 중복되는 이름이거나 NULL인 경우를 제외하고 출력하는 문제이다.

```SQL
SELECT COUNT(DISTINCT(NAME))
FROM ANIMAL_INS;
```

### 고양이와 개는 몇 마리 있을까

- 테이블에서 동물의 종류가 고양이 개가 각각 몇마리인지 조회하는데 고양이를 개보다 먼저 조회해야한다.

```SQL
SELECT ANIMAL_TYPE, COUNT(*)
FROM ANIMAL_INS
GROUP BY ANIMAL_TYPE
    HAVING ANIMAL_TYPE IN('Cat', 'Dog')
ORDER BY ANIMAL_TYPE;
```

- 테이블에는 동물의 종류가 `Cat`, `Dog`만 존재하지만 다른 종류가 있다면 HAVING절을 사용하여 구분해야한다.

### NULL 처리하기

- 테이블에 ID순으로 `ANIMAL_TYPE`,`NAME`,`SEX_UPON_INTAKE`를 출력하는 문제이다.
- 단 `NAME`중 NULL이 있다면 `No name`이라고 대체하여 출력해야한다.

```SQL
---01
SELECT ANIMAL_TYPE, NVL(NAME, 'No name'), SEX_UPON_INTAKE
FROM ANIMAL_INS
ORDER BY ANIMAL_ID;
---02
SELECT ANIMAL_TYPE, NVL2(NAME, NAME,'No name'), SEX_UPON_INTAKE
FROM ANIMAL_INS
ORDER BY ANIMAL_ID;
```

- `NVL함수`는 NULL일 DEFAULT값을 설정해줄 수 있다.
- `NVL2함수`는 NULL인 경우와 아닌 경우를 설정해줄 수 있다.

### 동명 동물 수 찾기

- 테이블에 동명의 `NAME`인 동물의 수를 출력하는 문제이다.
- 단 해당 `NAME`은 동명인 경우이므로 2마리 이상인 경우만 출력한다.

```SQL
SELECT NAME, COUNT(NAME)
FROM ANIMAL_INS
GROUP BY NAME
	HAVING COUNT(NAME) > 1
ORDER BY NAME;
```

- HAVING절을 사용해 조건을 만족시켜줄 수 있도록 한다.

### 입양 시각 구하기(1)

- 보호소에서 몇시`(DATETIME)`에 입양이 활발이 일어나는지 알아보는 문제이다.

- 09시부터 19시까지의 시간대별 입양수를 출력하는 문제이다.
- 우선 DATETIME의 타입은 DATE이므로 이를 `TO_CHAR`함수를 이용해 시간대만을 뽑아서 사용한다.

```SQL
SELECT TO_CHAR(DATETIME, 'HH24') AS HOUR, COUNT(DATETIME)
FROM ANIMAL_OUTS
GROUP BY TO_CHAR(DATETIME, 'HH24')
	HAVING TO_CHAR(DATETIME, 'HH24') >= 9 AND
		TO_CHAR(DATETIME, 'HH24') <= 19
ORDER BY TO_CHAR(DATETIME, 'HH24');
```

- `TO_CHAR`함수에서 타입을 `HH24`로 설정해 24시형인 `시`만 뽑는다
- 그리고 해당 값이 9시 이상 19시 이하로 HAVING절로 제한시켜준다.
- 컬럼에 문자로 바뀐 `시`를 다시 숫자로 변형해 불필요한 문자를 제거시켜준다.

### 루시와 엘라 찾기

- 테이블에서 `NAME`이 Lucy, Ella, Pickle, Rogan, Sabrina, Mitty인 동물의 아이디와 이름, 성별, 중성화 여부를 출력하는 문제이다.

```sql
SELECT ANIMAL_ID, NAME, SEX_UPON_INTAKE
FROM ANIMAL_INS
WHERE NAME IN ('Lucy', 'Ella', 'Pickle', 'Rogan', 'Sabrina', 'Mitty')
ORDER BY ANIMAL_ID;
```

### 이름에 el이 들어가는 동물찾기

- 테이블에서 동물의 타입이 개이면서 이름에 `EL`이 들어간 동물을 찾는 문제이다.
- 단 이름에 들어가는 `EL`은 대소문자를 구분하지 않고 `EL`이 들어간 모든 동물을 찾아야 한다.

```SQL
SELECT ANIMAL_ID, NAME
FROM ANIMAL_INS
WHERE UPPER(NAME) LIKE '%EL%' AND ANIMAL_TYPE = 'Dog'
ORDER BY NAME;
```

- `UPPER`, `LOWER`함수를 사용해 조회하는 `NAME`이 조건에 모두 만족시킬 수 있도록 한다.

### 중성화 여부 파악하기

- 테이블에서 중성화가 되있으면`SEX_UPON_INTAKE`컬럼에  `Neutered`, `Spayed` 라는 단어가 들어가 있다.
- 중성화된 동물들만을 출력하는 문제이다.

```SQL
---01
SELECT ANIMAL_ID, NAME, 
    CASE 
         WHEN SEX_UPON_INTAKE LIKE 'Neutered%' THEN 'O'
         WHEN SEX_UPON_INTAKE LIKE 'Spayed%' THEN 'O'
         ELSE 'X'
    END as 중성화
FROM ANIMAL_INS
ORDER BY ANIMAL_ID;
---02
SELECT ANIMAL_ID, NAME, 
    CASE 
         WHEN REGEXP_LIKE(SEX_UPON_INTAKE, '^Neutered|^Spayed', 'c') THEN 'O'
         ELSE 'X'
    END as 중성화
FROM ANIMAL_INS
ORDER BY ANIMAL_ID;
```

- CASE문을 사용하여 조건을 구분하여 들어갈 값을 매핑시켜준다.
- 혹은 정규식을 사용하여 2번과 같이할 수 있다.

> https://jhnyang.tistory.com/292

### DATETIME에서 DATE로 형 변환

- 테이블에 `DATETIME`컬럼에 값이 `2018-01-22 14:32:00`이면 `2018-01-22`과 같은 형태로 변환하는 문제이다.

```SQL
SELECT ANIMAL_ID, NAME, TO_CHAR(DATETIME, 'YYYY-MM-DD') AS 날짜
FROM ANIMAL_INS;
```

## LV3

### 없어진 기록 찾기

- 보호소에 들어온 테이블, 입양된 테이블이 존재한다.
- 하지만 천재지변으로 인해 데이터가 손실되었다.
- 입양간 기록은 있는데 보호소에 들어온 기록이 없는 동물의 ID와 이름을 출력하는 문제이다.

```SQL
SELECT O.ANIMAL_ID, O.NAME
FROM ANIMAL_INS I RIGHT OUTER JOIN ANIMAL_OUT O ON(I.ANIMAL_ID = O.ANIMAL_ID)
WHERE I.DATETIME IS NULL
ORDER BY O.ANIMAL_ID;
```

- 두 테이블을 조인하는데 입양간 테이블을 모두 출력할 수 있도록 OUTER JOIN을 사용한다.
- 그리고 보호소에 들어온 기록이 NULL인 동물을 찾아 출력하도록 한다.

### 있었는데요 없었습니다

- 보호소에 들어온 기록을 담은 테이블과 입양을 간 기록을 담은 테이블이 있다.
- 이때 직원의 실수로 보호소에 들어온 날자가 입양날짜보다 더 빠르게 작성되었는데 잘못작성된 데이터를 출력하는 문제이다.

```SQL
SELECT I.ANIMAL_ID, I.NAME
FROM ANIMAL_INS I JOIN ANIMAL_OUTS ON(I.ANIMAL_ID = O.ANIMAL_ID)
WHERE I.DATETIME > O.DATETIME
ORDER BY I.DATETIME;
```

- 두 테이블을 ID를 기준으로 조인한다.
- 그리고 보호소에 들어온 테이블의 `DATETIME`이  입양테이블의 `DATETIME`보다 큰 경우, 빠른경우를 조건으로 두고 출력하도록 한다.

### 오랜 기간 보호한 동물(1)

- 보호소에 들어온 기록을 담은 테이블과 입양을 간 기록을 담은 테이블이 있다.
- 입양을 아직 못간 동물 중 보호소에 들어온지 가장 오래된 동물 3마리의 이름과 보호시작일을 출력하는 문제이다.

```SQL
SELECT *
FROM   
    (SELECT I.NAME, I.DATETIME
        FROM ANIMAL_INS I LEFT OUTER JOIN ANIMAL_OUTS O ON(I.ANIMAL_ID = O.ANIMAL_ID)
        WHERE O.ANIMAL_ID IS NULL 
     ORDER BY I.DATETIME)
WHERE ROWNUM <= 3;
```

- 서브쿼리로 보호소로 들어온 테이블과 입양간 테이블을 조인시켜주는데 보호소에 들어온 기록을 전부 나타낼 수 있도록 한다.
- 그리고 조건으로 입양간 기록이 NULL인 경우를 찾아 입양가지 못한 동물을 구한다.
- 보호소에 들어온 테이블을 오름차순으로 정렬 후 `ROWNUM`을 이용해 3마리를 출력할 수 있도록 한다.

### 오랜 기간 보호한 동물(2)

- 보호소에 들어온 기록을 담은 테이블과 입양을 간 기록을 담은 테이블이 있다.
- 입양을 간 동물 중 보호기간이 가장 길어던 동물 2마리를 출력하는 문제이다.

```SQL
SELECT * 
FROM (
    SELECT O.ANIMAL_ID, O.NAME
    FROM ANIMAL_INS I JOIN ANIMAL_OUTS O ON(I.ANIMAL_ID = O.ANIMAL_ID)
    ORDER BY I.DATETIME - O.DATETIME
)
WHERE ROWNUM <= 2
```

- 서브쿼리로 보호소 테이블과 입양 테이블을 등가조인을 해준다
- `보호소에 들어간 기간 - 입양간 기간` 순으로 데이터를 정렬하고 `ROWNUM`을 이용해 2마리만 출력한다.

## LV4

### 우유와 요거트가 담긴 장바구니

- `CART_PRODUCTS`테이블에서 `NAME`이 `Milk`,` Yogurt`를 모두 가지는 `CART_ID`를 출력하는 문제이다.

```SQL
SELECT M.CART_ID
FROM(
	SELECT *
    FROM CART_PRODUCTS
    WHERE NAME = 'Milk'
) M JOIN (
	SELECT *
    FROM CART_PRODUCTS
    WHERE NAME = 'Yogurt'
) Y ON (M.CART_ID = Y.CART_ID)
ORDER BY CART_ID
```

- `Milk`,` Yogurt`를 각각 찾는 서브쿼리를 사용한다.
- 그리고 두 서브쿼리를 `CART_ID`로 등가조인을 수행하면 두 물건을 가진 `CART_ID`를 구할 수 있다.

### 입양 시간 구하기(2)

- 보호소에서 0시부터 23시까지 각 시간대별로 입양이 몇건 일어났는지 출력하는 문제이다.

```SQL
SELECT L.LV AS HOUR, NVL(H.CNT, 0) AS COUNT
FROM (
    SELECT LEVEL-1 AS LV
    FROM DUAL
    CONNECT BY LEVEL <= 24
) L LEFT OUTER JOIN(
    SELECT TO_CHAR(DATETIME, 'HH24') AS HOUR, COUNT(*) AS CNT
    FROM ANIMAL_OUTS
    GROUP BY TO_CHAR(DATETIME, 'HH24')
    ) H ON(L.LV = H.HOUR)
ORDER BY L.LV;
```

- 우선 첫 번째 0~23까지 테이블을 출력하는 서브쿼리를 작성한다.
- 두 번재 서브쿼리에는 `입양 시각 구하기(1)`처럼 `TO_CHAR`를 이용해 `24시 시`형태로 변환해 `COUNT`함수를 이용하여 값을 구한다.
- 두 서브쿼리에서 첫 번째 서브쿼리의 내용이 모두 출력될 수 있도록 OUTER JOIN을 수행한다.
- 그러면 입양가지 않은 시간대에는 값이 NULL이 들어가는데 이때 `NVL함수`를 이용해 NULL처리를 해준다.

### 보호소에서 중성화한 동물

- 보호소에 들어왔을때는 중성화되지 않고 입양나갈지 중성화된 동물을 출력하는 문제이다.

```SQL
SELECT O.ANIMAL_ID, O.ANIMAL_TYPE, O.NAME
FROM(
    SELECT *
    FROM ANIMAL_INS
    WHERE SEX_UPON_INTAKE LIKE 'Intact%'
) I JOIN (
    SELECT *
    FROM ANIMAL_OUTS
    WHERE REGEXP_LIKE(SEX_UPON_OUTCOME, '^Spayed|^Neutered')
) O ON(I.ANIMAL_ID = O.ANIMAL_ID)
```

- 첫 번째 서브쿼리에는 보호소에 들어왔을시 `SEX_UPON_INTAKE`칼럼 값에 `Intact`가 들어가는 동물을 조회한다.
- 두 번째 서브쿼리에는 입양갔을때 `SEX_UPON_OUTCOME`칼럼값이 `Spayed`이거나 `Neutered` 로 시작하는 동물을 조회한다.
- 두 서브쿼리를 등가조인하여 보호소에 들어왔을때 중성화되지 않았고 입양시 중성화된 동물을 찾을 수 있게 된다.