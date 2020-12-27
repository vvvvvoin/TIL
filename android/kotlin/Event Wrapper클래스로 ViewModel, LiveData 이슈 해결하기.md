# Event Wrapper클래스로 ViewModel, LiveData 이슈 해결하기

## 문제점

- viewModel과 LiveData를 이용하면 여러 장점으로 애플리케이션을 설계할 수 있다.
- 또한 애플리케이션 화면이 회전하여도 아래 그림에서는 viewModel의 수명주기 상태를 보여준다

<div>
<img src="https://developer.android.com/images/topic/libraries/architecture/viewmodel-lifecycle.png?hl=ko" width="400">
</div>

- 그리고 LiveData로 activity를 observe() 했다면 observer가 저장한 데이터를 콜백하여 view에 바로 데이터를 바인딩 시켜줄 수 있다.
- 많은 장점도 있지만 주의해서 사용해야 되는 부분들이 있다.
- 만약 화면이 회전되고 다시 activity를 구성하면 observer가 저장된 데이터를 콜백하는데 해당 데이터가 일회성으로 작성된 값이어도 다시 호출되게 된다.
- 이런 문제가 발생하는 이유
  - viewModel이 activity의 모든 생명주기 동안 존재
  - liveData를 사용했기 때문에 viewModel Scope동안 데이터를 저장하고 있음
  - 결과적으로 liveData가 비활성 상태에서 활성 상태로 가면서 observer에 콜백을 전달
- 하지만 간단한 토스트 메세지를 출력하는 데이터 였다면 불필요하게 된다.

## 해결책

- 해결책에는 `SingleLiveEvnet`, `EventWrapper`가 존재한다
- 일반적으로 EventWrapper가 권장된다.

### 문제가 되는 코드
- 문제가 되는 코드는 다음과 같다.
```kotlin
//viewModel
class SampleViewModel : ViewModel(){
    private val _someData = MediatorLiveData<String>()
    val someData: LiveData<String>
        get() = _someData

    fun setData(str: String){
        _someData.value = str
    }
}

//activity
viewModel.somData.observe(this, Observer{// it: String
	Toast.makeText(this, "메세지 = ${it}", Toast.LENGTH_SHORT).show()
})
```

- `setData`로 데이터를 설정하게 되면 view에서는 이를 observe하여 토스트 메세지를 띄위게 된다.
- 하지만 화면이 회전되면 또 다시 토스트 메세지가 출력되게 된다.

### EventWrapper class

- 다음 클래스를 생성한다.
- Event클래스로 라이브 데이터를 받아 해당 데이터가 처리가 됬는지를 boolean값으로 구분한다.

```kotlin
open class Event<out T>(private val content: T) {

    var hasBeenHandled = false
        private set // Allow external read but not write

    /**
     * Returns the content and prevents its use again.
     */
    fun getContentIfNotHandled(): T? {
        return if (hasBeenHandled) {	//처리가 되었으면
            null						//null 반환
        } else {						//처리가 안됬으면
            hasBeenHandled = true		//처리됨을 표시하고
            content						//값을 반환
        }
    }
    /**
     * Returns the content, even if it's already been handled.
     */
    fun peekContent(): T = content
}

/**
 * An [Observer] for [Event]s, simplifying the pattern of checking if the [Event]'s content has
 * already been handled.
 *
 * [onEventUnhandledContent] is *only* called if the [Event]'s contents has not been handled.
 */
class EventObserver<T>(private val onEventUnhandledContent: (T) -> Unit) : Observer<Event<T>> {
    override fun onChanged(event: Event<T>?) {
        event?.getContentIfNotHandled()?.let { value ->
            onEventUnhandledContent(value)
        }
    }
}
```

### 수정된 코드

- `getContentIfNotHandled`로 하나의 observer에서만 사용가능하고 나머지는 `peekContent`로 값을 받는다.

```kotlin
//viewModel
class SampleViewModel : ViewModel(){
    private val _someData = MediatorLiveData<Event<String>>()//Event로 감싸기
    val someData: LiveData<<Event<String>>
        get() = _someData

    fun setData(str: String){
        _someData.value = Event(str)	//Event객체로 전달
    }
}

//activity
viewModel.somData.observe(this, Observer{// it: Event<String>!
	it.getContentIfNotHandled()?.let {//it: String
		Toast.makeText(this, "메세지 = ${it}", Toast.LENGTH_SHORT).show()
	}
})
//or
viewModel.somData.observe(this, EventObserver{// it: String
	Toast.makeText(this, "메세지 = ${it}", Toast.LENGTH_SHORT).show()
})
```

- 결과적으로 `getContentIfNotHandled` 데이터 처리됬는지를 확인하게 된다.
- 화면이 회전되어 다시 observer에 콜백을 전달해도 `getContentIfNotHandled`를 통해 null 값을 반환하게 되므로 문제가 해결된다.
- 만약 처리전에 observer에 콜백을 전달해도 null이 아닌 값을 반환하여 정상적으로 처리된다.