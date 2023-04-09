# Coroutine 끄적이기

## Channel

### capacity
채널이 갖는 수용량(버퍼) 크기를 의미한다. 버퍼 이상으로 값을 받게 되면 onBufferOverflow에 값에 따라 동작이 변경된다.

### onBufferOverflow

- BufferOverflow.SUSPEND : 수용량보다 더 많은 값을 받게 된다면 생산자 쪽을 중단 시키고 소비를 하게 된다.
- BufferOverflow.DROP_OLDEST : 수용량 보다 더 많은 값을 받게 된다면 오래된 값을 버퍼에서 제게한다.
- BufferOverflow.DROP_LATEST : 수용량 보다 더 많은 값을 받게 되면 버퍼에 있는 값을 유지하고 새로 받은 값을 무시한다.

## StateFlow, SharedFlow

### SatetFlow

- 초기값을 설정해줘야 합니다.
- StateFlow의 Collect 구현을 보면 `oldState != newState`을 보면 같은 값을 emit하지 않기 때문에 사용시 주의해야한다.

```kotlin
override suspend fun collect(collector: FlowCollector<T>): Nothing {
        //....
        var oldState: Any? = null // previously emitted T!! | NULL (null -- nothing emitted yet)
        // The loop is arranged so that it starts delivering current value without waiting first
        while (true) {
            // Here the coroutine could have waited for a while to be dispatched,
            // so we use the most recent state here to ensure the best possible conflation of stale values
            val newState = _state.value
            // always check for cancellation
            collectorJob?.ensureActive()
            // Conflate value emissions using equality
            if (oldState == null || oldState != newState) {
                collector.emit(NULL.unbox(newState))
                oldState = newState
            }
         //....
}
```

### SharedFlow

#### replay

- 구독하는 시점에서 전달받을 데이터의 갯수를 설정합니다. 값이 1이 라면 최근에 발행된 값을 다른 구독자가 받을 수 있습니다.

#### extraBufferCapacity (= capacity)

수용량의 값을 설정합니다.

#### onBufferOverflow

channel에서의 정책과 동일합니다.

MutableSharedFlow 생성 시 일부 파라미터만 사용한다면 다음과  `require`에서 에러가 발생할 수 있다.

```kotlin
MutableSharedFlow<Foo>(onBufferOverflow = BufferOverflow.DROP_OLDEST) // error!!

require(replay >= 0) { "replay cannot be negative, but was $replay" }
require(extraBufferCapacity >= 0) { "extraBufferCapacity cannot be negative, but was $extraBufferCapacity" }
require(replay > 0 || extraBufferCapacity > 0 || onBufferOverflow == BufferOverflow.SUSPEND) {
    "replay or extraBufferCapacity must be positive with non-default onBufferOverflow strategy $onBufferOverflow"
}
```

### stateIn, shareIn

콜드 스트림을 핫 스트림으로 변환하기 위한 확장함수이다.

공통 파라미터로 SharingStarted가 존재한다.

#### SharingStarted


- SharingStarted.Eagerly - 구독에 상관없이 곧 바로 생산을 시작한다.

```kotlin
private class StartedEagerly : SharingStarted {
    override fun command(subscriptionCount: StateFlow<Int>): Flow<SharingCommand> =
        flowOf(SharingCommand.START) // 곧 바로 시작
}
```


- SharingStarted.Lazily - 하나의 구독자에 있을 때에 동작한다.

```kotlin
private class StartedLazily : SharingStarted {
    override fun command(subscriptionCount: StateFlow<Int>): Flow<SharingCommand> = flow {
        var started = false
        subscriptionCount.collect { count ->
            // 구독이 하나 이상일 경우 시작
            if (count > 0 && !started) {
                started = true
                emit(SharingCommand.START)
            }
        }
    }
}
```


- SharingStarted.WhileSubscribed - 구독이 없으질 경우 파라미터에 따라 중지됩니다.

  - stopTimeoutMillis : 구독이 없어지고 얼마나 기다리고 정지할지 값을 지정합니다.
  - replayExpriationMilis : stopTimeoutMillis 이후 얼마나 기다리고 저장된 값을 제거할지 지정합니다. StateIn 같은 경우 initialValue가 지정되고 ShareIn은 값이 제거됩니다.

```kotlin
private class StartedWhileSubscribed(
    private val stopTimeout: Long,
    private val replayExpiration: Long
) : SharingStarted {
    init {
        require(stopTimeout >= 0) { "stopTimeout($stopTimeout ms) cannot be negative" }
        require(replayExpiration >= 0) { "replayExpiration($replayExpiration ms) cannot be negative" }
    }

    override fun command(subscriptionCount: StateFlow<Int>): Flow<SharingCommand> = subscriptionCount
        .transformLatest { count ->
            if (count > 0) {
                emit(SharingCommand.START)
            } else {
                // 구독이 없다면 stopTimeout 만큼 기다림
                delay(stopTimeout)
                if (replayExpiration > 0) {
                    emit(SharingCommand.STOP)
                    // 중단되었지만 replayExpiration 만큼 기다리고 cashe를 리셋함
                    delay(replayExpiration)
                }
                emit(SharingCommand.STOP_AND_RESET_REPLAY_CACHE)
            }
        }
        .dropWhile { it != SharingCommand.START } // don't emit any STOP/RESET_BUFFER to start with, only START
        .distinctUntilChanged() // just in case somebody forgets it, don't leak our multiple sending of START
}
```



#### stateIn

- StateFlow로 변환해주고 초기값을 설정해줘야 합니다.

#### shareIn

- SharedFlow로 변환해주고 버퍼에 대한 설정을 할 수 있습니다.

