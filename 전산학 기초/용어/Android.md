### ViewModel

- viewModel은 activity나 fragment에 자료가 제한되는 것을 방지하고 UI관련 데이터를 수명 주기에 관계없이 보존할 수 있게 해준다.
- 화면회전으로 activity, fragment를 재구성하게 될 경우 일반적으로 데이터는 초기화 되지만 사진과 같이 viewModel의 scope는 초기 activity가 `destroy`된 후에 `onCleared()`된다.

<div>
<img src="https://developer.android.com/images/topic/libraries/architecture/viewmodel-lifecycle.png?hl=ko" width="400">
</div>

- viewModel에 activity, fragment에 대한 컨텍스트를 저장해서는 안된다.
- activity가 재성생될 때 viewModel은 액티비티 수명주기 외부에 존재하기 때문에 컨텍스트를 viewModel에 저장하면 메모리 leak이 발생한다.
- application컨텍스트를 주는 것은 가능하다.

### LiveData

- 일반 클래스와 달리 수명 주기를 인식한다.
- activity, fragment의 수명주기를 고려할 수 있다.
- 수명 주기를 인식하는 것은 `Observer`가 인식하여 데이터를 업데이터 한다.

- `Observer` 클래스는 관찰자의 수명주기가 `STARTED`, `RESUMRED`상태이면 LiveData는 관찰자 활성상태로 간주한다.
- 그리고 LiveData는 활성 관찰자(Observer)에게 업데이트 정보를 알린다.

- 이처럼 수명주기를 인식하며 동작하기 때문에 Observer를 사용하는데에 해당 context의 lifeCycler을 전달해준다.
- 그리고 `DESTROYED`상태를 인식해 `Observer`를 삭제할 수 있다.

- 결과적으로 다음과 같은 장점이 있다.
  - 메모리 누수 없음
    - `LifeCycler`객체에 결합되어 수명주기가 끝나면 자동으로 삭제됨
  - UI와 데이터 상태 일치 보장
    - LiveData는 관찰자 패턴을 따라 수명주기가 변경될때 `Observer`객체에 알린다.
    - `Observer`객체에 UI를 업데이트할 수 있다.
    - 앱 데이터가 변경될 때마다 UI를 업데이트하는 대신, 관찰자가 UI를 업데이트할 수 있다.

#### setValue, postValue

- setValue, postValue는 LiveData의 데이터를 업데이터하는 메소드이다.
- 이를 사용하는 주체가 UI스레드일 경우는 차이가 없다.
- 하지만 UI스르데가 아닐경우 setValue로 세팅한 값은 UI를 변경하지 못한다.
- postValue로 세팅한 값은 해당 값을 UI스레드로 post해주기 때문에 UI스레드가 아니여도 UI를 변경할 수 있다.

```kotlin
private val _mDBMarkDataOne =  MutableLiveData<MarkerDataVO>()
val mDBMarkDataOne: LiveData<MarkerDataVO>
	get() = _mDBMarkDataOne
```

### Activity 생명주기

- activity는 크게 3가지 상태로 나뉜다. resumed, paused, stopped
- Resumed
  - active상태로 화면에 보이는 상태
  - dialog가 떠도 dialog가 activity에 일부이기 때문에 active상태이다.
- paused
  - 화면에 보이지는 않지만 focus받지 못한 상태
  - 투명 activity에 가려진 경우도 paused상태이다.
- stopped
  - 화면에 보이지 않는 상태
  - 다른 activity에 가려지거나 홈버튼을 눌른 경우

#### 순서

- onCreate
  - 뷰가 생성되고 call-back method들이 실행된다.
  - `setContentView`를 호출하여 activity에 레이아웃을 정의함
- onStared
  - 포그라운드로 나오는 작업
  - 컴포넌트들이 visible된다
- onResume
  - 사용될 수 있도록 focus된다.
- onPaused
  - focus를 읽게 될 경우
- onStpped
  - 앱이 완전히 안보이게 된 경우
- onDestroy
  - 앱이 종료

### build 속도를 높이는 방법

- Gradle버전을 높힌다.
- Gradle Cashing을 true로 변경
- JVM Heap Size를 확장
- Dependency에 라이브러리 버전을 다이나믹이 아닌 정적버전으로 명시
  - 다이나믹 버전일 경우 지속적으로 버전을 체크하기에 성능이 저하된다.

### Context란?

- activitry나 애플리케이션에 대한 정보를 얻는데 사용된다.
- 리소스, DB, SharedPreference등에 사용하는데 권한을 얻는데 필요하다.

### ApplicationContext

- 앱의 수명주기를 의미한다.
- 현재 context와 무관하게 context가 필요하거나 activty에 벗어나는 context가 필요할 때 사용할 수 있다.

### Handler, Looper, MessageQueue

- 위 3가지는 Thread를 구성하는 구성요소이다.
- 또한 UI스레드와 workerThread와 통신할 수 있게 해준다.
- Looper는 MessageQueue에 있는 Message를 Handler에게 넘겨준다.
- Handler는 thread로 부터 `sendMessage()`부터 받은 받아 MessageQueue에 넘겨준다.
- MessageQueue로  부터 나온 Message는 Handler의 `handleMessage`에서 받아 처리된다.
  - 이러한 처리를 통해 thread에서 처리된 결과를 MainThread에 보내줘서 사용자가 결과를 받아 볼 수 있게 할 수 있다.
  - [예제](https://github.com/vvvvvoin/MC_Android/blob/master/app/src/main/java/com/example/androidlectureexample/Example11_CounterLogHandlerActivity.java)

### AsyncTask

- 파라미터 타입으로 <param, progress, result>가 존재

- doInbackground(param)이 실질적인 백그라운드 작업을 한다. 
- 그리고 중간에 publishProgress(progress)를 호출하여 onProgressUpdate(progress)가 진행상황을 받아 UI를 업데이트 할 수 있다. 
- 그리고 doInbackground()가 종료될때 return으로 result를 반환하고 이를 onPostExcute, onCancel이 받을 수 있게 된다.

- AsyncTask는 LifeCycler과 무관하게 작동한다.
- 그래서 activity가 destroy될 때 `aysyncTask.cancel(true)`를 호출해야 한다.

### 패딩과 마진의 차이

- 마진은 해당 위젯의 부모 위젯간의 여백을 지정하는 것이다

- 패딩은 자기자신과 내용물 사이에 여백을 주는것 입니다.

### Lambda function과 high order function

### MainThread, WorkerThread

- 메인 스레드는 액티비티와 컴포넌트를 담당하고 연동하는 역할을 수행한다.
- UI스레드라고 하며 UI처리에 대한 역할을 수행하는데요
- 그렇기에 복잡한 작업, 네트워크, DB처리에 있어 UI스레드로 수행할 경우 화면이 멈추고 `ANR(Application Not Responding)`현상이 나타난다.
- 이러한 형상은 사용자를 하여금 답답한다.
- 그래서 위와 같은 연산은 비동기 스레드를 생성해서 해결한다.

### 4대 컴포넌트

#### Activity

- 사용자와 애플리케이션과 상호작용하는 화면이다.
- 사용자와 상호작용을 담당하는 인터페이스이다.
- 안드로이드 애플리케이션에는 하나 이상의 activity를 포함하고 생명주기와 관련된 메서드들을 정의하고 기능들을 구현할 수 있다.
  - 인텐트를 통해 다른 애플리케이션의 activity를 호출할 수 있다.
  - 2개 이상의 activity를 동시에 표시할 수 없다.
    - 프래그먼트로 해결

#### Service

- 서비스는 백그라운드에서 작업을 수행할 수 있는 컴포넌트이다.
- 서비스는 MainThread에서 동작하기 때문에 별도의 스레드를 생성해서 처리해야 한다.
  - mDB, 네트워크 연동
  - 애플리케이션이 종료되어도 시작된 서비스는 백그라운드에서 작동한다.

#### BroadCast Receiver

- 안드로이드 OS로 부터 발생하는 각종 이벤트와 정보를 받아 핸들링하는 컴포넌트이다.
- 이벤트에는 문자수신, 배터리 부족 등 다양한 정보를 받아 처리할 수 있게 해준다.

- OS 혹은 애플리케이션에서 `Intent Filter`를 담아 `BroadCast`하면 해당 filter를 갖고 있는 수신자가 `onReceiver`에서 핸들링하게 된다.
  - `BroadCastReceiver`를 구현한 클래스를 생성해 `manifetst.xml`에 filter로 작성한다
    - `manifetst.xml`에 `Intent Action`을 명시
  - 익명 클래스로 `BroadCastReceiver`를 생성과 동시에 `Intent Filter`를 생성해 `action`을 바인딩

#### Content Provider

- 콘텐트 제공자는 데이터를 관리하고 다른 애플리케이션에 데이터를 제공하는 역할을 수행하는 컴포넌트이다.
- 특정 애플리케이션이 사용하고 있는 DB를 공유하기 위해 사용하며 애플리케이션 가느이 데이터 공유를 위한 표준 인터페이스를 담당한다.

#### Intent

- 인텐트는 컴포넌트간에 작업 수행을 위해 정보를 전달하는 메세지 역할을 수행한다.
- 컴포넌트와 관련된 action, Data를 전달한다.
- 명시적, 암시적 인텐트로 나뉠 수 있다.
- 명시적 - 패키지명, 클래스명 등을 명시하여 실행하는 애플리케이션이 무엇인지 명시
- 암시적 - 일반적인 작업만 작성하고 다른 앱이 해당 인텐트를 처리하게 된다.
  - `anifest.xml`에 정의된 `Intent-Filter`가 이를 처리한다.

### ReactiveX

- 명령형 프로그래밍(Imperative programming) – 작성된 코드가 정해진 순서대로 실행됨.
- 리액티브 프로그래밍(Reactive Programing) – 데이터 흐름을 먼저 정의하고 데이터가 변경되었을 때 연관되는 메서드가 업데이트 되는 방식.
  - Retrofit에는 이를 다루기위해 Single 등에 여러 반환타입이 존재하는데 이를 리액티브 프로그래밍할 수 있다
  - 해당 작업을 수행하는 스레드를 `subscribeOn` 하고 해당 스레드로 부터 결과를 `ObserveOn`하는 스레드를 지정해 해당 결과를 `subscribe`하여 성공, 실패여부로 나누어  처리한다.

### sharedPreferences에서 commit, apply차이

- 서로 에디터에 작성된 결과를 반영시키는 메소드이다.
- commit은 메인스레드를 사용한 동기처리방식
- apply은 비동기처리방식이다

### 프래그먼트가 디폴트 생성자 하나만 사용하는 것을 추천하는 이유는 무엇인가요?

- 안드로이드에서 프래그먼트가 복원될때 프래그먼트는 기본 생성자를 호출한다.
- 이때 오버로딩된 생성자의 호출이 보장되지 않습니다.
- 그렇기에 생성자에 들어갈 객체는 Bundle에 담아 setArgument함수를 호출하는게 일반적이다.
- 그래서 newInstance로 fragment를 생성하는 이유도 이에 해당

### 안드로이드의 테스크란?

- Task는 어플리케이션에서 실행되는 Activity를 관리하는 스택입니다. 
- 스택이여서 선입 후출의 형태로 나중에 적제된 액티비티가 가장 먼저 사용됩니다. 
- 최초적재된 엑티비티는 Root Activity라고 하고 마지막에 적재된 Activity는 Top Activity라고 합니다.
- Flag를 이용하여 엑티비티의 흐름을 제어 할 수 있습니다.

### DI

- 의존성 주입이다.
- 의존성이란 함수에 필요한 클래스나 참조변수가 객체에 의존하는 것이다.
- 내부에서 필요한 객체를 생성하고 참조하지만 외부에서 그러한 객체를 생성해서 주입시켜주는 것이 주입이다.
- 그래서 개발자들이 객체를 생성하는 번거로움을 줄이고 클래스간 결합도를 낮추어 의존성을 낮춘다.

#### Dagger와 Koin의 차이점

- Dagger는 런타임 과정에서 에러가 발생하지 않는다.
- Koin은 발생한다.


### MVC

- 모델-뷰-컨트롤러로 이루어진 디자인 패턴이다.
- 비즈니스 로직과 사용자 인터페이스를 구분하여 서로간의 종속성을 줄여 유지보수에 유리하게 만드는 장점이 있다.
- 모델 - 비즈니스 로직이 처리되는 모듈로 사용자에게 보여지지 않습니다.
- 뷰 - 사용자와 상호작용하는 인터페이스로, Spring에 JSP가 해당 역할을 수행한다.
- 컨트롤러 - 뷰로 부터 받은 입력을 모델에 전달하여 상태정보를 업데이트하는 역할을 수행한다.
- 하지만 이를 android 관점으로 바꾸어본다면 android의 activity에서는 사용자에 입력을 받고(controller) 화면을 보여주는(view)의 역할을 수행한다.
- 또한 view와 model간에 의존성이 존재하게된다.
- 프로젝트 규모가 커질수록 코드가 복잡해지기 때문에 유지보수에 어려워 진다.

### MVP

- MVC에서 나타난 view와 model간에 의존성을 최소화하기 위해 나온 개념이다.

- 모델 - view, presenter등 다른 요소에 의존적이지 않은 데이터를 처리하는 역할을 수행
- 뷰 - 사용자와 상호작용하는 인터페이스 역할을 하며 Activity, fragment가 해당 역할을 수행
  - Prensenter를 이용해 데이터를 주고받기 때문에 서로 의존적임
- Presenter
  - view에 직접 연결되는 대신 인터페이스를 통해 상호작용한다는 점이 다름
  - 인터페이스로 작성되어있기 때문에 MVC가 가지는 모듈화, 테스트 문제를 해결할 수 있음

- 하지만 애플리케이션 규모가 커질수록 View와 Presenter간에 의존성이 강해진다.













