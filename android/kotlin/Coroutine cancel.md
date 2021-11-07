# Coroutine cancel() in AAC-ViewModel

- 일반적으로 Coroutine을 통해 네트워크, DB처리를 손쉽게 할 수 있다.
- 또한 AAC-ViewModeld을 통해 구조화된 안드로이드 프로젝트를 만들 수 있다.
- 그렇지만 상황에 따라 비동기 처리를 중단하고 리소스를 반납시켜야 하는 경우가 존재한다.
- 많이 사용하는 ViewModel에서의 Coroutine의 cancel처리는 어떻게 이뤄질까?

## ViewModel에 Coroutine 등록 과정

- 우리는 일반적으로 ViewModel extension에는 *viewModelScope*를 통해 간단하게 코드를 작성할 수 있다.

```kotlin
public val ViewModel.viewModelScope: CoroutineScope
    get() {
        val scope: CoroutineScope? = this.getTag(JOB_KEY)
        if (scope != null) {
            return scope
        }
        return setTagIfAbsent(
            JOB_KEY,
            CloseableCoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)
        )
    }

internal class CloseableCoroutineScope(context: CoroutineContext) : Closeable, CoroutineScope {
    override val coroutineContext: CoroutineContext = context

    override fun close() {
        coroutineContext.cancel()
    }
}
```

- 리턴값은 `CloseableCoroutineScope`으로 `CoroutineScope`를 구현한 internal 클래스이다.
- 또한 Cloasable 인터페이스를 구현하여 `cloase()`를 오버라이딩하여 coroutineContext를 cancel시켜주고 있다.
- *viewModelScope*의 getter내부 코드에는 `setTagIfAbsent`메서드는 job_key로 ViewModel의 HashMap에 등록시킨다.

```java
    <T> T setTagIfAbsent(String key, T newValue) {
        T previous;
        synchronized (mBagOfTags) {
            previous = (T) mBagOfTags.get(key);
            if (previous == null) {
                mBagOfTags.put(key, newValue);
            }
        }
        T result = previous == null ? newValue : previous;
        if (mCleared) {
            // It is possible that we'll call close() multiple times on the same object, but
            // Closeable interface requires close method to be idempotent:
            // "if the stream is already closed then invoking this method has no effect." (c)
            closeWithRuntimeException(result);
        }
        return result;
    }
```

- 그리고 우리는 ViewModel 내부에서는 다음과 같이 사용한다.

```kotlin
@HiltViewModel
class MainViewModel @Inject constructor(
    private val getBooksRequestUseCase: GetBooksRequestUseCase,
) : BaseViewModel() {

    fun searchBooks(query: String) {
        viewModelScope.launch {
            getBooksRequestUseCase(query)
                .onSuccess {  }
                .onFailure {  }
        }
    }
}
```

- 결과적으로 CoroutineScope가 ViewModel에 등록됨과 동시에 해당 scope로 비동기 처리를 할 수 있도록 해준다.

## 등록된 Coroutine cancel 처리 과정

- activity, fragment의 ViewModeld은 ViewModelStored에서 관리된다.

```kotlin
public class ViewModelStore {

    private final HashMap<String, ViewModel> mMap = new HashMap<>();

		// some code //

    /**
     *  Clears internal storage and notifies ViewModels that they are no longer used.
     */
    public final void clear() {
        for (ViewModel vm : mMap.values()) {
            vm.clear();
        }
        mMap.clear();
    }
}
```

- `clear()`가 호출되면 각 ViewModel에 정의된 clear()가 호출되게 된다.

- ViewModelStored의 clear는 다음 두 곳에서 호출된다.

  - ComponentActivity.java -> 라이프사이클 이벤트가 onDestroy를 관찰했을 때

    ```java
            getLifecycle().addObserver(new LifecycleEventObserver() {
                @Override
                public void onStateChanged(@NonNull LifecycleOwner source,
                        @NonNull Lifecycle.Event event) {
                    if (event == Lifecycle.Event.ON_DESTROY) {
                        // Clear out the available context
                        mContextAwareHelper.clearAvailableContext();
                        // And clear the ViewModelStore
                        if (!isChangingConfigurations()) {
                            getViewModelStore().clear();
                        }
                    }
                }
            });
    ```

  - FragmentManagerViewModel.java -> onDestory가 호출될 때

- 그리고 ViewModelStore에서 각 ViewModel에서 호출하는 clear()를 살펴보자.

```java
    @SuppressWarnings("WeakerAccess")
    protected void onCleared() {
    }

    @MainThread
    final void clear() {
        mCleared = true;
        // Since clear() is final, this method is still called on mock objects
        // and in those cases, mBagOfTags is null. It'll always be empty though
        // because setTagIfAbsent and getTag are not final so we can skip
        // clearing it
        if (mBagOfTags != null) {
            synchronized (mBagOfTags) {
                for (Object value : mBagOfTags.values()) {
                    // see comment for the similar call in setTagIfAbsent
                    closeWithRuntimeException(value);
                }
            }
        }
        onCleared();
    }

```

- Coroutine등록된 hashMap의 값을 closeWithRuntimeException으로 처리하는 것을 확인할 수 있다.

```java
    private static void closeWithRuntimeException(Object obj) {
        if (obj instanceof Closeable) {
            try {
                ((Closeable) obj).close();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
```

- 그러면 *ViewModelScope*에서 closable을 구현한 인터페이스를 여기서 instanceOf로 확인하여 내부에 정의된 `close()`를 호출하고 결과적으로 coroutineContenxt.cancel()이 불려 activity가 종료시 coroutine 처리가 취소되게 된다.

## 정리

- Rx를 이용했다면 CompositeDisposable 객체를 만들고 bind시켜주고 BaseViewModel에  `protected void onCleared()`를 정의해서 dispose시켜줘야 했을 것이다.
- 그렇지만 Coroutine ViewModel Extension을 이용하여 관련 처리를 크게 구현할 필요가 없어진다.
- 크게 처리할 필요가 없는 이유는 일부 Cancel 처리에서 부분적으로 개발자가 핸들링해줘야 하는 부분이 있기 때문이다.

### Cacnel

- cancel은 coroutine의 동작을 취소시키는데 반드시 호출 즉시 정지되는 것은 아니다.
- while, 재귀함수 등에서 오랜 시간이 걸리는 작업에서는 inActivie, job을 통해 핸들링해줘야 한다.

> 참고 
>
> https://github.com/vvvvvoin/TIL/blob/master/android/kotlin/Coroutine.md#cancel
>
> https://thdev.tech/kotlin/2020/12/29/kotlin_effective_17/