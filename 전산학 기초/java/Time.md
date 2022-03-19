# Time (java.time)

## 종류

날짜, 시간, 날짜시간, 협정세계시 4가지로 구분해서 사용할 수 있다.

### LocalData

```java
LocalDate localDate = LocalDate.now();
LocalDate localDate = LocalDate.of(int year, Month month, int dayOfMonth);
LocalDate localDate = LocalDate.of(int year, int month, int dayOfMonth);
```

- year – MIN_YEAR to MAX_YEAR
- month – 1 (January) to 12 (December)
- dayOfMonth – 1 to 31
- `Month`는 이넘타입이며 `JANUARY`,`DECEMBER`으로 사용하거나 Month.of(int month)로 사용할 수 있다.

### LocalTime

```java
LocalTime localTime = LocalTime.now();
LocalTime localTime = LocalTime.of(int hour, int minute);
LocalTime localTime = LocalTime.of(int hour, int minute, int second);
LocalTime localTime = LocalTime.of(int hour, int minute, int second, int nanoOfSecond);
```

- hour – 0 to 23
- minute – 0 to 59
- second – 0 to 59
- nanoOfSecond – 0 to 999,999,999

### LocalDateTime

```java
LocalDateTime localDateTime = LocalDateTime.now();
LocalDateTime localDateTime = LocalDateTime.of(LocalDate date, LocalTime time);
LocalDateTime localDateTime = LocalDateTime.of( ... );
```

- LocalDateTime.of 에 들어갈 수 있는 경우는 LocalDate, LocalTime에서 사용되는 `of`의 6가지 조합으로 구성되어 있다.

### ZoneDateTime

```java
ZonedDateTime zdt = ZonedDateTime.now();
ZonedDateTime zdt = ZonedDateTime.of(LocalDateTime localDateTime, ZoneId zone);
ZonedDateTime zdt = ZonedDateTime.of(LocalDate date, LocalTime time, ZoneId zone);
ZonedDateTime zdt = ZonedDateTime.of(int year, int month, int dayOfMonth, int hour, int minute, int second, int nanoOfSecond, ZoneId zone);
```

- ZoneID - the time-zone ID, not null

  https://en.wikipedia.org/wiki/List_of_tz_database_time_zones 를 참고하여 타임존을 입력하면된다.

## 설정
일반적으로 withXXX로 값을 설정할 수 있다.

```java
LocalTime lt = LocalTime.now().withSecond(10);
LocalDate ld = LocalDate.now().withMonth(2);
LocalDateTime ldt = LocalDateTime.now().withYear(2222);
ZonedDateTime zdt = ZonedDateTime.now().withHour(12);
```

- withXXX 리턴값은 해당 타입으로 리턴된다.

## 포맷

포맷은 이미 지정된 ISO 타입인 static 값도 있고 `ofLocalizedXXX`로 커스텀하게 사용할 수 도 있다.

```java
DateTimeFormatter.ISO_DATE;
DateTimeFormatter.ISO_OFFSET_DATE_TIME;

DateTimeFormatter.ofLocalizedDateTime(FormatStyle.FULL);
DateTimeFormatter.ofLocalizedDateTime(FormatStyle.LONG, FormatStyle.MEDIUM);
DateTimeFormatter.ofLocalizedDate(FormatStyle.MEDIUM);
DateTimeFormatter.ofLocalizedTime(FormatStyle.SHORT);
```

- `ofLocalizedXXX`에 withXXX로 몇몇 설정을 추가할 수 있다.
  - withZone을 이용하여 원하는 지역에 맞게 포매팅을 변경할 수 있다.

다음과 같이 사용한다.

```java
ZonedDateTime.now().format(DateTimeFormatter formatter);
```

