## Room (mobileDB)

- 구글에서 만든 공식 ORM이다
- 많은 양에 데이터를 처리하는데 로컬에 데이터가 있다면 큰 이점으로 작용한다
- 오프라인으로 작업이 가능하며, 캐싱할 수 있기 때문이다
- 또한 동기화를 통해 데이터를 데이터의 변경사항을 처리할 수 있다
- 구글에서는 기존의 SQLite대신 Room을 적극적으로 권장하고 있다
- Room은 SQLite에 대한 추상화 레이어를 제공하여 원활한 데이터베이스 액세스를 지원하는 동시에 SQLite를 완벽히 활용합니다.
- SQLite를 이용하기 위해 Helper클래스를 만들어 사용했지만, Room은 Database, DAO, Entity를 이용한다

### 구성요소
#### Database
- Database에 접근하는 DAO를 관리한다
- @Database 어노테이션으로 Entity목록을 작성해야한다
#### DAO
- Database에 접근하는 메소드를 포함한다
- 마찬가지로 어노테이션에 쿼리문을 작성한다
- 또한 LiveData, Observable query도 이용가능하다
#### Entity
- 테이블을 의미한다

![room아키텍처](image/room_architecture.JPG)

### gradle

```
dependencies {
	def room_version = "2.2.5"

	implementation "androidx.room:room-runtime:$room_version"
	annotationProcessor "androidx.room:room-compiler:$room_version" // For 	Kotlin use kapt instead of annotationProcessor

	// optional - Kotlin Extensions and Coroutines support for Room
	implementation "androidx.room:room-ktx:$room_version"

	// optional - RxJava support for Room
	implementation "androidx.room:room-rxjava2:$room_version"

	// optional - Guava support for Room, including Optional and ListenableFuture
	implementation "androidx.room:room-guava:$room_version"

	// Test helpers
	testImplementation "androidx.room:room-testing:$room_version"
}
```

> **참고:** Kotlin 기반 앱에서는 `annotationProcessor` 대신 `kapt`를 사용해야 합니다. 또한 `kotlin-kapt` 플러그인도 추가해야 합니다.

```
apply plugin: 'kotlin-android-extensions'
apply plugin: 'kotlin-kapt'	//참고
android {
    compileSdkVersion 30
```



### Database
- 구글문서에 다음 설명이 있다
> 참고: 앱이 단일 프로세스에서 실행되면 AppDatabase 객체를 인스턴스화할 때 싱글톤 디자인 패턴을 따라야 합니다. 각 RoomDatabase 인스턴스는 리소스를 상당히 많이 소비합니다. 그리고 단일 프로세스 내에서 여러 인스턴스에 액세스할 필요가 거의 없습니다.

- RoomDatabase를 만드는 과정은 많은 리소스를 필요하기에 Singletone패턴을 이용하는 것을 권장한다
- @Database 어노테이션에 Entity를 배열로 입력하여 다수의 테이블을 관리하게 할 수 있다
- markerDAO는 RoomDatabase에서 관리 권한을 위함하여 직접적으로 접근을 막아야 한다
```kotlin
@Database(entities = [MarkerDataVO::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun markerDAO(): MarkerDAO

    companion object {
        private val DB_NAME = "marker-db"
        private var instance: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return instance ?: synchronized(this) {
                instance ?: buildDatabase(context)
            }
        }

        private fun buildDatabase(context: Context): AppDatabase {
            return Room.databaseBuilder(context.applicationContext, AppDatabase::class.java, DB_NAME)
                .addCallback(object : RoomDatabase.Callback() {
                    override fun onCreate(db: SupportSQLiteDatabase) {
                        super.onCreate(db)
                    }
                }).build()
        }
    }
}
```

### DAO
- interface, abstract class 로 작성해야한다
- 어노테이션을 통해 query문을 작성해야한다
- query문은 자동완성을 지원한다

```kotlin
@Dao
interface MarkerDAO{
    @Query("SELECT * FROM marker")
     fun getAll() : List<MarkerDataVO>

    @Insert
     fun insert(markerEntity: MarkerDataVO)

    @Delete
     fun delete(markerEntity: MarkerDataVO)

}
```

### Entity
- Entity(table)의 이름을 따로 지정하지 않으면 default값으로 클래스명으로 지정된다
- 따로 대소문자를 구분하지 않는다
- 컬럼값도 동일하다
```kotlin
@Entity
data class MarkerEntity (
    var id : Int = 0,
    var subject: String = "",
    var content: String = "",
)
```

참고 :[https://developer.android.com/training/data-storage/room/index.html]( https://developer.android.com/training/data-storage/room/index.html)

[[https://medium.com/@gus0000123/mvvm-aac-room%EC%82%AC%EC%9A%A9%EB%B2%95-1-%EA%B0%9C%EB%85%90%ED%8E%B8-59ad680ea6fe](https://medium.com/@gus0000123/mvvm-aac-room사용법-1-개념편-59ad680ea6fe)]