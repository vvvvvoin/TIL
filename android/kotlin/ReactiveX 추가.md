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

## Throttle, Debounce

- Debounce는 발행된 데이터가 설정한 시간 이후에 구독할 수 있도록 한다.
- 하지만 설정한 시간 이전에 다른 데이터가 발행되면 최근에 발행된 데이터를 기준으로 다시 설정한 시간을 카운트하여 구독할 수 있도록한다.
- 반면에 Throttle는 최근에 생성된 데이터를 발행하고 설정한 시간동안 다른 발행되는 데이터를 무시하고 설정시간이 지나면 발행된 데이터를 처리하게 된다.

### Throttle

<div><img src="https://user-images.githubusercontent.com/58923717/111862377-5b9d4580-8998-11eb-9a05-4efb0403546f.JPG"/></div>

- 그림과 같이 발행된 데이터 파란색(1)이 들어오면 100ms간 발행되는 데이터를 무시하게 된다.
- 3번째로 발행된 녹색(2)가 들어오면 200ms간 발생된 데이터를 무시하여 노란(1), 파란(1)이 처리되지 않았다.
- 이때 3번째 발행된 녹색(2) 데이터를 2번째로 발행된 녹색(1)의 범위내로 움직이면 다음과 같이 된다.

<div><img src="https://user-images.githubusercontent.com/58923717/111862433-a8811c00-8998-11eb-88a6-59e6214618fc.JPG"/></div>

- 녹색(2)의 발생되는 데이터를 무시하게 되고 녹색(1)의 100ms이후 노란색(1)의 데이터가 처리되게 된다.

