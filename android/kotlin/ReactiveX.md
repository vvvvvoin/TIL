# ReactiveX

- Reactive Prgram은 옵저버 패턴으로 구독자에게 변경사항을 알려주는 비동기 기반 프로그래밍이다.
- 일반적인 명령형 프로그램이 아닌 데이터의 흐름을 먼저 정의하고 데이터가 변경되었을 때 연관되는 메소드가 업데이트 되는 방식을 Reaxtive Programming이라고 한다.
- 즉 필요에 의해 데이터를 요청하여 가공하는 것(절차형)이 아닌, 데이터를 관리주체하는 `Observable`에 데이터 변경시 요청을 받을 수 있도록 subscribe하여 변경사항을 전달하는 방식이다.
- 데이터의 흐름, 스트림을 만드는 `Observable`
  - 스트림을 만드는 일을 누가 할것인지 지정하는 `subscribeOn`
- 흐름, 스트림에서 데이터를 처리하는 `Subscriber`
  - 스트림에서 데이터를 누가 할 것인지 지정하는 `observeOn`

- Obserable은 데이터를 제공하는 생산자의 역할을 하여 3가지의 행동을 한다.
  - onNext - 새로운 데이터를 전달
  - onCompleted - 스트림의 종료
  - onError - 에러 신호를 전달

## Observable

- 이벤트 발행하는 주체
- Type
  - Observable - 최상위 기본타입
  - Single - 1개의 데이터만 반환 (null 반환시 예외 발생)
    - `just`를 통해 데이터를 1개만 입력할 수 있다
  - Maybe - Null  가능성이 있는 1개의 데이터 반환 + Single
  - Completable - 반환값 없이 처리 후 종료
  - Flowable - Backpressure 지원, Observable의 발행과 구독의 속도차이를 조절

```kotlin
Observable.just("a", "b", "c", "d", "e")	//Observable 내부에 값을 순서대로 전달
	.subscribe { 							//5번의 onNext로 전달됨
        println(it) 						//Observable, 스트림으로 부터 데이터를 subsribe하여 출력
    }
```

- 이를 안드로이드에서 발행과 구독을 다루는 스케줄러를 지정할 수 있다.

```kotlin
Observable.just("a", "b", "c", "d", "e")
	.subscribeOn(Scheduler.io())		
    .observeOn(AndroidSchedulers.mainThread())
	.subscribe { 							
        Log("test", "now value ${it}")
    }
```

- `subscribeOn`을 선언하여 Observable와 Observer의 실행 Thread를 설정
  - 선언위치에 상관없음
- `observeOn` 선언 아래부분에만 선언한 Thread를 설정하는 함수
- 해당 Observable 스트림을 `Scheduler.io()`를 이용하여 발행하고 이를 `AndroidSchedulers.mainThread()`를 이용하여 데이터를 핸들링한다.

> subscribeOn보다 observeOn의 우선순위가 높기 때문에 각각의 Thread영역이 다르게 설정된다.

- subscribe는 다음과 같이 오버로딩되어 있다

```java
public final Disposable subscribe(@NonNull Consumer<? super T> onNext)
public final Disposable subscribe(@NonNull Consumer<? super T> onNext, @NonNull Consumer<? super Throwable> onError)
public final Disposable subscribe(@NonNull Consumer<? super T> onNext, @NonNull Consumer<? super Throwable> onError,
            @NonNull Action onComplete) 
```

- 각 상황에 맞게 데이터를 처리, 에러처리, 완료 후 처리를 정의할 수 있다.

> Action은 Runnable과 같이 매개변수가 없고 반환타입도 없다.
>
> 실행 메서드도 run()인 함수형 인터페이스이다.

### **Observable** 주요 콜벡 메서드

- onSubScribe(d : Disposable) : 구독을 신청하면 처음 호출됨
- onNext(item : T) : 값을 발행할 때 호출하여 값을 넘겨줌
- onError(e : Throwable) : Observable에서 에러 발생시 호출
- onComplete() : 모든 값이 발행하면 호출

```kotlin
val observer :Observer<String> = object : Observer<String> {
	override fun onSubscribe(d: Disposable?) {
		println("onSubscribe")
	}
	override fun onNext(t: String?) {
		println("onNext = ${t}")
	}
	override fun onError(e: Throwable?) {
		println("onError = ${e}")
	}
	override fun onComplete() {
		println("onComplete")
	}
}
Observable.just("a", "b", "c", "d", "e").subscribe(observer)
//결과
//onSubscribe
//onNext = a
//onNext = b
//onNext = c
//onNext = d
//onNext = e
//onComplete
```

### Observable 생성 메서드

#### Create

- just()는 선언 요소들을 순서대로 발행하지만 create는 직접 onNext를 호출하여 발행해야한다.

<div><img src="http://reactivex.io/documentation/operators/images/create.c.png" /></div>

```kotlin
Observable.create<Int>{	//it:ObservableEmitter<Int!>!
	it.onNext(10)	//값을 발행
	it.onNext(20)
	it.onNext(30)
	it.onComplete()	//발행 종료
}.subscribe({
	println(it)
},{
	println(it)
})
```

- ObservableEmitter는 onNext, onError, onComplete를 의미함

#### Just

- 받은 인자를 차례대로 순서에 맟춰서 발행하는 Observable을 생성
- 최대 10개까지 입력을 받을 수 있음

<div><img src="http://reactivex.io/documentation/operators/images/just.c.png"/></div>

```kotlin
Observable
	.just("a", 1, "string", 10.5)	//최대 10개까지 가능
	.subscribe({
		println(it)
	},{
		println(it)
})
```

#### Range

- 주어진 n지점부터 m 번까지 카운트한 Integer타입 데이터를 발행

<div><img src="http://reactivex.io/documentation/operators/images/range.c.png"/></div>

```kotlin
Observable
	.range(5, 10)
	.subscribe({
		println(it)
	},{
		println(it)
})
```

- m번까지 출력이 아닌 m번카운트 하는 것이기 떄문에 마지막 데이터는 14가 된다.(그림참고)

#### Empty, Never, Throw

- Empty는 데이터가 없는 Observable
<div><img src="http://reactivex.io/documentation/operators/images/empty.c.png" ></div>
- Never은 데이터가 없고  발행의 끝이 없는 Observable
<div><img src="http://reactivex.io/documentation/operators/images/never.c.png" ></div>
- Throw는 데이터가 없고 에러로써 발행이 종료되는 Observable
<div><img src="http://reactivex.io/documentation/operators/images/throw.c.png" ></div>

#### Interval

- 지정된 시간 간격에 따라 정수값을 발행하는 Observable
- 해당 Observable은 무한하게 오름차순으로 정수를 발행한다.
<div><img src="http://reactivex.io/documentation/operators/images/interval.c.png" ></div>

```kotlin
Observable.interval(100, TimeUnit.MILLISECONDS)
	.take(5)	//5개 까지만 발행
	.subscribe({
			println(it)
	}, {
			println(it)
	})
//출력은 0, 1, 2, 3, 4
```

- 정수는 0부터 시작됨

