# ReactiveX

- Reactive Prgram은 옵저버 패턴으로 구독자에게 변경사항을 알려주는 비동기 기반 프로그래밍이다.
- 일반적인 명령형 프로그램이 아닌 데이터의 흐름을 먼저 정의하고 데이터가 변경되었을 때 연관되는 메소드가 업데이트 되는 방식을 Reaxtive Programming이라고 한다.
- 즉 필요에 의해 데이터를 요청하여 가공하는 것(절차형)이 아닌, 데이터를 관리주체하는 `Observable`에 데이터 변경시 요청을 받을 수 있도록 subscribe하여 변경사항을 전달하는 방식이다.
- 데이터의 흐름, 스트림을 만드는 `Observable`
  - 스트림을 만드는 일을 누가 할것인지 지정하는 `subscribeOn`
- 흐름, 스트림에서 데이터를 처리하는 `Subscribe`
  - 스트림에서 데이터를 누가  할 것인지 지정하는 `observeOn`

- Obserable은 데이터를 제공하는 생산자의 역할을 하여 3가지의 행동을 한다.
  - onNext - 새로운 데이터를 전달
  - onCompleted - 스트림의 종료
  - onError - 에러 신호를 전달

## Observable

- 이벤트 발행하는 주체
- Type
  - Observable - 최상위 기본타입
  - Single - 1개의 데이터만 반환 (null 반환시 예외 발생)
    - `just`를 사용하면 데이터를 1개만을 입력할 수 있다
  - Maybe - Null  가능성이 있는 1개의 데이터 반환 + Single
  - Completable - 반환값 없이 처리 후 종료
  - Flowable - Backpressure 지원, Observable의 발행과 구독의 속도차이를 조절

```kotlin
Observable
	.just("a", "b", "c", "d", "e")			//Observable 내부에 값을 순서대로 전달
	.subscribe { 							//5번의 onNext로 전달됨
		println(it) 						//Observable, 스트림으로 부터 데이터를 subsribe하여 출력
	}
```

> `just`는 매개변수 순서에 맟춰서 데이터를 발행한다.

- subscribe는 발행된 데이터를 처리하는 로직이 작성된다.

- subscribe는 다음과 같이 오버로딩되어 있다

```java
public final void subscribe(@NonNull Observer<? super T> observer)
public final Disposable subscribe(@NonNull Consumer<? super T> onNext)
public final Disposable subscribe(@NonNull Consumer<? super T> onNext, @NonNull Consumer<? super Throwable> onError)
public final Disposable subscribe(@NonNull Consumer<? super T> onNext, @NonNull Consumer<? super Throwable> onError,
            @NonNull Action onComplete) 
```

- 각 상황에 맞게 데이터를 처리, 에러처리, 완료 후 처리를 정의할 수 있다.

> `Action`은 `Runnable`과 같이 매개변수가 없고 반환타입도 없다.
>
> 실행 메서드도 `run()`인 함수형 인터페이스이다.

### Observable 구독

#### Subscribe 신청

- `subscribe` 메서드를 이용하여 발생된 데이터를 구독할 수 있다.
- 구독하는 방법에는 두 가지가 존재한다.
  1. Observer 객체를 생성

  2. 객체가 아닌 사용자가 필요한 함수형 인터페이스만을 지정

##### 1. Observer 객체를 생성

- Observable 주요 콜벡 메서드
  - onSubScribe(d : Disposable) : 구독을 신청하면 처음 호출됨
  - onNext(item : T) : 값을 발행할 때 호출하여 값을 넘겨줌
  - onError(e : Throwable) : Observable에서 에러 발생시 호출
  - onComplete() : 모든 값이 발행하면 호출
- 메서드를 오버라이딩하는 작성하는 번거로움이 있지만 재활용할 수 있다는 점에서 이점이 있다

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

##### 2. 함수형 인터페이스 지정

- Observable클래스에는 subscribe 메서드과 다음과 같이 오버로딩되어 있다.

```java
public final void subscribe(@NonNull Observer<? super T> observer)	//Observer 객체를 생성해서 구독하는 방법
public final Disposable subscribe(@NonNull Consumer<? super T> onNext)
public final Disposable subscribe(@NonNull Consumer<? super T> onNext, @NonNull Consumer<? super Throwable> onError)
public final Disposable subscribe(@NonNull Consumer<? super T> onNext, @NonNull Consumer<? super Throwable> onError,
            @NonNull Action onComplete) 
```

```kotlin
Observable.just("a", "b", "c", "d", "e")
	.subscribe ({
		println("onNext")
	},{
		println("onError")
	},{
		println("onComplete")
	})
```

#### Subscribe 해지

- 구독해지도 신청과 마찬가지로 2가지 방법이 존재한다.
- 구독시 observer객체를 넣어 해당 객체에 `Disposable`과 관련된 로직을 정의한다.
- `Disposable`를 `dispose()`를 이용하면 구독이 해지된다.

##### 1. Observer 객체를 이용한 구독해지

- observer객체 내부에 `Disposable`타입 객체를 선언하고
- `end`데이터가 삽입되면 구독해지 되도록 설정하였다.

```kotlin
val observer: Observer<String> = object : Observer<String> {
    lateinit var disposable : Disposable                    
    override fun onSubscribe(d: Disposable?) {              
        println("onSubscribe")                              
        if (d != null) {                                    
            disposable = d                                  
        }                                                   
    }                                                       
    override fun onNext(t: String?) {                       
        if(t == "end"){                                     
            disposable.dispose()                            
            println("subscribe dispose")                    
        }                                                   
        println("onNext = ${t}")                            
    }                                                       
    override fun onError(e: Throwable?) { }                 
    override fun onComplete() { }                           
}

Observable.just("a", "b", "c", "d", "end", "e")
    .subscribe(observer)
//결과
//onSubscribe
//onNext = a
//onNext = b
//onNext = c
//onNext = d
//subscribe dispose
//e가 출력되지 않음
```

##### 2. Disposable 객체를 이용한 구독해지

- `subscribe`한 후 `disposable`타입의 객체를 `dispose`해준다

```kotlin
val disposable = Observable.interval(100, TimeUnit.MILLISECONDS)
    .subscribe {                                                 
        println("onNext = ${it}")                               
    }                                                           
Thread.sleep(2000)                                              
disposable.dispose()                                            
println("main end")
//결과
//...
//onNext = 17
//onNext = 18
//main end
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
Observable.just("a", 1, "string", 10.5)
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

- m번까지 출력이 아닌 m번카운트 하는 것이기 때문에 마지막 데이터는 14가 된다.(그림참고)

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

- 정수는 0부터 시작되고 타입은 Integer

### Hot, Cold Observable

- Observable은 구독을 신청하면 데이터의 순서에 맞게 데이터를 발행해준다.
- 여러번 subscribe를 해도 처음 순서대로 동일한 데이터를 보내주는 방식을 `Cold Observable`이라 한다.
  - web 요청, DB 요청
- 반변에 데이터의 발행 시점이 구독시점이 아니여서 이전에 발행된 데이터를 받지 못하는 방식이 `Hot Observable`이다.
  - 센서값
  - 강물과 같이 이미 흘러간 물을 받을 수 없는 것과 같다

#### ConnectableObservable

- `Hot Observable` 중 하나로 `connect()`메서드를 호출하면 발행을 시작하는 Observable이다.
- `publish()`메서드로 기존 `Cold Observable`이 `Hot Observable`이 된다.

```kotlin
val connectableObservable = Observable.interval(100, TimeUnit.MILLISECONDS).publish()
connectableObservable.subscribe { println("1 Observer = ${it}") }
connectableObservable.connect()
Thread.sleep(200)
connectableObservable.subscribe { println("2 Observer = ${it}") }
Thread.sleep(200)
//결과
//1 Observer = 0
//1 Observer = 1
//2 Observer = 1
//1 Observer = 2
//2 Observer = 2
```

- `connect()` 메서드 호출전에 미리 구독한 `1 observer`은 0부터 데이터를 발행받는다.
- 하지만 이후에 구독한 `2 observer`는 1부터 데이터를 받기 시작한다.

## Subject

- Subject는 Oserver와 Observable과 같이 행동하는 프록시다.
- 왜냐하면 Subject는 Oserver이기 때문에 하나 이상의 Observable을 구독하거나 동시에 Observable이기 때문이다.
- 또한 하나의 Subject가 둘 이상의 Observable를 구독하면서 Cold Observable를 Hot Observable로 만들기도 한다.
- Subject는 Observer를 구현한 추상메서드이다.

### Subject 종류

#### AsyncSubject

- AsyncSubject는 Observable로 부터 발행된 마지막 값을 발행하고 Observable의 동작이 완료된 후 동작한다.

<div><img src="http://reactivex.io/documentation/operators/images/S.AsyncSubject.png"/></div>

- 또한 마지막 값이 에러가 발생된다면 observer는 아무 데이터도 발행받지 못하고 오류를 그대로 전달한다.

<div><img src="http://reactivex.io/documentation/operators/images/S.AsyncSubject.e.png"/></div>

```kotlin
val observable = Observable.range(1, 10)	//1부터 10번 카운트하여 정수값을 발행
val asyncSubject = AsyncSubject.create<Int>()

observable.subscribe(asyncSubject)	//Subject는 Observer를 구현한 추상메서드라서 Observer타입의 매개변수가 될 수 있다.
                                                        
asyncSubject.subscribe { println("1 observer = ${it}") }
Thread.sleep(1000)
asyncSubject.subscribe { println("2 observer = ${it}") }
//결과
//1 observer = 10
//2 observer = 10
```

#### BehaviorSubject

- observer가 BehaviorSubject를 구독하기 시작하면 Observable이 가장 최근에 발행한 항목의 발행을 시작한다.
- 만약 아직 아무것도 발행하지 않았으면 기본값을 발행 후 이후에 발행된 데이터를 처리한다.

<div><img src="http://reactivex.io/documentation/operators/images/S.BehaviorSubject.png"/></div>

> 1번째 observer가 구독할 시점에는 발행된 데이터가 없어서 기본 데이터 발행
>
> 2번째 observer가 구독할 시점에 최신 데이터는 녹색이므로 녹색 데이터가 발행됨

- 오류 때문에 종료된다면 이후 구독하는 observer는 아무런 데이터를 받지 못하고 발생된 오류를 받는다.

<div><img src="http://reactivex.io/documentation/operators/images/S.BehaviorSubject.e.png"/></div>

```kotlin
val behaviorSubject = BehaviorSubject.createDefault(0)
behaviorSubject.subscribe { println("1 observer = ${it}") }
behaviorSubject.onNext(100)
behaviorSubject.onNext(200)

behaviorSubject.subscribe { println("2 observer = ${it}") }
behaviorSubject.onNext(300)
behaviorSubject.onNext(400)
//결과
//1 observer = 0	//구독시점에서 발행된 데이터가 없어서 기본값을 받음
//1 observer = 100
//1 observer = 200
//2 observer = 200
//1 observer = 300
//2 observer = 300
//1 observer = 400
//2 observer = 400
```

#### PublishSubject

- PublishSubject는 구독 이후에 발행된 데이터만 발행한다.
- PublishSubject는 생성시점에서 즉시 데이터를 발행하는 특성이 있기 때문에 생성시점에서 observer가 해당 subject를 구독하기 시작하는 사이에 데이터를 발행할 수 있다.
- 그렇기 때문에 Observable이 발행하는 모든 데이터를 보장받기 위해서는 `Create`메서드를 이용하여 명시적인 `Cold Observable`로 생성해야 한다.
- 혹은 ReplaySubject를 사용해야 한다.

<div><img src="http://reactivex.io/documentation/operators/images/S.PublishSubject.png"/></div>

```kotlin
val observable = Observable.interval(100, TimeUnit.MILLISECONDS)
val publishSubject = PublishSubject.create<Long>()
observable.subscribe(publishSubject)
publishSubject.subscribe { println("1 observer = ${it}") }
Thread.sleep(200)
publishSubject.subscribe { println("2 observer = ${it}") }
Thread.sleep(200)
//결과
//1 observer = 0
//1 observer = 1
//1 observer = 2
//2 observer = 2
//1 observer = 3
//2 observer = 3
```

#### ReplaySubject

- ReplaySubject는 Observer가 구독을 시작한 시점과 관계 없이 이전에 배출된 모든 데이터를 observer에게 발행한다.
- ReplaySubject의 생성자 오버로드를 통해 버퍼의 크기가 특정 이상으로 증가할 경우 처음 발행된 데이터를 지정된 시간이후 삭제하게 된다.
- ReplaySubject를 Observer로 사용할 경우 멀티스레드 환경에서는 비순차적 호출을 유할시키는 메서드는 사용하지 않도록 해야한다.

> [Observable 계약]([ReactiveX - The Observable Contract](http://reactivex.io/documentation/ko/contract.html))

<div><img src="http://reactivex.io/documentation/operators/images/S.ReplaySubject.png"/></div>

```kotlin
val replaySubject = ReplaySubject.interval(200, TimeUnit.MILLISECONDS)
replaySubject.subscribe { println("1 observer = ${it}") }
Thread.sleep(500)
replaySubject.subscribe { println("2 observer = ${it}") }
Thread.sleep(500)
//결과
//1 observer = 0
//1 observer = 1
//1 observer = 2
//2 observer = 0
//1 observer = 3
//2 observer = 1
```

## Operator

- Operator는 Java8에 추가된 람다와 스트림에서 사용되는 중간연산, 최종연산과 같은 역할을 수행한다.
- Operator에는 생성, 변환, 필터, 결합, 에러, 유틸, 상태, 연산과 관련된 메서드들이 정의되어 있다.

### 생성

- 생성 operator는 Observable을 생성하는 `create`,` empty`, `interval`, `just`, `range`등이 존재한다.

### 변환 & 필터

#### Filter

- Filter는 Observable에서 발행하는 데이터를 조건식으로 구분한다.

<div><img src="http://reactivex.io/documentation/operators/images/filter.png"/></div>

```kotlin
Observable.just(1,2,3,4,5,6,7,8,9)
    .filter { it -> it % 2 == 0 }	//짝수 값만을 필터링
    .subscribe {
        println("onNext = ${it}")
    }
//결과
//onNext = 2
//onNext = 4
//onNext = 6
//onNext = 8
```

> filter는 Predicate 함수형 인터페이스로 입력값 하나, boolean값을 리턴한다

#### Distinct

- 발행되는 데이터가 중복되지 않게 한다.

<div><img src="http://reactivex.io/documentation/operators/images/distinct.png"/></div>

```kotlin
Observable.just(1,2,3,1,2,3,4)     
    .distinct()                    
    .subscribe(System.out::println)
//결과
//1
//2
//3
//4
```

#### First, Last

- First와 Last는 발행된 데이터의 첫번째와 마지막 값을 받는 필터링 operator이다
- 해당 메서드를 사용하는데 있어 조건에 만족시키는 값이 없을 수 있으므로 default값을 넣어야 한다.
- 또한 발행된 값이 하나가 나오는 것을 보장하기에 해당 Ovservable은 `Single`이 된다.

<div><img src="http://reactivex.io/documentation/operators/images/first.png"/></div>

```kotlin
Observable.just(1,2,3,4,5,6,7,8,9)
    .filter { it -> it % 2 == 0 }
    .first(0)
    .subscribe({
        println("onSuccess = ${it}"
    },{
        println("onError = ${it}")
    })
//결과
//onSuccess = 2
```

> 해당 subscribe는 public final Disposable subscribe(@NonNull Consumer<? super T> onSuccess, @NonNull Consumer<? super Throwable> onError)로 정의되어 있다.

- 또한 single의 subscribe에는 다음 오버로딩 메서드가 존재한다.

```kotlin
public final Disposable subscribe(@NonNull Consumer<? super T> onSuccess)
public final Disposable subscribe(@NonNull BiConsumer<? super T, ? super Throwable> onCallback)
```

- subscribe의 매개변수가 하나이기 때문에 람다식으로 사용하게 될 경우 명시적으로 함수형 인터페이스의 매개변수를 지정해줘야 한다.

#### Take, Skip

- Take(N)는 Observable에서 발행된 N개의 값만을 발행
  - TakeLast(N)는 Observable에서 마지막 N개의 값만을 발행
- Skip(N)은 Observable에서 발행된 최초 N개를 제외하고 발행
  - SkipLast(N)은 Observable에서 발행된 마지막 N개를 제외하고 발행

<div><img src="http://reactivex.io/documentation/operators/images/take.png"/></div>

```kotlin
Observable.just(1, 2, 3, 4, 5, 6, 7, 8, 9)
    .filter { it % 2 == 0 }
    .take(2)
    .subscribe { it
        println("onNext = ${it}")
    }
//결과
//onNext = 2
//onNext = 4
```

#### Map

- 발행된 각 항목에 함수를 적용시켜 변환하는 메서드

<div><img src="http://reactivex.io/documentation/operators/images/map.png"/></div>

```kotlin
Observable.just(1,2, 3, 4, 5)
    .map { it -> it * 10}
    .subscribe { 
        println("onNext = ${it}")
    }
//결과
//onNext = 10
//onNext = 20
//onNext = 30
//onNext = 40
//onNext = 50
```

#### FlatMap, ConcatMap

- FlatMap은 Observable에서 발행된 항목을을 다시 새로운 Single Observable로 항목들을 발행하게 된다.
- 새로운 Single Observable로 발행된 데이터들은 순서를 보장받지 못한다.

<div><img src ="http://reactivex.io/documentation/operators/images/flatMap.c.png"/></div>

```kotlin
Observable.just("1","2","3","4","5")
    .flatMap { value: String ->
        Observable.interval(200, TimeUnit.MILLISECONDS)
            .map { cnt: Long -> "$value nowCnt =  $cnt" }
            .take(2)
    }
    .subscribe {
        println("onNext = ${it}")
    }
//결과
//onNext = 3 nowCnt =  0
//onNext = 1 nowCnt =  0
//onNext = 2 nowCnt =  0
//onNext = 4 nowCnt =  0
//onNext = 5 nowCnt =  0
//onNext = 1 nowCnt =  1
//onNext = 2 nowCnt =  1
//onNext = 3 nowCnt =  1
//onNext = 4 nowCnt =  1
//onNext = 5 nowCnt =  1
```

- flatMap내부에 새로운 Observable을 이용하여 200ms주기 마다 정수를 발행하는 값을 value에 붙였다.
- 또한 출력 결과는 순서를 보장하지 않는다는 것을 확인 할 수 있다.
- 대신 `concatMap`을 사용하여 순서를 보장할 수 있지만 성능은 flatMap에 비해 떨어진다.
- 또한 `concatMap`에 여러 Observable이 사용되면 다음과 같이 병합되지 않고 연결된다.

#### Debounce

- 특정시간 범위에서의 항목을 방출하지 않고 범위를 경과한 값을 방행한다.

<div><img src="http://reactivex.io/documentation/operators/images/debounce.png"/></div>

```kotlin
Observable.interval(105, TimeUnit.MILLISECONDS)
    .take(5)
    .debounce(100, TimeUnit.MILLISECONDS)
    .subscribe(System.out::println)
//결과 (매번바뀜)
//1
//3
//4
```

- 105ms간격마다 데이터를 입력하고 발행 시점에서 100ms가 지나면 해당값을 출력하게 된다.
- 5ms의 미세한 오차를 두어 몇몇 데이터가 출력되지 않음을 볼 수 있다.
- 이를 안드로이드에서 키보드 입력을 받을때 매번 새로운 입력이 들어올때마다 로직을 수행하는 것이아닌 debounce를 사용해 키보드 입력이 끝난 몇 ms후 로직을 수행할 수 있다.

#### Scan

- Scan은 순차적으로 함수를 적용하여 연속적으로 값을 방출한다.
- Java Stream의 Reduce와 같은 역할을 수행하는데 Scan은 순차적으로 처리된 값을 출력해준다.

<div><img src="http://reactivex.io/documentation/operators/images/scan.png"/></div>

```kotlin
Observable.just("a","b","c","d","e")
    .scan { now, next ->            
        "${now} -> ${next}"         
    }                               
    .subscribe(System.out::println) 
//결과
//a
//a -> b
//a -> b -> c
//a -> b -> c -> d
//a -> b -> c -> d -> e
```

- 순차적으로 발행된 값이 처리되는 과정을 알 수 있게 된다.

### 연산

#### Reduce

- 발행된 모든 데이터를 순차적으로 함수에 적용하고 최종값 하나를 발행한다.

<div><img src="http://reactivex.io/documentation/operators/images/reduce.png"/></div>

```kotlin
Observable.just("a","b","c","d","e")
    .reduce { now, next ->
        "${now} -> ${next}"
    }
    .subscribe(System.out::println)
//결과
//a -> b -> c -> d -> e
```

- Scan과 다르게 한번에 출력만을 보여준다.

#### Concat

- 두 개 이상의 Observable을 발행되는 데이터를 중간에 섞이지 않고 순차적으로 발행시킨다.

<div><img src="http://reactivex.io/documentation/operators/images/concat.png"/></div>

```kotlin
val observable1 = Observable.interval(0, 100, TimeUnit.MILLISECONDS)
    .map { "observable1 = $it" }
    .take(5)

val observable2 = Observable.interval(0, 200, TimeUnit.MILLISECONDS)
    .map { "observable2 = $it" }
    .take(5)

Observable.concat(observable1, observable2)
    .subscribe(System.out::println)
//결과
//observable1 = 0
//observable1 = 1
//observable1 = 2
//observable1 = 3
//observable1 = 4
//observable2 = 0
//observable2 = 1
//observable2 = 2
//observable2 = 3
//observable2 = 4
```

### 결합

#### Zip

- 지정된 기능을 통해 최소2개, 최대9개 Observable을 결합하여 순차적인 결합에 의해 데이터를 발행한다.

<div><img src="http://reactivex.io/documentation/operators/images/zip.png"/></div>

```kotlin
val observable1 = Observable.just(1,2,3,4,5,6,7)
val observable2 = Observable.just("a","b","c")

Observable.zip(observable1, observable2, BiFunction { obs1, obs2 ->
    return@BiFunction "$obs1 + $obs2"
}).subscribe(System.out::println)
//결과
//1 + a
//2 + b
//3 + c
```

- Zip의 특성상 순차적인 결합으로 observable1의 남은 데이터 4,5,6,7은 결합될 observable이 없어 출력되지 않는다.

#### CombineLatest

- 두 개의 Observable 중 하나의 데이터가 발행되는 경우 지정된 함수를 통해 각 Observable에서 발행된 최신데이터와 결합하여 이를 발행한다.

<div><img src="http://reactivex.io/documentation/operators/images/combineLatest.png"/></div>

```kotlin
val list1 = mutableListOf(1,2,3,4,5,6,7,8,9)
val list2 = mutableListOf("dog","cat","elephant", "human","thanos","deer")

val observable1 = Observable.fromIterable(list1)
    .zipWith(Observable.interval(200, TimeUnit.MILLISECONDS), BiFunction { int, time ->
        return@BiFunction int
    })
val observable2 = Observable.fromIterable(list2)
    .zipWith(Observable.interval(150, 200, TimeUnit.MILLISECONDS), BiFunction { str, time ->
        return@BiFunction str
    })

Observable.combineLatest(observable1, observable2, BiFunction { obs1, obs2 ->
    return@BiFunction "$obs1 + $obs2"
}).subscribe(System.out::println)
//결과
//1 + dog
//1 + cat
//2 + cat
//2 + elephant
//3 + elephant
//3 + human
//4 + human
//4 + thanos
//5 + thanos
//5 + deer
//6 + deer
//7 + deer
//8 + deer
//9 + deer
```

- observable1이 값을 발행하고 observable2가 150ms 늦게 시작하게 된다.
- 약간의 차이로 최근에 발행된 값과 함께 출력됨을 알 수 있다.

#### Merge

- 여러 Observable를 하나의 발행으로 결합시킨다.

<div><img src="http://reactivex.io/documentation/operators/images/merge.png"/></div>

```kotlin
val observable1 = Observable.interval(0, 100, TimeUnit.MILLISECONDS)
    .map { "observable1 = $it" }
    .take(5)

val observable2 = Observable.interval(0, 200, TimeUnit.MILLISECONDS)
    .map { "observable2 = $it" }
    .take(5)

Observable.merge(observable1, observable2)
    .subscribe(System.out::println)
//결과
//observable1 = 0
//observable2 = 0
//observable1 = 1
//observable1 = 2
//observable2 = 1
//observable1 = 3
//observable2 = 2
//observable1 = 4
//observable2 = 3
//observable2 = 4
```

### 상태 및 boolean

#### All

- Observable에서 발행되는 모든 데이터가 조건을 만족시키는 확인

<div><img src="http://reactivex.io/documentation/operators/images/all.png"/></div>

```kotlin
Observable.just("a", "b", "c", "d", "e", 5)
    .all { it is String }
    .subscribe({
        if (it == true) println("all is String type")
        else println("there are another type")
    }, {
        println("error")
    })
//결과
//there are another type
```

- all의 매개변수는 `Predicate`이므로 결과가 `boolean`타입으로 반환되고 이는 1개의 값만을 발행하는 것을 보장하기 때문에 `Single`을 반환한다.

#### Amb

- 둘 이상의 Observable이 주어지면 그 중 첫 번째로 발행된 Observable만을 발행한다.

<div><img src="http://reactivex.io/documentation/operators/images/amb.png"/></div>

```kotlin
val observable1 = Observable.interval(100, TimeUnit.MILLISECONDS).take(3).map { "observable1 = $it" }
val observable2 = Observable.interval(50, TimeUnit.MILLISECONDS).take(3).map { "observable2 = $it" }
val observable3 = Observable.interval(0,100, TimeUnit.MILLISECONDS).take(3).map { "observable3 = $it" }
val list = listOf(observable1, observable2, observable3)

Observable.amb(list).subscribe(System.out::println)
//결과
//observable3 = 0
//observable3 = 1
//observable3 = 2
```

- observable3은 최초 딜레이 없이 곧바로 값을 발행하여 observable3의 데이터만 발행하게 된다.

#### TakeUntil

- 두 번째 Observable에서 발행데이터를 받게 되면 모든 항목을 삭제하고 발행을 멈춘다.
- 만약 두 번재 발행이 첫 번째 발행과 겹치게 되면 출력하고 발행을 중지한다.

<div><img src="http://reactivex.io/documentation/operators/images/takeUntil.png"/></div>

```kotlin
Observable.interval(100, TimeUnit.MILLISECONDS)
    .map { "observable = $it" }
    .takeUntil(Observable.timer(500, TimeUnit.MILLISECONDS))
    .subscribe(System.out::println)
//결과
//observable = 0
//observable = 1
//observable = 2
//observable = 3
```

#### SkipUntil

- TakeUntil과 다르게 두번째 Observable에서 발행된 이후 데이터를 발행하게 된다.

<div><img src="http://reactivex.io/documentation/operators/images/skipUntil.png"/></div>

```kotlin
Observable.interval(100, TimeUnit.MILLISECONDS)
    .take(10)
    .skipUntil(Observable.timer(500, TimeUnit.MILLISECONDS))
    .subscribe(System.out::println)
//결과
//5
//6
//7
//8
//9
```
