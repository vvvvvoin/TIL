# MVP - Android

- Model, View, Presenter로 구성된 디자인 패턴이며 구조이다.
- android의 구조를 MVC패턴으로 보면 activity/fragment에서 view와 controller의 기능을 동시에 담당하게 된다.
- MVC패턴으로 안드로이드 구조를 만들다보면 view와 model이 직접적으로 접근하게 되고 의존성이 높아지게 되고 결과적으로 유지보수에 어려움이 생긴다.

> 중간에 위치한 controller가 view와 함께 사용되기 떄문이다.

- 이러한 문제를 보완시킨것이 MVP, MVVM패턴들이 존재한다.

## MVP?

- MVP패턴은 기존 MVC에서 view와 controller가 한 번에 사용되어 문제가 존재했다면 MVP에서는 controller를 presenter를 두어 view와 model중간에서 인터페이스 역할을 수행하게 된다.
- 결과적으로 인터페이스로 view와 model이 직접 접근하는 일이 없어지고 의존성 문제를 해결할 수 있다.

## View, Presenter

### BaseContract

- presenter가 인터페이스 역할을 수행한다.
- view가 인터페이스를 통해 model에 접근할때에 여러 activity/fragment에서 공통적으로 사용되는 기능을 정의한다.

```kotlin
interface BaseContract {
    interface View {
        //view에서 실행되는 공통적인 기능을 추가할 수 있다.
    }

    interface Presenter<T> {
        //view와 presenter가 서로 연결되고 어떤 view가 연결되고
        //반환하는 공통 메서드를 정의한다.
        fun setView(view: T)
        fun detachView()
    }
}
```

### MyContract

- BaseConstract를 구현한 contract를 정의한다.
- Presenter에서는 `setView`, `detachView`를 해당 Contract에 맞게 구현되었다.

```kotlin
interface HomeContract {
    interface View : BaseContract.View {
        fun updateList(list : ArrayList<String>)
    }

    interface Presenter : BaseContract.Presenter<View> {
        override fun setView(view: View)
        override fun detachView()
        fun searchWithQuery(query : String)
    }
}
```

### Presenter

- `HomeContract.Presenter`를 구현한 HomePresenter를 정의한다.
- `searchWithQuery`메서드에서는 model과 관련하여 remote, local과 관련된 데이터를 처리한 데이터를 `updateList`메서드를 호출하여 View가 UI를 갱신할 수 있도록 한다.

```kotlin
class HomePresenter() : HomeContract.Presenter {

    private var view : HomeContract.View? = null

    override fun setView(view: HomeContract.View) {
        this.view = view
    }

    override fun detachView() {
        this.view = null
    }

    override fun searchWithQuery(query: String) {
        //remote, local과 관련된 데이터를 처리 후 view의 UI관련 로직 수행
        view?.updateList(list)
    }
}
```

### View - Fragment

- fragment에서 `HomeContract.View`를 구현한다.
- `searchWithQuery`메서드를 이용하여 Presenter가 model를 통해 데이터를 받아올 수 있도록 한다.

```kotlin
class HomeFragment : Fragment(), HomeContract.View {
    private lateinit var mPresenter: HomeContract.Presenter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        mPresenter = HomePresenter(myRepository)
        mPresenter.setView(this)
        
        mPresenter.searchWithQuery("someData")
    }
    
    override fun updateList(list : ArrayList<String>) {
        //받아온 ArrayList타입 데이터를 UI데이터 갱신
    }
}
```

- 결과적으로 view와 model이 직접 접근하는 로직을 presenter 인터페이스를 사용함으로써 의존성 문제를 줄일 수 있다.
- model과 관련된 로직은 Repository를 사용하거나 presenter내부에 API, Local과 관련된 모듈을 생성해서 사용할 수 있다.
- 혹은 view에서 mPresenter를 생성할 때 생성자에 API, Local과 관련된 객체를 넘겨서 사용할 수도 있다.

## Model

- model에서 비지니스, 데이터 로직을처리하기 위해서 model 모듈이 필요하다.
- 내부에서 싱글톤으로 생성된 model을 사용하거나 의존성 주입을 통해 구현할 수 있다.

### Model - init

- presenter에서 model을 다음과 같이 사용할 수 있다.

```kotlin
class HomePresenter() : HomeContract.Presenter {

    private var view : HomeContract.View? = null
    private val compositeDisposable = CompositeDisposable()
    
    private lateinit var api : MyApi
    
    init {
        this.api = MyApiProvider.getInstance()
    }
    
    override fun setView(view: HomeContract.View) {
        this.view = view
    }

    override fun detachView() {
        this.view = null
        compositeDisposable.clear()
    }

    override fun searchWithQuery(query: String) {
       api.searchWithQuery(query)
        .subscribeOn(Schedulers.io())
        .observeOn(AndroidSchedulers.mainThread())
        .subscribe({
          view?.updateList(list)  
        },{
           //error 처리
        }).addTo(compositeDisposable)
    }
}
```

- 멤버변수로 `compositeDisposable`, `API`를 선언해주었다.
- 그리고 init을 (혹은 생성자로) 통해 api를 정의해준다.
- 그리고 기존 `searchWithQuery` 메서드 내부에 api를 호출하고 Rx를 이용하여 비동기 처리하였다.
- 그리고 해당 결과를 받는 `subscribe`내부에 UI처리 메서드를 호출한다.
- `subscribe`를 함으로써 Rx의 반환값인 `Disposable`이 되는데 이를 멤버변수 `compositeDisposable`에 넣어주고 view가 `destroy`될 때 `detachView()`를 실행하여 `compositeDisposable.clear()`를 수행할 수 있도록 한다.

### Model - DI

- view에서 presenter를 생성할때 의존성을 주입시켜 다음과 같이 구현할 수 있다.

```kotlin
class HomePresenter(private val api : MyApi) : HomeContract.Presenter {

    private var view : HomeContract.View? = null
    
    override fun setView(view: HomeContract.View) {
        this.view = view
    }

}
```

- 이를 좀 더 확장시켜 Koin이나 Dagger를 통해 의존성 주입을 수행할 수도 있다.

