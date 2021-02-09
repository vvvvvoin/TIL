# ReactiveX 추가

- 특정 주제와 분류없이 새롭게 배운 ReactiveX의 내용을 추가 및 정리합니다.

## Observable과 Flowable

- Observable과 Flowable의 서로 Ovservable이라는 공통점이 있다.
- 반면 Flowable은 backpressure이라는 buffer가 존재한다.
- Reactive는 발행과 구독 두 가지로 데이터가 처리가 된다.
- 하지만 발행속도에 비해 구독처리 속도가 느리다면 메모리 문제가 될 것이다.
- 다음과 같이 발행과 구독의 처리차이를 만들 수 있다.

```kotlin
val observable = Observable.range(1, 1000)
    .map {
        runBlocking { delay(100) }
        println("sending value = $it")
        "mapping value = $it"
    }
observable.observeOn(Schedulers.computation())
    .subscribe{
        println("receiving value = $it")
        runBlocking { delay(300) }
    }
//결과
//...
//receiving value = mapping value = 42
//sending value = 118
//sending value = 119
//sending value = 120
//receiving value = mapping value = 43
//sending value = 121
//sending value = 122
//receiving value = mapping value = 44
//sending value = 123
//sending value = 124
//sending value = 125
//...
```

- 위의 코드로는 문제가 발생하지는 않지만 처리되는 데이터에 따라 문제가 발생할 요인이 충분히 있을 수 있다.
- 이를 Flowable로 바꿔처리하게 된다면 일반적으로 128개의 요소를 버퍼로 담고 처리되게 된다.

```kotlin
val flowable = Flowable.range(1, 1000)
    .map {
        runBlocking { delay(100) }
        println("sending value = $it")
        "mapping value = $it"
    }
flowable.observeOn(Schedulers.computation())
    .subscribe{
        println("receiving value = $it")
        runBlocking { delay(300) }
    }
//결과
//...
//receiving value = mapping value = 44
//sending value = 124
//sending value = 125
//sending value = 126
//receiving value = mapping value = 45
//sending value = 127
//sending value = 128
//receiving value = mapping value = 46
//receiving value = mapping value = 47
//receiving value = mapping value = 48
//receiving value = mapping value = 49
//receiving value = mapping value = 50
//...
```

- 128개의 요소로 버퍼가 다채워지자 발행을 멈추고 지속적으로 구독처리를 진행하는 형태를 갖게 된다.