## MVVM

## 개요

### MVC는 ?

- 안드로이드 관점에서 MVC 패턴을 적용하면 activity/fragment에 view와 controller가 포함된다.
- 그리고 model에서 비즈니스 로직이 처리된다.
- 하지만 로직을 처리하는데 있어 view와 model간에 의존성이 존재하게 되고 프로젝트 규모가 커질수록 복잡해지고 유리보수에 어려워지는 단점이 있다.

### MVP는 ?

- MVP패턴은 기존 MVC에서 나타난 model과 view간에 종속성 문제를 보완한다.
- presenter라는 인터페이스를 두어 model과 view가 서로 직접연결되지 않게 하여 종속문제를 보완한다.
- 하지만 프로젝트 규모가 커질수록 view와 presenter간에 의존성이 커지게 된다.

### 왜 MVVM인가?

- MVC, MVP패턴에는 view의 의존성 문제가 공통적으로 존재했다.
- 이는 프로젝트를 진행하는데 있어 유지보수와 테스트를 어렵게 만든다.
- 이러한 문제를 `Android Jetpack`에서 제공하는 `Android AC`와 `MVVM패턴`을 이용하여 의존성 문제를 해결할 수 있다.

### MVVM

- MVVM패턴도 기존 패턴과 마찬가지로 view와 model이 있고 기존 역할과 동일하다.
- 하지만 ViewModel이 새롭게 추가되었는데 니는 기존 처럼 view의 요청을 받아 model의 변경된 데이터를 직접 view에 전달하지 않는다.
  - `직접 데이터를 전달하지 않는다`의 의미는 ViewModel에서 view와 관련된(android.*) 라이브러리를 사용하지 않는다는 것을 말한다.
- Androd AC의 ViewModel, Livedata 라이브러리를 통해 observer패턴으로 변경된 데이터를 전달한다.

- - observer패턴은 안드로이드 관점에서 말하면 view가 요청을 ViewModel에 요청하면 ViewModel은 이를 처리하고 직접알려주지 않고 값만(mutable type LiveData) 변경한다.
  - 그리고 view가 그 값(immutable type LiveData)을 관찰하고 있고 변경이 되면 해당 값을 받아 처리하게 된다.

<div><img src="https://developer.android.com/topic/libraries/architecture/images/final-architecture.png?hl=ko"></div>

- 일반적인 MVVM패턴의 다이어그램이고 각 구성요소가 한 수준 아래의 구성요소에만 종속되는 것을 볼 수 있다.
- 이러한 구조는 일관되고 좋은 사용자 환경을 제공할 수 있게 해준다.

## 환경

### 버전

- Android Studio 4.1.1

### dependency

```groovy
//gson
implementation 'com.google.code.gson:gson:2.8.6'

//retrofit
implementation 'com.squareup.retrofit2:retrofit:2.8.1'
implementation 'com.squareup.retrofit2:converter-gson:2.8.1'
implementation 'com.squareup.retrofit2:adapter-rxjava2:2.8.1'

//Rx
implementation 'io.reactivex.rxjava2:rxandroid:2.1.1'
implementation 'io.reactivex.rxjava2:rxjava:2.2.13'
implementation 'io.reactivex.rxjava2:rxkotlin:2.4.0'

// OkHttp3
implementation 'com.squareup.okhttp3:okhttp:4.2.1'
implementation 'com.squareup.okhttp3:logging-interceptor:4.2.1'
implementation 'com.squareup.okhttp3:okhttp-urlconnection:4.0.1'

// koin
implementation "org.koin:koin-androidx-scope:1.0.2"
implementation "org.koin:koin-androidx-viewmodel:1.0.2"
testImplementation 'org.koin:koin-test:1.0.1'

implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:2.3.0"
implementation "androidx.lifecycle:lifecycle-runtime-ktx:2.3.0"
implementation "androidx.lifecycle:lifecycle-livedata-ktx:2.3.0"
```

### AndroidManifest.xml

```xml
<uses-permission android:name="android.permission.INTERNET"/>
```

## 본문

### 사용자 인터페이스

#### BaseViewModel

- ViewModel를 구현한 `BaseViewModel` 추상클래스를 다음과 같이 만든다.

```kotlin
abstract class BaseViewModel : ViewModel() {
    protected val _error = MediatorLiveData<Event<String>>()
    val error: LiveData<Event<String>>
        get() = _error

    private val disposable = CompositeDisposable()

    operator fun invoke(disposable: Disposable) {
        this.disposable.add(disposable)
    }

    override fun onCleared() {
        disposable.clear()
        super.onCleared()
    }
}
```

- `BaseViewModel`을 구현한 클래스에서 Rx를 이용하여 비동기 처리를 한다.
- 이때 비동기 처리를 오퍼레이터 오버로딩으로 `CompositeDisposable` 에 추가하고 ViewModel이 제거될때 함게 clear시켜준다.

> _error의 MediatorLiveData 타입 : [TIL/ViewModel + LiveData.md](https://github.com/vvvvvoin/TIL/blob/master/android/kotlin/ViewModel %2B LiveData.md#livedata-병합)

#### ViewModel

- `BaseViewModel`을 구현한 MyViewModel 클래스

```kotlin
class MyViewModel() : BaseViewModel() {

    private val _personData = MutableLiveData<List<Person>>()
    val personData: LiveData<List<Person>>
        get() = _personData
}
```

- MyViewModel에서 사용되는 disposable객체는 자동적으로 `CompositeDisposable` 에 추가된다.

#### Activity

- 추가된 LiveData타입의 personData 변수를 view에서 참조할 수 있게 만들어야 한다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<layout  xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">

    <data>
        <variable
            name="viewModel"
            type="com.example.mvvm_template.viewModel.MyViewModel" />

    </data>

    <!-- ui -->>

</layout>
```

```kotlin
class MainActivity : AppCompatActivity() {

    private val myViewModel: MyViewModel by viewModel()
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = DataBindingUtil.setContentView<ActivityMainBinding>(this, R.layout.activity_main)
            .apply {
                viewModel = myViewModel
                lifecycleOwner = this@MainActivity
            }
    }
}
```

- DataBinding으로 view의 lifecycler에 맞게 데이터를 업데이트 할 수 있도록 해준다.

### 데이터 가져오기

#### Remote DataSource

- Retrofit을 이용하여 데이터를 접근할 수 있도록 한다.

```kotlin
interface MyAPIService {
    @GET("/")
    fun search(
        @Header("Authorization") auth : String,
        @Query("query") query: String,
    ) : Single<List<Person>>
}
```

- 해당 인터페이스는 OkHttp3를 이용하여 클라이언트와 함께 retrofit객체를 생성하여 Repository에 의존성을 주입할 것이다.

#### Data Model

- `Person` 데이터 클래스

```kotlin
data class Person(
    val name : String,
    var age : Int,
    var sex : Int
)
```

#### Repository

- Repositrory를 만들어 비즈니스 로직이 처리될 수 있도록 해준다.

```kotlin
class RemoteRepository(private val myApi: MyAPIService) {		//의존성 주입

    fun search(argument1 : String, argument2 : String): Single<List<Person>> {
        return myApi.search(argument1, argument2)
            .subscribeOn(Schedulers.io())
            .observeOn(AndroidSchedulers.mainThread())
    }
}
```

- `search`메서드의 반환은 `Single`타입의 `Observable`이고 이를 ViewModel에서 subscribe해서 disposable객체로 만들 것이다.

#### ViewModel

- ViewModel에 repository 의존성 주입과 `search`메서드를 subscribe해준다.

```kotlin
class MyViewModel(
    private val remoteRepository: RemoteRepository		//의존성 주입
) : BaseViewModel() {

    private val _personData = MutableLiveData<List<Person>>()
    val personData: LiveData<List<Person>>
        get() = _personData

    fun search(argument1: String, argument2: String) {
        remoteRepository.search(argument1, argument2).subscribe({		//CompositeDisposable에 add될 것이다.
            _personData.value = it.data!!
        }, {
            callNetworkError()
        })
    }

    private fun callNetworkError() {
        _error.value = Event("network")		//baseViewModel의 _error
    }
}
```

> Event 객체 : [TIL/Event Wrapper클래스로 ViewModel, LiveData 이슈 해결하기.md](https://github.com/vvvvvoin/TIL/blob/master/android/kotlin/Event Wrapper클래스로 ViewModel%2C LiveData 이슈 해결하기.md)

#### XML

- activity_main.xml에서도 ViewModel에 사용된 `search`메서드를 사용할 수 있게 만든다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">

    <data>

        <variable
            name="viewModel"
            type="com.example.mvvm_template.viewModel.MyViewModel" />

    </data>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        tools:context=".view.ui.MainActivity">

        <Button
            android:id="@+id/button"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:onClick='@{() -> viewModel.search("testValue1", "testValue2")}'
            android:text="Button"
            android:layout_gravity="center"/>

        <androidx.recyclerview.widget.RecyclerView
            android:id="@+id/recyclerView"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:layout_marginHorizontal="10dp"
            app:item="@{viewModel.personData}"
            app:layoutManager="androidx.recyclerview.widget.LinearLayoutManager"
            tools:listitem="@layout/person_item" />


    </LinearLayout>
</layout>
```

- 버튼클릭시 search메서드가 실행된고 list타입의 person데이터를 받아오게 된다.
- 받아온 데이터를 RecyclerView에 바인딩 시켜주게 된다.

#### BindingAdapter

- attribute `app:item`에 들어온 데이터를 처리할 수 있도록 해준다.

```kotlin
@BindingAdapter("item")
fun setList(
    recyclerView: RecyclerView,
    item: List<Person>?
){
    val personAdapter: PersonListAdapter	//참조 변수선언
    if(recyclerView.adapter == null){
        return
    }else{
        personAdapter = recyclerView.adapter as PersonListAdapter
    }

    item?.let {
        personAdapter.list = it as ArrayList	//어탭터에서 다루는 list를 변경
        personAdapter.notifyDataSetChanged()	
    }
}
```

> DataBinding 주의사항1 : [TIL/DataBinding.md](https://github.com/vvvvvoin/TIL/blob/master/android/kotlin/DataBinding.md#바인딩-어탭터-주의사항)
>
> DataBinding 주의사항2 : [TIL/DataBinding.md](https://github.com/vvvvvoin/TIL/blob/master/android/kotlin/DataBinding.md#바인딩-어탭터-주의사항-1)

#### MainActivity

- 추가된 recylcerView와 observer를 초기화 시켜준다.

```kotlin
class MainActivity : AppCompatActivity() {

    private val myViewModel: MyViewModel by viewModel()
    private lateinit var binding: ActivityMainBinding

    private val personListAdapter: PersonListAdapter by lazy {	//어탭터 객체 초기화
        PersonListAdapter()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = DataBindingUtil.setContentView<ActivityMainBinding>(this, R.layout.activity_main)
            .apply {
                viewModel = myViewModel
                lifecycleOwner = this@MainActivity
            }

        binding.recyclerView.apply {	//recylcerView초기화
            adapter = personListAdapter
            setHasFixedSize(true)
        }
        
        initObserver()
    }

    private fun initObserver() {
        myViewModel.error.observe(this, EventObserver{
            Toast.makeText(this, "네트워크 에러 발생", Toast.LENGTH_LONG).show()
        })
    }
}
```

#### Adapter

- RecylcerView Adapter도 바인딩할 수 있도록 만들어 준다.

```kotlin
class PersonListAdapter : RecyclerView.Adapter<PersonListAdapter.ItemHolder>() {

    var list = ArrayList<Person>()		//바인딩 어탭터에서 변경하게 되는 변수

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        ItemHolder(PersonItemBinding.inflate(LayoutInflater.from(parent.context), parent, false))

    override fun onBindViewHolder(holder: ItemHolder, position: Int) {
        holder.bind(list[position])
    }

    override fun getItemCount(): Int {
        return list.size
    }

    class ItemHolder(private val binding: PersonItemBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(item : Person) {
            binding.item = item
        }
    }
}
```

- recylcerView item의 xml도 정의해준다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">

    <data>
        <variable
            name="item"
            type="com.example.mvvm_template.model.dataModel.Person" />
    </data>

    <LinearLayout
        android:id="@+id/search_item_layout"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_margin="10dp"
        android:clickable="true"
        android:focusable="true"
        android:orientation="horizontal">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_gravity="center"
            android:orientation="vertical">

            <TextView
                android:id="@+id/book_name"
                android:layout_width="match_parent"
                android:layout_height="20dp"
                android:text="@{item.name}"
                android:textColor="#000000"
                android:textSize="10sp"
                android:textStyle="bold"
                tools:text="NAME"/>

            <TextView
                android:id="@+id/book_contents"
                android:layout_width="match_parent"
                android:layout_height="20dp"
                android:text="@{item.age}"
                android:textColor="#000000"
                android:textSize="10sp"
                android:textStyle="bold"
                tools:text="AGE"/>

            <TextView
                android:id="@+id/book_publisher"
                android:layout_width="match_parent"
                android:layout_height="20dp"
                android:layout_marginRight="10dp"
                android:text="@{item.sex}"
                android:textColor="#000000"
                android:textSize="10sp"
                android:textStyle="bold"
                tools:text="SEX"/>
        </LinearLayout>
    </LinearLayout>
</layout>
```

> 참조 : [vvvvvoin/MVVM-Template: MVVM-Template](https://github.com/vvvvvoin/MVVM-Template)

## 주의사항

### ViewModel에서 View를 왜 참조 하지 않을까?

- 기본적으로 ViewModel은 Activity/Fragment보다 다음과 같이 생명주기가 길다.

<div><img src="https://developer.android.com/images/topic/libraries/architecture/viewmodel-lifecycle.png?hl=ko"></div>

- Activity/Fragment가 destroy되고 다시 recreate되도 기존 ViewModel을 사용하게 된다.
- 만약 destroyed된 Activity/Fragment를 참조하면 메모리릭이 발생하거나 잘못된 참조로 에러가 발생하게 될 것이다.
- 그렇기 때문에 View뿐만 아니라 Activity/Fragment의 context를 참조하는 다른 클래스도 참조하면 안된다.

> ViewModel에서 mDB를 사용할때는 context가 필요한데 이때는 AndroidViewModel를 구현한 ViewModel를 사용하면된다.

### ViewModel안에 Android와 관련된 라이브러리가 있어도 될까?

- ViewModel에서는 Android와 관련된 라이브러리를 최대한 제거하는 방향으로 코드를 작성해야 한다.
- 관련된 라이브러리가 존재한다면 종속성 문제와 모듈화에 영향을 주게 된다.

### Activity/Framgent는 여러 개의 ViewModel을 가져도 될까?

- 일반적으로 하나의 ViewModel를 갖는 것을 권장하고 있다.
- 여러 ViewModel을 사용할 수는 있지만 여러 View에 여러 ViewModel이 존재한다면 프로젝트가 복잡해질 것이다.

> 참조 : [MVVM Anti Pattern (gangnamunni.com)](https://blog.gangnamunni.com/post/mvvm_anti_pattern/)