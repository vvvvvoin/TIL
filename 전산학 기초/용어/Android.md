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

