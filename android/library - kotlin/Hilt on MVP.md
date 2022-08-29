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

## 의문점 - @Provides 만 써도 될거 같은데????

- hilt를 MVP에서 쓸 때 왜 View, Presenter를 왜 `@Binds`에 정의해서 사용하는 것일까?
- 사실 `@Binds`를 대신해서 `@Provides`로 다음과 같이 사용할 수 있다.

```kotlin
@InstallIn(ActivityComponent::class)
@Module
object MainActivityModule {

    @Provides
    fun bindActivity(impl: MainPresenter): MainContract.Presenter {
        return impl
    }
  
    @Provides
    fun bindActivity(activity: Activity): MainActivity {
        return activity as MainActivity
    }
}
```

- 실제 동작은 동일하고 문제 없어 보인다.
- 근데 왜 `@Binds`를 사용하는 걸까?
- 이를 알기 위해서는 hilt이전의 dagger의 히스토리에 대해 잠깐 알아 볼 필요가 있다.
- 사실 dagger 초창기에는 module이라는 개념이 없었다.
- 여러 개발자들은 연관된 것들 끼리 그룹화 시키고 싶었고, dagger2 개발자들이 module의 개념을 만들었다.
- 그럼에도 불구하고 `@Provides`가 있는 `@Module`에서 생성된 코드에 일부 오버헤드를 발생시켰고, `@Binds`가 이러한 부분들 해결하기 위해 소개되었다.
- 오버헤드가 무엇이고, 위에서 작성한 코드를 빌드시키고 생성되는 코드를 살펴보자
- **@Binds**

```kotlin
@Module
@InstallIn(ActivityComponent::class)
abstract class MainModule {
    @Binds
    abstract fun bindActivityView(view: MainActivity): MainContract.View

    @Binds
    abstract fun bindActivityPresenter(presenter: MainPresenter): MainContract.Presenter
}

@Module
@InstallIn(ActivityComponent::class)
object MainActivityModule {

    @Provides
    fun bindActivity(fragment: Activity): MainActivity {
        return fragment as MainActivity
    }
}
```

<img width="510" alt="스크린샷 2021-09-20 오후 6 46 16" src="https://user-images.githubusercontent.com/58923717/134004009-da31020f-2893-4d5f-9767-298992033a54.png">

- **@Provides**

```kotlin
@Module
@InstallIn(ActivityComponent::class)
object MainActivityModule {

    @Provides
    fun bindActivity(fragment: Activity): MainActivity {
        return fragment as MainActivity
    }
    
    @Provides
    fun bindActivityView(view: MainActivity): MainContract.View {
        return view
    }

    @Provides
    fun bindPresenter(presenter: MainPresenter) : MainContract.Presenter {
        return presenter
    }
}

```

<img width="498" alt="스크린샷 2021-09-20 오후 9 50 07" src="https://user-images.githubusercontent.com/58923717/134005080-128d5b49-544b-419e-b619-cc9c16bc57f2.png">

- @Provides를 사용할때 `MainActivityModule_BindXXXXFactory`라는 클래스가 생성되는 차이를 확인할 수 있다.
- 그러면 BindXXXXFactory는 어떻게 되어 있을까?

<img width="1264" alt="스크린샷 2021-09-20 오후 9 52 13" src="https://user-images.githubusercontent.com/58923717/134005344-da0ecdad-5d20-4ac7-8ad6-cdc4f74fdde2.png">

- 만약 모듈에 1개 이상의 모듈이 있다면 각 모듈에서는 factory class를 `@Provides` 어노테이션 만큼 생성할 것이다.
- 그리고 해당 factory클래스를 사용하는 @Provides와 @Binds를 사용하는 `HiltComponents class`를 확인하면 다음과 같이 diff가 발생한다.

<img width="1660" alt="스크린샷 2021-09-20 오후 10 04 55" src="https://user-images.githubusercontent.com/58923717/134007043-f7c53a8a-c0e8-4557-998b-f352e133fed6.png">

- 안드로이드 패키지에서 하나의 View에 Presenter가 결합한 경우 위와 같은 코드 diff를 보여주는데 만약 보다 큰 프로젝트에서 @Provides를 지속적으로 사용하면 더 많은 코드가 늘어나게 된다.

- 그리고 dagger에서는 코드 diff가 더 심해 약 40%정도의 차이가 있었지만 hilt에서는 보다 줄어들었다.
- 위 코드를 통해 Provide와 Binds의 코드 흐름을 알 수 있다.
- Provides를 먼저 확인해보자.

```java
private MainActivity mainActivity() {                                                
  return MainActivityModule_BindActivityFactory.bindActivity(activity);              
}                                                                                    
                                                                                     
private MainContract.View view() {                                                   
  return MainActivityModule_BindActivityViewFactory.bindActivityView(mainActivity());
}                                                                                    
                                                                                     
private MainPresenter mainPresenter() {                                              
  return new MainPresenter(view());                                                  
}                                                                                    
```

- MainPresenter를 반환하기 위해서 각각의 factory class에 접근하는 과정을 확인할 수 있다.
- 반면 Binds를 사용할 경우 다음과 같이 된다.

```java
private MainActivity mainActivity() {                                  
  return MainActivityModule_BindActivityFactory.bindActivity(activity);
}                                                                      
                                                                       
private MainPresenter mainPresenter() {                                
  return new MainPresenter(mainActivity());                            
}                                                                      
```

- 보다 간결한 것을 확인할 수 있다.

### 결론

- 결과적으로 `@Binds`는 `@Provides` 보다 **객체의 생성을 줄이고 작업의 흐름을 줄일 수 있다.**
- 그러면 **모든 의존성 주입을 `@Binds`로 하면될까? 그건 아니다.**
- @Binds 메서드에는 리턴 타입으로 지정할 수 있는 매개변수가 하나만 있어야 한다.

> @Binds 내부 코드를 보면 보다 정확히 확인할 수 있다.

