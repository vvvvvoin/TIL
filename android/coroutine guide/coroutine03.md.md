# Composing suspending functions﻿

## Sequential by default﻿

API콜이나 복잡한 연산을 어디서든 수행할 수 있는 2개의 `suspending functions`이 있다고 가정해보자. 하지만 다음 예제의 목적에서는 각각 딜레이를 갖는것을 확인할 수 있다.

```kotlin
suspend fun doSomethingUsefulOne(): Int {
    delay(1000L)
    return 13
}

suspend fun doSomethingUsefulTwo(): Int {
    delay(1000L)
    return 29
}
```

`doSomethingUsefulOne`, `doSomethingUsefulTwo` 를 순차적으로 호출할려면 어떻게 해야할까? 그리고 결과의 합은 얼마일까? 실제로 첫 번째 함수의 결과로 다른 함수를 호출해야하는 혹은 호출을 어떻게 할지를 결정해야 한다.



일반적으로 순차적으로 처리된다. 왜냐하먼 일반적으로 작성된 코루틴 코드는 순차처리(*sequential*)가 기본이다. 다음 예제에서 suspending functinos함수를 수행하는데 걸린 시간을 측정함으로서 설명할 수 있다.

```kotlin
fun main() = runBlocking {
    val time = measureTimeMillis {
        val one = doSomethingUsefulOne()
        val two = doSomethingUsefulTwo()
        println("The answer is ${one + two}")
    }
    println("Completed in $time ms")
}
```

```
The answer is 42
Completed in 2012 ms
```



## Concurrent using async﻿

`doSomethingUsefulOne`,  `doSomethingUsefulTwo` 두 사이에 종속성이 없다면 어떻게 될까? 그리고 두 함수를 동시에 실행함으로서 더 빠르게 결과를 얻어 보고 싶다.



개념적으로 `async`는 `launch`와 유사하다. aync는 모든 coroutine을 처리하는 경량 스레드에 나뉘어저서 처리가 시작된다. 차이점은 반환값으로 `job`을 반환하고 다른 결과를 가져오지 않는 `lanuch`와 다르게 `async`는 나중에 결과를 반환해주는`deferred`를 반환하게 된다. 그리고 `deferred`값에 `.awit()`을 사용하여 결과를 반환받을 수 있고 `deferred` 또한 `job`이며 원하는 중에 취소시킬 수 있다.



```kotlin
fun main() = runBlocking {
    val time = measureTimeMillis {
        val one = async { doSomethingUsefulOne() }
        val two = async { doSomethingUsefulTwo() }
        println("The answer is ${one.await() + two.await()}")
    }
    println("Completed in $time ms")
}
```

```
The answer is 42
Completed in 1019 mss
```

coroutine이 동시에 실행되었기에 더욱 빨라졌다. coroutine의 동시성은 항상 명시적이다.



## Lazily started async﻿

추가적으로, `async`는 `start` 매개변수를 `CoroutineStart.LAZY`를 설정함으로서 lazy하게 만들 수 있다. 이 설저에서는 coroutine은 `await`가 호출될 때나  `job`의 `start`가 호출될때도 실행된다.

```kotlin
fun main() = runBlocking {
    val time = measureTimeMillis {
        val one = async(start = CoroutineStart.LAZY) { doSomethingUsefulOne() }
        val two = async(start = CoroutineStart.LAZY) { doSomethingUsefulTwo() }
        // some computation
        one.start() // start the first one
        two.start() // start the second one
        println("The answer is ${one.await() + two.await()}")
    }
    println("Completed in $time ms")
}
```

```
The answer is 42
Completed in 1024 ms
```

위 예제에서 실행은 안됬지만 정의된 두 개의 coroutin이 있엇지만 프로그램적으로 `start`를 호출함으로서 제어할 수 있도록 하였다. 먼저 `one`을  `start` 후에 `two`를 수행했고 각각의 coroutine의 끝날때까지 기다렸다.



각각의 coroutine을 처음에 `start`를 호출없이 `println`에서 `await`를 호출했다면 순차적인 것으로 수행되었을 것이고 `await`가 coroutine을 실행하고 끝날때까지 기다리기 때문에 순차적인 동작으로 이어지는데 이는 lazy에 대한 의도된 사용사례가 아니다. `aync(start = CoroutineStart.LAZY)`를 사용하는 사례는 계산 값이  `suspending functions`을 포함할 때 표준 `lazy`함수로 대체된다.



## Async-style functions﻿

구조화된 동시성의 `opt-out`를  참고하는 `GloblaScop`을 사용하는 `async` coroutine 빌더를 사용함으로써 비동기적으로 `doSomethingUsefulOne`,  `doSomethingUsefulTwo`을 수행하는 비동기 스타일 함수를 정의했다. 각 함수가 비동기적으로 처리된다는 것과 deffred 값으로 결과를 얻기 위해 사용해야 한다는 것을  "...Aync"로 접미사를 붙여 이름지어 알려줄 수 있다.

> `GlobalScope`는 섬세한 API에서 반작용을 일으킬 수 있는데 이는 아래에서 설명할 것이다. 그래서 `GlobalScope`를 사용한다면 명시적으로 ``@OptIn(DelicateCoroutinesApi::class)`를 사용해야 한다.

```kotlin
// The result type of somethingUsefulOneAsync is Deferred<Int>
@OptIn(DelicateCoroutinesApi::class)
fun somethingUsefulOneAsync() = GlobalScope.async {
    doSomethingUsefulOne()
}

// The result type of somethingUsefulTwoAsync is Deferred<Int>
@OptIn(DelicateCoroutinesApi::class)
fun somethingUsefulTwoAsync() = GlobalScope.async {
    doSomethingUsefulTwo()
}
```

`xxxAsync`함수들은 suspending function이 아니다. 해당 함수들은 어디서든 사용될 수 있다. 그러나 사용한다는 것은 항상 비동기 실행을 의미한다.



```kotlin
fun main() {
    val time = measureTimeMillis {
        // we can initiate async actions outside of a coroutine
        val one = somethingUsefulOneAsync()
        val two = somethingUsefulTwoAsync()
        // but waiting for a result must involve either suspending or blocking.
        // here we use `runBlocking { ... }` to block the main thread while waiting for the result
        runBlocking {
            println("The answer is ${one.await() + two.await()}")
        }
    }
    println("Completed in $time ms")
}
```

```
The answer is 42
Completed in 1092 ms
```

`val one = somethingUsefulOneAsync()` 라인과 `one.await()`사이에서  코드상에 몇가지 에러가 발생했다며 고려한다면, 프로그램은 에러를 발생시킬 것이고 수행중인 작업들은 중단될 것이다. 일반적으로 전역의 에러 처리자는 에러, 로그를 발견하고 개발자에게 알려줄 것이지만 프로그램은 계속해서 작업을 수행해 나갈 것이다. 그러나 여기 `somethingUsefulOneAsync`는 백그라운에서 작업이 중단되어도 계속해서 수행될 것이다. 이러한 문제는 아래와 같은 구조화된 동시성에서는 발생하지 않는다.



## Structured concurrency with async﻿

`concurrent using async`예제를 보자. 동시에 `doSomethingUsefulOne`,  `doSomethingUsefulTwo`를 수행하는 함수를 추출하고 해당 결과의 함을 반환받는다. 왜냐하면 `async` coroutine 빌더는 CoroutineScope 확장함수로 정의되어 있기 때문에 스코프에 포함시켜애 하며 coroutineScope함수가 제공하는 것은 다음과 같다.

```kotlin
suspend fun concurrentSum(): Int = coroutineScope {
    val one = async { doSomethingUsefulOne() }
    val two = async { doSomethingUsefulTwo() }
    one.await() + two.await()
}
```

이러한 방법으로 `concurrentSum` 함수 내부에서 어떤 코드가 잘못되었을 경우에는 에러를 던질것이고 스코프 빌더에서 시작하는 모든 coroutine은 취소될 수 있다.

```kotlin
fun main() = runBlocking {
    val time = measureTimeMillis {
        println("The answer is ${concurrentSum()}")
    }
    println("Completed in $time ms")
}
```

```
The answer is 42
Completed in 1015 ms
```



취소는 항상 코루틴 계층을 통해 전파됩니다.

```kotlin
fun main(): Unit = runBlocking {
    try {
        failedConcurrentSum()
    } catch (e: ArithmeticException) {
        println("Computation failed with ArithmeticException")
    }
}

suspend fun failedConcurrentSum(): Int = coroutineScope {
    val one = async<Int> {
        try {
            delay(Long.MAX_VALUE) // Emulates very long computation
            42
        } finally {
            println("First child was cancelled")
        }
    }
    val two = async<Int> {
        println("Second child throws an exception")
        throw ArithmeticException()
    }
    one.await() + two.await()
}
```

```
Second child throws an exception
First child was cancelled
Computation failed with ArithmeticException
```





