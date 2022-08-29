### SharedPreferences

- 안드로이드에서 기본적으로 제공하는 앱 데이터를 관리해주는 기능
- SQLite 같은 DB에 저장하거나 파일로써 저장하기 부담되는 설정 값, 변수값을 간편하게 저장함
- 앱을 삭제할 경우 SharedPreferences의 데이터 또한 삭제됨

#### SharedPreferences 파일 불러오기
- "공유설정파일"라는 이름의 환경변수 설정데이터를 불러옴
```java
SharedPreferences sharedPreferences = getSharedPreferences("공유설정파일", MODE_PRIVATE);
```
> 주의: MODE_WORLD_READABLE 및 MODE_WORLD_WRITEABLE 모드는 API 수준 17부터 지원 중단되었습니다. Android 7.0(API 수준 24)부터 Android에서 이러한 모드를 사용하면 SecurityException이 발생합니다.

> 파일 이름 앞에 애플리케이션 ID를 붙이면 쉽습니다. 예: "com.example.mytestapplication.PREFERENCE_FILE"

- 환경설정 파일이 하나일 경우 getPreferecnces()를 사용할 수 있다
```java
SharedPreferences sharedPreferences = getPreferences(Context.MODE_PRIVATE);
```


#### SharedPreferences 변수 저장하기
- SharedPreferences에서 edit()를 호출하여 SharedPreferences.Editor를 만든다
```java
SharedPreferences sharedPreferences = getSharedPreferences("공유설정파일", MODE_PRIVATE);
SharedPreferences.Editor editor = appData.edit();
```
- 저장 타입은 boolean, float, int, long, String
- editor는 key와 value의 한쌍으로 값을 저장
- 변수를 기입 후 apply(), commit()을 반드시 해줘야한다.
```java
editor.putBoolean("booleanValue", true);
editor.apply();
//editor.commit();
```

#### SharedPreferences 변수 일기
- 저장했던 타입과 값은 method를 이용하여 불러온다
- 만약 키가 존재하지 않으면 반환할 기본값을 지정해준다.
```java
SharedPreferences sharedPreferences = getSharedPreferences("공유설정파일", MODE_PRIVATE);
//booleanValue라는 키에 저장된 변수를 반환
//booleanValue라는 키가 존재하지 않을 경우 false를 기본값으로 반환
boolean value = sharedPreferences.getBoolean("booleanValue", false);
```



참고 : [https://developer.android.com/training/data-storage/shared-preferences?hl=ko#java](https://developer.android.com/training/data-storage/shared-preferences?hl=ko#java)


































































