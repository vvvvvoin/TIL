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

## distinctUntilChanged

- 해당 operator는 발행되는 값이 연속적을 다시 발행하는 것을 방지한다.
- distinct와는 다르게 추후에 같은 같이 나와도 출력은 가능하지만 연속적인 값만을 핸들링한다.
  - 즉, 중복이 발생한다
  - distinct의 경우 모든 경우에 대해 처리해야 하므로 메모리 사용량이 distinctUntilChanged보다 높다.

```kotlin
Observable.just(1, 2, 3, 3, 2, 2, 1, 3)
    .distinctUntilChanged()
    .subscribeOn(Schedulers.io())
    .subscribe {
        print("${it} -> ")
    }

// 결과
1 -> 2 -> 3 -> 2 -> 1 -> 3 -> 
```

- 객체같은 경우는 람다식에 연속적으로 나타나지 말아야할 값들을 지정해준다.

```kotlin
var a = Pserson(1, "james")
var b = Pserson(2, "john")
var c = Pserson(2, "merlin")
var d = Pserson(3, "josh")
var e = Pserson(4, "haily")

Observable.just(a, b, c, d, e)
    .distinctUntilChanged { t1, t2 -> t1.id == t2.id }
    //.distinctUntilChanged { t1, t2 -> t1.id == t2.id && t1.name == t2.name}
    .subscribeOn(Schedulers.io())
    .subscribe {
        println("${it} ")
    }

//결과
Pserson(id=1, name=james) 
Pserson(id=2, name=john) 
Pserson(id=3, name=josh) 
Pserson(id=4, name=haily) 
```

<div>
  <img src="https://user-images.githubusercontent.com/58923717/121766525-60375b80-cb8d-11eb-82f8-7558338cbc5a.png"/
</div>
## IgnoreElement

- RX1에서는 반환값이 없다면 `void`를 반환시켰다.
- 하지만 RX2에서는 이를 `competable` 반환하도록 권장하고 있고 이를 마이그레이션하고 void대신 사용하기 위한 오퍼레이터가 ignoreElement 이다.

## Processor

- RX에서는 다양한 subject가 존재한다.
- behavior, async, publish, replay subject가 존재하는데 이는 subject외에도 processor가 존재한다.
- behaviorPrecessor, publishProcessor가 존재한다.
- subject와 차이점이라면 backpressure를 지원하는 차이가 있고 이는 Flowable타입으로 활용될 수 있다.

## 실수

- Rx를 이용하면 비즈니스 로직을 간편하고 다양한 케이스에 대응하는 강력한 도구가 된다.
- 하지만 오퍼레이커가 많고 잘 못 사용하면 어디서 문제가 되는지 찾기 어려울 것이다.
- 다음은 실제 경험담을 통해 실수한 내용을 작성해본다.
- 잘 못 작성한 코드는 다음과 같았다.

```kotlin
fun main() {
    getInformationUseCase()
        .subscribe(System.out::println)
}

fun getInformationUseCase(): Single<String> {
    return Single.just("getMetaData")
        .map { metaData ->
            if (metaData.isNotEmpty()) {
                Single.zip(
                    Single.just("API call1"),
                    Single.just("API call2"),
                    ::Pair,
                ).map { println(it.first) }
            } else {
                Single.just("API call2").map(System.out::println)
            }
        }
        .ignoreElement()
        .andThen(
            Single.just("getInformation")
        )
}
```

- 초기에 metaData를 얻어서 해당 결과에 따라서 Single에 대한 발행값들이 찾이가 나고 이를 실행후 Completable로 변환 후 getInformation이라는 API를 호출했었다.
- main함수를 실행하면 결과는 `getInformation`만 표시된다.
- metaData를 이용하여 API call에 대한 발행값들은 표시가 되지 않았다.
- 아래 이유를 보기전에 원인을 생각해보면 좋을거 같다.
- 이유는 초기 metaData를 발행하고 이를 `map`한게 문제였다.
- metaData로 Single스트림을 유지하고 해당 값을 다시 `Single<Single<String>>`으로 처리되었고 해당 API call 스트림이 실행한되는게 문제였다.
- 이를 인지하지 못한 이유는 API call이후에 `ignoreElement`로 값을 무시해서 따로 어떤 타입인지 확인하지 못 했고 `map`안에서 당연하게 새로운 Observable을 만든게 실수였다.
- `map` -> `flatMap`으로 변경하면 정상동작하게 된다.

