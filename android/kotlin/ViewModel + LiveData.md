## ViewModel
- ViewModel 클래스는 수명주기를 고려하여 UI관련 데이터를 저장 및 관리할 수 있도록 설계되었다.
- ViewModel은 activity, fragment에 자료가 제한되는 것을 방지한다.
- UI관련 데이터를 수명주기에 관계없이 보존할 수 있다.
- 화면 회전으로 activity와 fragment를 재구성하게 될 경우 일반적인 데이터는 초기화 되지만 ViewModel은 activity보다 긴 `LifeCycler`를 가지기 때문에 ViewModel을 이용하여 데이터를 재사용할 수 있다.

<div>
<img src="https://developer.android.com/images/topic/libraries/architecture/viewmodel-lifecycle.png?hl=ko" width="400">
</div>

- activity의 `onSaveInstanceState()`를 이용하여 데이터를 재사용할 수 있다.
- 그러나 복원할 데이터가 사용자 목록, 비트맵과 같은 대용량일 경우 적합하지 않다.

## LiveData

- `LiveData` 클래스는 수명주기를 인식한다.
- activity, fragment의 수명주기를 고려하여 작동된다.
- 수명주기는 `Observer` 클래스가 인식하여 데이터를 업데이트 한다.
- 수명주기를 인식하며 동작하기 때문에 `Observer`를 생성하고 사용하는데 해당 Context의 `LifeCycler`을 전달해줘야 한다.
- `Observer`클래스가 수명주기가 `STARTED`, `RESUMED`상태이면 LiveData는 `Observer`를 활성상태로 간주한다.

## ViewModel + LiveData와 안드로이드 구조에 대한 관계

- activity, fragment와 같은 UI 컨트롤러의 목적은 일반적으로 UI 데이터를 표시, 사용자 작업에 반응의 역할을 담당한다.
- 하지만 network, mDB 작업까지 할당하면 코드의 복잡성과 종속성이 커지고 테스트하고 유지보수에 어려워진다.
- UI 컨트롤러에서는 UI처리만 담당하는게 효율적이고 좋은 방법이다.
- 이를 ViewModel과 LiveData를 통해 UI로직과 비즈니스로직을 나누어 종속성을 줄이고 효율적으로 개선한다.
- 이와 관련된 안드로이드 구조에는 MVVM, Clean Architecture가 존재한다.

## 사용법

### ViewModel, LiveData 선언

- 일반적으로 `LiveData`인스턴스는 `ViewModel`클래스 내부 다음과 같이 이루워진다.

```kotlin
class TestViewModel : ViewModel() {
    val currentName : MutableLiveData<String> by lazy{
        MutableLiveData<String>()
    }
}
```

- `LiveData`, ` MutableLiveData`는 Collections을 구현한 `List`와 같은 객체를 비롯한 모든 데이터를 함께 사용할 수 있는 래퍼이다.

- 안드로이드 구조와의 관계에서 말한 것처럼 activity나 fragment가 과도한 작업을 할당하지 않게 하기 위해서 ViewModel에 LiveData로 데이터 상태를 유지시킬 수 있도록 한다.
- 또한 ViewModel이 LiveData를 사용하여 activity와 fragment와 분리하고 객체를 유지할 수 있게 한다. (ViewModel Scope가 길기 때문에)

### LiveData 객체 관찰

- 일반적으로 activity의 `onCreate()`메서드에 `LiveData` 객체 `Observer`를 정의하는데 적합한 장소이다.
  - activity와 fragment의 `onResume()`메소드에 정의할 경우 중복 호출되기 때문이다.
  - activity와 fragment의 active상태가 되는 즉시 표시할 데이터가 포함되기 위함이다.
    - `STARTED`상태가 되면 `LiveData`객체에서 최신값을 수신하기 때문

```kotlin
class NameActivity : AppCompatActivity() {

    private val model: TestViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
		
        //관찰자 객체 생성하기 내부에는 UI처리 로직
        val nameObserver = Observer<String> { newName ->
            nameTextView.text = newName
        }
        //viewModel에 존재하는 currentName인 liveData를 관찰한다.
        //메소드는 관찰자가 있는 해당 context의 LifeCycler(this)과 관찰자 객체
        model.currentName.observe(this, nameObserver)
        
        // 다음과 같이 한번에 정의 할 수도 있다.
        model.currentName.observe(this, Observer {
            nameTextView.text = newName
        })
    }
}
```

### LiveData 객체 업데이트

- `LiveDta`에는 저장된 데이터를 업데이트하는데 public 메소드가 없다.
- `LiveData`객체에 저장된 값을 수정하러면 `MutableLiveData`에 public인 `setValue()`, `postValue()` 메소드를 이용해야 한다.
- 일반적으로 `MutableLiveData`는 ViewModel에 사용되고 `LiveData`객체만 public으로 한다.
- 그래서 다음과같이 관찰자 관계를 설정한다.

```kotlin
class TestViewModel : ViewModel() {
	private val _currentName = MutableLiveData<String>()
	val currentName: LiveData<String>
        get() = _currentName
}
```

```kotlin
button.setOnClickListener {
    val anotherName = "John Doe"
    model.currentName.setValue(anotherName)
}
```

#### setValue(), postValue() 차이

- setValue(), postValue() 두 메소드 모두 LiveData의 데이터를 업데이트하는 메소드이다.
- 이를 사용하는 주체가 UI스레드일 경우는 차이가 없다.
- 하지만 UI스레드가 아닐경우 `setValue()`로 세팅한 값은 UI를 변경하지 못한다.
- `postValue()`로 세팅한 값은 해당 값을 UI스레드로 post해주기 때문에 UI스레드가 아니여도 UI를 변경할 수 있다.

## LiveData 병합

- `MediatorLiveData`는 `LiveData`의 서브클래스이다.
- `MediatorLiveData`클래스를 이용하여 여러 `LiveData`소스를 병합할 수 있다.
- `MediatorLiveData`객체의 관찰자는 원본 `LiveData` 소스 객체가 변경될때마다 트리거 된다.
- 즉 `LiveData`를 관찰하는 `MediatorLiveData`인 것이다.
- 네트워크, mDB를 업데이트하는 `LiveData`객체가 있다면 해당 값을 관찰하는 `MediatorLiveData`를 이용하여 UI를 업데이트 할 수 있다.

```kotlin
private val _searchHistory = MediatorLiveData<ArrayList<SearchHistory>>()
val searchHistory: LiveData<ArrayList<SearchHistory>>
	get() = _searchHistory

_searchHistory.addSource(getHistoryResult){
	//처리 로직
}
```

- `getHistoryResult`는 네트워크, mDB에서 처리된 `MutableLiveData`타입의 객체이다.
- 어떤 로직이 처리되어 `getHistoryResult`가 `setValue()`, `postValue()`러 처리되면 이를 `MediatorLiveData`타입인 `_searchHistory`가 이를 감지하여 로직을 처리할 수 있게 된다.

## 정리 및 추가

- ViewModel + LiveData를 이용하여 UI처리 로직과 데이터 처리(비즈니스) 로직을 분리시켜 종속성을 줄일 수 있게 되었다.

  - ViewModel내부에 android.*관련 라이브러리가 없어진다.

- ViewModel의 `LifeCycler`은 activity, fragment보다 길기 때문에 view를 참조해서는 안된다.

  - viewModel에는 `context`가 있으면 안된다.
  - 만약 ViewModel에서 `Room`을 사용하게 된다면 `context`가 필요한데 이때는 다음과 같이 `AndroidViewModel`를 사용한 `ViewModel`클래스를 생성한다.

  ```kotlin
  class MyViewModel(application: Application) : AndroidViewModel(application) {
      Room.databaseBuilder(application, myDatabase::class.java, "YOUR_DATABASE").build() 
      //viewModel contents
  }
  ```

  > DI를 이용한 방법도 존재

- Google에서는 하나의 ViewModel만을 사용하는 것을 권장하고 있다

  - 하나의 ViewModel이 여러 View를 처리한다.