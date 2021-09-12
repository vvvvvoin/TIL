# Room (mobileDB) 사용방법
- 이전에 [Room](https://github.com/vvvvvoin/TIL/blob/master/android/kotlin/Room%20(mobileDB)%20%EA%B8%B0%EB%B3%B8%EA%B0%9C%EB%85%90.md) 개념을 확인하면 쉽게 이해할 수 있다
- Room의 구성요소인 Database, Entity, DAO에 대해 설명한다

## Entity
- DB의 테이블 역할을 한다
- @Entity(tableName = "테이블명")으로 테이블의 이름을 사용자가 지정할 수 있다
- 어노테이션이 없을 경우 default값으로 class명이 테이블명이 된다
- 대소문자는 구분하지 않는다
- @PrimaryKey 어노테이션으로 PK값을 지정한다
- autoGenerate속성값을 적어 ket값을 자동으로 생성할 수 있다
- @ColumnInfo으로 컬러명을 지정할 수 있다
- 어노테이션이 없다면 변수명이 컬럼명이 된다

```kotlin
@Entity(tableName = "marker")
data class MarkerEntity (
    @PrimaryKey(autoGenerate = true) var id : Int = 0,
    var subject: String = "",
    var content: String = "",
    @ColumnInfo(name = "LATITUDE") val lat: Double = 0.0,
    @ColumnInfo(name = "LONGITUDE") val lng: Double = 0.0,
    var writer: String = "",
    val address: String = ""
)
```

### Entity Annotation
#### @Entity
- @Entity 어노테이션을 이용해 테이블에 대한 설정을 한번에 지정할 수 있다

  - tableName() : Database내의 테이블 이름을 설정할 수 있습니다. 설정하지 않을경우 클래스이름이 기본값으로 설정됩니다.
  - indices() : 데이터베이스 쿼리 속도를 높이기 위한 컬럼들을 인덱스로 지정할 수 있습니다.
  - inheritSuperIndices() : true로 설정할 경우 부모클래스에 선언된 모든 인덱스가 현재의 Entity클래스로 옮겨집니다.
  - primaryKeys() : 기본키로 지정하고 싶은 칼럼 값들을 한번에 설정 할 수 있습니다.
  - foreignKeys() : 외래키로 지정하고 싶은 칼럼 값들을 한번에 설정 할 수 있습니다.
  - ignoredColumns() : DB에 생성되기를 원하지 않는 컬럼을 한번에 설정할 수 있습니다.
- 설정들을 @Entity 어노테이션에 설정하면 다음과 같다

```kotlin
@Entity(tableName = "marker",
    indices = arrayOf(Index(value = ["lat", "lng"])),
    inheritSuperIndices = true,
    primaryKeys = arrayOf("id"),
    foreignKeys = arrayOf(
        ForeignKey(
            entity = PersonEntity::class,
            parentColumns = arrayOf("personId"),
            childColumns = arrayOf("personForeignKey"),
            onDelete = ForeignKey.CASCADE
        )
    ),
    ignoredColumns = arrayOf("address")
)
data class MarkerEntity (
    var id : Int = 0,
    var personForeignKey : Int = 0,
    var subject: String = "",
    var content: String = "",
    @ColumnInfo(name = "LATITUDE") val lat: Double = 0.0,
    @ColumnInfo(name = "LONGITUDE")val lng: Double = 0.0,
    var writer: String = "",
    val address: String = ""
)
```
- @Entity에 한번에 설정하지 않고 각 변수에다 설정을 줄 수 있다
```kotlin
@Entity(tableName = "marker",
    inheritSuperIndices = true  
)
data class MarkerEntity (
    @PrimaryKey var id : Int = 0,
    @ForeignKey(
        entity = PersonEntity::class,
        parentColumns = arrayOf("personId"),
        childColumns = arrayOf("personForeignKey"),
        onDelete = ForeignKey.CASCADE
    )var personForeignKey : Int = 0,
    var subject: String = "",
    var content: String = "",
    @ColumnInfo(name = "LATITUDE", index = true) val lat: Double = 0.0,
    @ColumnInfo(name = "LONGITUDE", index = true) val lng: Double = 0.0,
    var writer: String = "",
    @Ignore val address: String = ""
)
```
- 위와 아래는 결과는 같지만 사용하기 편하고 보기 좋은 것을 선택하면 된다



##### @PrimaryKey
- Entity에는 반드시 1개 이상의 PrimaryKey가 존재해야한다
- 컬럼값이 1개이면 그 값이 PK로 설정해 주어야한다
- 또한 별개의 필드값으로 생성하고 autoGenerate = true로 설정하여 유니크한 아이디값을 자동으로 생성해주도록 한다

```kotlin
@Entity(tableName = "marker")
data class MarkerEntity (
    @PrimaryKey(autoGenerate = true) var id : Int = 0,
)
```


##### @ForignKey

- 여러 Entity를 정의하면서 다양한 조건을 설정할 수 있다
- @ForignKey 속성은 다음과 같다

  - entity : 참조할 부모 Entity를 의미합니다. ParentsEntity::class
  - parentColumns : 참조할 부모의 key값들
  - childColumns : 참조한 부모의 key값을 저장할 현재 Entity의 값들이며 parentColumns의 갯수와 동일해야 합니다.
  - onDelete : 참조하고 있는 부모 Entity가 삭제될 때 이뤄지는 행위를 정의합니다.(default: NO_ACTION. RESTRICT. SET_NULL. SET_DEFAULT. CASCADE)
  - onUpdate : 참조하고 있는 부모 Entity가 업데이트될 때 이뤄지는 행위를 정의합니다.(onDelete와 같음)
  - deferred : true로 설정할 경우 트랜잭션이 완료될 때까지 외래키의 제약 조건을 연기할 수 있습니다.
```kotlin
//자식 entity
@Entity(tableName = "marker2",
	foreignKeys = arrayOf(
        ForeignKey(
            entity = MarkerEntity::class,
            parentColumns = arrayOf("id"),
            childColumns = arrayOf("test_id"),
            onDelete = ForeignKey.CASCADE
        )
    )
)
data class MarkerEntity2 (
	@PrimaryKey(autoGenerate = true) var seq : Int = 0,
	var test_id : Int = 0,
)
```
```kotlin
//부모 entity
@Entity(tableName = "marker1")
data class MarkerEntity (
    @PrimaryKey(autoGenerate = true) var id : Int = 0,
)
```
- onDelete = CASCADE 옵션은 부모 클래스의 entity가 삭제될 경우 해당 값을 참조하는 다른 entity에서도 값이 제거된다
  - default : 부모 Entity가 삭제되거나 변경되어도 아무런 행위를 하지 않습니다.
  - RESTRICT : 참조하고 있는 부모의 key값을 삭제하거나 변경할 수 없게 합니다.
  - SET_NULL : 참조하고 있는 key값이 삭제되거나 변경되면 FK를 NULL로 초기화 시킵니다.
  - SET_DEFAULT : SET_NULL과 매우 유사합니다. 참조하고 있는 key값이 삭제되거나 변경되면 기본값으로 변경합니다.
  - CASCADE(삭제시) : 부모 Entity가 삭제될 경우 자식 Entity를 삭제합니다.
  - CASCADE(업데이트시) : 부모 Entity가 업데이트 될 경우에는 자식 Entity의 FK값을 새로운 값으로 변경 합니다.



##### @ColumnInfo
- 컬럼의 속성을 지정해 줄 수 있습니다
	- name : 데이터베이스에서의 컬럼명을 지정할 수 있습니다. 기본값으로 Entity 내에 있는 필드명이 사용됩니다.
	- typeAffinity : 컬럼의 타입을 지정할 수 있습니다.(default: UNDEFINED. TEXT. INTEGER. REAL. BLOB)
	- index : 컬럼들을 인덱싱할 수 있습니다.
	- collate : 컬럼값들의 정렬과 정렬 캐스트 작업을 정의힙니다.(default: UNSPECIFIED. BINARY. NOCASE. RTRIM. LOCALIZED. UNICODE)

```kotlin
@Entity(tableName = "marker")
data class MarkerEntity (
    @PrimaryKey(autoGenerate = true) var id : Int = 0,
    @ColumnInfo(
    	name = "LATITUDE",
        index = true,
        typeAffinitty = ColumnInfo.TEXT,
        collate = ColumnInfo.UNSPECIFIED
        ) val subject: String = "",
)
```
- typeAffinitty의 값은 다음과 같다
	- UNDEFINED(default) : 타입을 지정하지 않으며 입력되는 값에 따라 자동으로 저장됩니다.
	-TEXT : 문자열로 저장합니다.
	- INTEGER : Int값으로 저장합니다.
	- REAL : Double 또는 Float값으로 저장합니다.
	- BLOB : Binary값으로 저장합니다.


- collate 값은 다음과 같다
	- UNSPECIFIED(default) : 특별이 설정하지 않으나 BINARY처럼 동작합니다.
	- BINARY : 대소문자를 구분하여 정렬합니다.
	- NOCASE : 대소문자를 구분하지 않고 정렬합니다.
	- RTRIM : 앞뒤 공백을 제거하고 대소문자를 구분하여 정렬합니다.
	- LOCALIZED : 시스템의 현재 지역을 기반으로 정렬합니다.
	- UNICODE : 유니코드 데이터 정렬 알고리즘을 이용하여 정렬합니다.



##### @Ignore

- 별도의 값을 할당해주지 않으면 해당 컬럼의 데이터는 DB에 생성되지 않는다



## DAO

- DAO 클래스는 Room에서 SQL에 접근하기 위한 퀴리문을 작성하고 이를 수행한다
- DAO클래스는 인터페이스, 추상클래스로 구현되어야 한다
- 가장 큰 특징은 기존 SQL 쿼리상의 syntax오류를 결과를 받아야 알았지만, Room에서는 컴파일시에 발견하여 오류를 크게 줄일 수 있다.
- 또한 자동완성 기능을 이용할 수 있다

### @Insert
- DB에 데이터를 입력할 때 사용합니다
```kotlin
@Insert
fun insert(markerEntity: MarkerDataVO)
 
@Insert
fun insert(markerEntity01: MarkerDataVO, markerEntity02: MarkerDataVO)

@Insert
fun insert(markerEntity: List<MarkerDataVO>)

//가변인자로 값을 매핑할 수 있다
@Insert(onConflict = OnConflictStrategy.REPLACE)
fun insert(vararg markerEntity: MarkerDataVO)
```
- onConflict의 설정은 다음과 같다 (Update구문도 같습니다)
	- ABORT(default) : 충돌이 발생하면 트랜잭션을 롤백 시킵니다.
	- REPLACE : 충돌이 발생하면 기존데이터와 입력데이터를 교체합니다.
	- IGNORE : 충돌이 발생하면 기존데이터를 유지하고 입력데이터를 버립니다.

### @Update
- 데이터를 갱신할 때 사용됩니다
- 전달받은 매개변수의 PK값에 매칭되는 entity를 찾아 갱신합니다.

```kotlin
@Update
fun update(markerEntity: MarkerDataVO)
 
@Update
fun update(markerEntity01: MarkerDataVO, markerEntity02: MarkerDataVO)

@Update
fun update(markerEntity: List<MarkerDataVO>)

//가변인자로 값을 매핑할 수 있다
@Update(onConflict = OnConflictStrategy.REPLACE)
fun update(vararg markerEntity: MarkerDataVO)
```

### @Update
- 데이터를 삭제할 때 사용됩니다
- 전달받은 매개변수의 PK값에 매칭되는 entity를 찾아 갱신합니다.
```kotlin
@Delete
fun delete(markerEntity: MarkerDataVO)
 
@Delete
fun delete(markerEntity01: MarkerDataVO, markerEntity02: MarkerDataVO)

@Delete
fun delete(markerEntity: List<MarkerDataVO>)

//가변인자로 값을 매핑할 수 있다
@Delete(onConflict = OnConflictStrategy.REPLACE)
fun delete(vararg markerEntity: MarkerDataVO)
```

### Query
- 데이터를 선택하는 기능을 수행한다
- Annotation에 쿼리문을 작성하고 쿼리문 수행후 리턴값을 받도록 지정해준다
- 자동완성과 컴파일시 query문의 오류를 검사해준다
```kotlin
@Query("SELECT * FROM marker")
fun getAll() : List<MarkerDataVO>

@Query("SELECT * FROM marker WHERE seq = :seq")
fun getOne(seq : Int) : MarkerDataVO

@Query("SELECT * FROM marker WHERE synchronization = 'false'")
fun getAsyncList() :  List<MarkerDataVO>

@Query("SELECT * FROM marker WHERE seq > :minSeq")
fun getAsyncList(seq : Int) : Cursor
```
> 주의: Cursor API를 사용하여 작업하지 않는 것이 좋습니다. 행의 존재 여부 또는 행에 포함된 값을 보장하지 않기 때문입니다. 커서를 예상하는 코드 및 쉽게 리팩터링할 수 없는 코드가 이미 있는 경우에만 이 기능을 사용하세요.
## 예제
- DB처리는 반드시 RxJava, Coroutine, Thread를 이용해서 처리해야한다
- MainThread에서 처리하는 allowMainThreadQueries() 기능이 존재하지만 반드시 비동기처리 방식을 사용하는 것이 좋다
```kotlin
val data : List<MarkerDataVO> = .......
GlobalScope.launch(Dispatchers.IO) {
	val async01 : Deferred<unit> = async(Dispatchers.IO){
		markerDAO.insertMarkerList(data)
	}
    //데이터 리스트를 DB에 저장하는 것을 기다린 후
    //DAO에 getAll() 메소드를 이용하여 최신 데이터를 받아 Log창에 출력한다
	async01.await().let{
		val async02 : Deferred<List<MarkerDataVO>> = async(Dispatchers.IO){markerDAO.getAll()}
		for(data : MarkerData in async02.await()){
			println(data)
		}
	}
}
```

참고 :[https://developer.android.com/training/data-storage/room/index.html]( https://developer.android.com/training/data-storage/room/index.html)

[https://medium.com/@gus0000123/mvvm-aac-room%EC%82%AC%EC%9A%A9%EB%B2%95-1-%EA%B0%9C%EB%85%90%ED%8E%B8-59ad680ea6fe](https://medium.com/@gus0000123/mvvm-aac-room%EC%82%AC%EC%9A%A9%EB%B2%95-1-%EA%B0%9C%EB%85%90%ED%8E%B8-59ad680ea6fe)



## 추가

### TypeConverter

- 일반적으로 room 에서 entity에는 기본형(래퍼클래스)만을 취급한다.
- list, 객체를 저장할려고 하면 에러가 발생한다.
- 왜냐하면 성능과 메모리 상의 문제로 주 이유이다.
- 하지만 typeConverter를 이용하여 이러한 부분들을 접근해볼 수 있다.
- DB에 데이터를 저장하려고 할대 개발자가 원하는 타입(객체, 리스트, enum) 종류를 추가하고 싶다면 @TypeConverter를 사용하는 클래스를 만든다.

```kotlin
class DataConverters {
	@TypeConverter
	fun fromString(string: String): Date {
        return Day.values().first {it.value == value}
    }
    
	@TypeConverter
	fun fromDay(day: Day): String? {
        return Day.valueOf(day)
    }    
}
```

```kotlin
enum class Day {
    Sun, Mon, Tue, Wed, Thu, Fri, Sat,
}
```

- 이후 이를 사용하는 DB에 @TypeConventers을 추가한다.

```kotlin
@TypeConverters(DataConverters::class)
abstract fun Database: RoomDatabase() { ... }
```

