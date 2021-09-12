# Hilt on MVP

## 사용법

### Applicatoin

```kotlin
@HiltAndroidApp
class ExampleApplication : Application() { ... }
```

- Hilt가 Application 클래스에 `@HiltAndroidApp`이 설정되면 애플리케이션 구성요소를 사용할 수 있게 되고 Hilt가 `@AndroidEntryPoint` 어노테이션으로 다른 클래스에 종속성을 제공할 수 있다.
- 그리고  `@HiltAndroidApp`이 적용된 클래스를 어플리케이션 컨테이라 하며 이는 앱의 생명주기와 관련지어 진다.
- 이는 앱의 상위 구성요소이므로 다른 구성요소는 이 상위 구성요소에서 제공하는 종속 항목에 액세스할 수 있습니다.

### Android 클래스 종속성 제공

-  `@HiltAndroidApp` 를 hilt에 적용하면 안드로이드 클래스에 종속성을 제공할 준비가 된거다.
- 안드로이드 클래스는 다음을 의미한다.
  - Application, Activity, Fragment, Service, BroadcastReceiver, View
- 안드로이드 클래스에서 `@AndroidEntryPoint` 을 이용하여 hilt의 구성요소를 생성한다.
-  Android 클래스에 `@AndroidEntryPoint` 설정해주면 해당 클래스에 종속된 Android 클래스에도 어노테이션을 추가해주어야 한다.
- 만약, Hilt가 주입한 클래스는 베이스 클래스, 추상클래스가 있는 경우 추상 클래스에 `@AndroidEntryPoint`는 필요 없다.

- 구성요소 계층은 다음과 같다.

<img src="https://developer.android.com/images/training/dependency-injection/hilt-hierarchy.svg?hl=ko" />

- 계층에서 나타나 있듯이 상위 클래스에서 종속 항목을 받을 수 있다.
- 구성요소에서 종속된 항목을 가져오기 위해서는 `@inject`를 사용한다.

```kotlin
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {

  @Inject lateinit var presenter: MainContract.Presenter
  ...
}
```

- 클래스의 생성자에서 `@Inject` 주석을 사용하여 클래스의 인스턴스를 제공하는 방법을 Hilt에 알려줍니다.


```kotlin
class MainPresenter @Inject constructor(
    private val view: MainContract.View
) : MainContract.Presenter {

	/../

}
```

- 필드 삽입을 실행하려면 Hilt가 해당 구성요소에서 필요한 종속 항목의 인스턴스를 제공하는 방법을 알아야 한다.
- 결합에는 특정 유형의 인스턴스를 종속 항목으로 제공하는 데 필요한 정보가 포함된다.
- 그렇다면 MVP패턴에서 힐트가 해당 인터페이스와 결합, 구현한 인스턴스가 무엇인지 찾아야하는데 알 수가 없다.
- 그래서 Hilt 모듈 내에 `@Binds`로 주석이 지정된 추상 함수를 생성하여 Hilt에 결합 정보를 제공합니다.

```kotlin
@InstallIn(ActivityComponent::class)
@Module
abstract class MainModule {

    @Binds
    abstract fun bindPresenter(impl: MainPresenter): MainContract.Presenter

}
```

- `@Binds`는 다음 정보를 제공한다.
  - 함수 반환 유형은 함수가 어떤 인터페이스의 인스턴스를 제공하는지 작성한다.
  - 함수 매개변수에는 해당 인터페이스를 구현한 실제 객체를 작성해준다.

> "MainContract.View와 결합한 객체가 MainActivity 이다" 라는 것을 힐트가 알 수 있게 해준다.

- 그리고 MVP패턴에서는 Presenter 생성자에 Contract.View가 들어가고 이는 인터페이스이다.
- 마찬가지로 같은 모듈에서 해당 바인딩을 다음과 같이 제공해야한다.

```kotlin
@InstallIn(ActivityComponent::class)
@Module
abstract class MainModule {

    @Binds
    abstract fun bindActivity(activity: MainActivity): MainContract.View

    @Binds
    abstract fun bindPresenter(impl: MainPresenter): MainContract.Presenter

}
```

- 같은 이유로 presenter에서는 초기화 할 MainActivity 와 결합한 인스턴스의 종속된 항목이 무엇인지 제공해줘야 한다. 

```kotlin
@InstallIn(ActivityComponent::class)
@Module
object MainActivityModule {

    @Provides
    fun bindActivity(activity: Activity): MainActivity {
        return activity as MainActivity
    }
}
```

- `@Provides`는 다음 정보를 제공한다.
  - 함수 반환 유형은 함수가 어떤 유형의 인스턴스를 제공하는지 Hilt에 알려준다.
  - 함수 매개변수는 해당 유형의 종속 항목을 Hilt에 알려준다.
  - 함수 본문은 해당 유형의 인스턴스를 제공하는 방법을 Hilt에 알려준다.
  - Hilt는 해당 유형의 인스턴스를 제공해야 할 때마다 함수 본문을 실행한다.



