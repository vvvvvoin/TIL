# Cancellation and timeouts﻿

## Cancelling coroutine execution﻿

백그라운드에서 앱이 긴 시간동안 작동중인 경우 섬세한 제어가 필요할 것이다. 예들 들어 유저가 어떤 페이지에서 동작중인 프로그래스가 더 이상 필요없어서 취소시킨다면 결과가 반환될 필요없이 해당 처리가 종료될 수 있어야 한다. `launch`함수가 `job`을 반환하는데 이를 통해서 작동중인 coroutine을 제어할 수 있다.

```kotlin
fun main() = runBlocking {
    val job = launch {
        repeat(1000) { i ->
            println("job: I'm sleeping $i ...")
            delay(500L)
        }
    }
    delay(1300L) // delay a bit
    println("main: I'm tired of waiting!")
    job.cancel() // cancels the job
    job.join() // waits for job's completion 
    println("main: Now I can quit.")
}
```

```
job: I'm sleeping 0 ...
job: I'm sleeping 1 ...
job: I'm sleeping 2 ...
main: I'm tired of waiting!
main: Now I can quit.
```

메인에서 `job.cancel`를 수행시키자마자, 해당 coroutine이 취소가 되었으므로 결과값을 볼 필요가 없다. `cancel`은 해당 coroutine이 completion되었다는 거를 의미하고 이를 기다리는 join을 통해서 결과를 기다린다. `job`확장함수에는 `cancelAndJoin`이 있는데 이는 `cancel`, `join`을 조합되어서 한 번에 사용할 수 있다.



## Cancellation is cooperative﻿

coroutine 코드는 취소될 수 있도록 되어있는데 모든 `kotlinx.coroutines`의  `suspending fuctions`는 취소할 수 있다. 이러한 함수들은 coroutine이 취소되었는지 확인하며 취소되었을 때에는 `CancelationExceoption`을 발생시킨다. 그러나 복잡한 계산을 수행하는 coroutine에서는 취소됨을 체크할 수가 없다. 다음 코드가 그러한 예제이다.

```kotlin
fun main() = runBlocking {
    val startTime = System.currentTimeMillis()
    val job = launch(Dispatchers.Default) {
        var nextPrintTime = startTime
        var i = 0
        while (i < 5) { // computation loop, just wastes CPU
            // print a message twice a second
            if (System.currentTimeMillis() >= nextPrintTime) {
                println("job: I'm sleeping ${i++} ...")
                nextPrintTime += 500L
            }
        }
    }
    delay(1300L) // delay a bit
    println("main: I'm tired of waiting!")
    job.cancelAndJoin() // cancels the job and waits for its completion
    println("main: Now I can quit.")
}
```

```
job: I'm sleeping 0 ...
job: I'm sleeping 1 ...
job: I'm sleeping 2 ...
main: I'm tired of waiting!
job: I'm sleeping 3 ...
job: I'm sleeping 4 ...
main: Now I can quit.
```



## Making computation code cancellable﻿

연산중에 코드가 취소될 수 있도록하는 방법이 2가지 있다. 첫번째는 코드상에 주기적으로 취소됨을 체크할 수 있는 `suspending function`을 사용하는 것이다. `yield`가 이러한 것에 적합하다. 다른 방법으로는 취소상태를 명확하게 확인하는 것이다.

위에 있는 코드중에 `while (i < 5)`를 `while (isActive)`로 바꾸고 확인해보라.

```kotlin
fun main() = runBlocking {
    val startTime = System.currentTimeMillis()
    val job = launch(Dispatchers.Default) {
        var nextPrintTime = startTime
        var i = 0
        while (isActive) { // cancellable computation loop
            // print a message twice a second
            if (System.currentTimeMillis() >= nextPrintTime) {
                println("job: I'm sleeping ${i++} ...")
                nextPrintTime += 500L
            }
        }
    }
    delay(1300L) // delay a bit
    println("main: I'm tired of waiting!")
    job.cancelAndJoin() // cancels the job and waits for its completion
    println("main: Now I can quit.")
}
```

```
job: I'm sleeping 0 ...
job: I'm sleeping 1 ...
job: I'm sleeping 2 ...
main: I'm tired of waiting!
main: Now I can quit.
```

반복문이 취소되었음을 확인할 수 있다. `isActive`는 `CoroutineScope` 객체를 통해 coroutine내부에서 사용할 수 있는 확장 속성이다.



## Closing resources with finally﻿

`CancellationException`을 발생시키는 취소가능한 `suspending functions`는 일반적인 방법으로 핸들린할 수 있다. try~finally 혹은 kotlin의 `use`를 통해 coroutine이 취소되었을때에 일반적인 방법으로 종료문을 수행할 수 있다.

```kotlin
fun main() = runBlocking {
    val job = launch {
        try {
            repeat(1000) { i ->
                println("job: I'm sleeping $i ...")
                delay(500L)
            }
        } finally {
            println("job: I'm running finally")
        }
    }
    delay(1300L) // delay a bit
    println("main: I'm tired of waiting!")
    job.cancelAndJoin() // cancels the job and waits for its completion
    println("main: Now I can quit.")
}
```

```
job: I'm sleeping 0 ...
job: I'm sleeping 1 ...
job: I'm sleeping 2 ...
main: I'm tired of waiting!
job: I'm running finally
main: Now I can quit.
```

`join`이나 `cancelAndJoin`은 종료문이 끝날때까지 기다리는 것을 위의 예제문에서 확인할 수 있다.



## Run non-cancellable block﻿

이전 예제에서 finally블록에서 `suspending function` 을 사용하면 `CancellationExceptino`이 발생한다고 예상할 수 있다. 왜냐하면 동작중인 coroutine이 취소되었기 때문이다. 일반적으로 이러한 것은 문제가 되지 않는다. 반변 잘 만들어저야하는 처리(스트림을 처리, job을 취소, 자원반납)에서는 일반적으로 `non-blocking`이고 다른 `suspending functions`을 발생시키지 않는다. 그러나 취소된 coroutine에서 중단을 해야할 특이한 케이스에서는 해당 코드를 `withContenxt(NonCancellable) {}`로 래핑할 수 있다. 이를 사용한 예제는 다음과 같다.

```kotlin
fun main() = runBlocking {
    val job = launch {
        try {
            repeat(1000) { i ->
                println("job: I'm sleeping $i ...")
                delay(500L)
            }
        } finally {
            withContext(NonCancellable) {
                println("job: I'm running finally")
                delay(1000L)
                println("job: And I've just delayed for 1 sec because I'm non-cancellable")
            }
        }
    }
    delay(1300L) // delay a bit
    println("main: I'm tired of waiting!")
    job.cancelAndJoin() // cancels the job and waits for its completion
    println("main: Now I can quit.")
}
```

```
job: I'm sleeping 0 ...
job: I'm sleeping 1 ...
job: I'm sleeping 2 ...
main: I'm tired of waiting!
job: I'm running finally
job: And I've just delayed for 1 sec because I'm non-cancellable
main: Now I can quit.
```

> Closing resources with finally﻿ 목차의 코드에서 suspending funciton을 사용할 경우 원하는데로 동작하지 않음을 확인할 수 있다.



## Timeout﻿

실행하는데 너무 오래결려 시간초과가 된다면 명백하고 확실하게 coroutine의 실행을 취소해야할 이유가 있다. 반변에 수동적으로 해당되는 `job`에 이를 취소할 수 있도록 하거나 별도의 다른 coroutine으로 지연된 이후에 취소시킬 수 있다. 다음코드에서 예저를 확인할 수 있다.

```kotlin
fun main() = runBlocking {
    withTimeout(1300L) {
        repeat(1000) { i ->
            println("I'm sleeping $i ...")
            delay(500L)
        }
    }
}
```

```
I'm sleeping 0 ...
I'm sleeping 1 ...
I'm sleeping 2 ...
Exception in thread "main" kotlinx.coroutines.TimeoutCancellationException: Timed out waiting for 1300 ms
```

`withTimeout`으로 발생한 `TimeoutCancellationException`은 `CancellationExceptino`의 서브 클래스이다. 콘솔에서 보기전까지 해당 에러를 본적이 없었다. 왜냐하면 취소된 coroutine의 `CancellationException`은 coroutine이 완료되면서 일반적으로 고려되었기 때문이다.

반변 취소는 단지 예외이기 때문이다. 일반적인 경우에서는 모든 자원들은 반환된다. timeout코드를 `try-catch(e: TimeoutCancellationException)`으로 래핑할 수 있고 만약 어떤 종류에 상관없이 시간초과에 대해 추가적인 작업을 하기 위해서는 `withTimeout`과 비슷하지만 시간초과 시 예외대신 null을 반환하는`withTimeoutOrNull`함수를 사용할 수 있다.

```kotlin
fun main() = runBlocking {
    val result = withTimeoutOrNull(1300L) {
        repeat(1000) { i ->
            println("I'm sleeping $i ...")
            delay(500L)
        }
        "Done" // will get cancelled before it produces this result
    }
    println("Result is $result")
}
```

```
I'm sleeping 0 ...
I'm sleeping 1 ...
I'm sleeping 2 ...
Result is null
```



## Asynchronous timeout and resources﻿

`withTimeout`에서의 시간초과는 해당 블록에서 실행 중인 코드와 관련하여 비동기적이고 시간초과 블록의 내부로 되기 직적, 언제든 발생될 수 있다. 블록 외부에서 자원을 해제해야하는 자원을 블록내부에서 수행할 경우 유의해야한다.



예를 들어, 여러번 `acquired`카운터 값을가 증가되고 감소되는 함수를 갖는  `Resource`클래스에서 확인할 수 있다. 짧은 시간초과내에 자원을 획득하고 외부에서 해제하는 coroutine을 많이 실행시켜본다.

```kotlin
var acquired = 0

class Resource {
    init { acquired++ } // Acquire the resource
    fun close() { acquired-- } // Release the resource
}

fun main() = runBlocking {
    runBlocking {
        repeat(100_000) { // Launch 100K coroutines
            launch {
                val resource = withTimeout(60) { // Timeout of 60 ms
                    delay(50) // Delay for 50 ms
                    Resource() // Acquire a resource and return it from withTimeout block
                }
                resource.close() // Release the resource
            }
        }
    }
    // Outside of runBlocking all coroutines have completed
    println(acquired) // Print the number of resources still acquired
}
```

위 코드를 실행시키면 항상 값이 0인 것을 확인할 수 있다. 컴퓨터의 시간에 따라 달라질 수 있지만 이 예에서는 0이 아닌 값을 실제로 보려면 제한 시간을 조정해야 할 수 있습니다.

> `acquired`값을 증가, 감소를 100k번을 수행하는데는 완전히 안전하다. 이는 같은 메인스레드에서 수행되기 때문이다.



이 문제를 해결하려면 `with Timeout` 블록에서 리소스를 반환하는 대신 변수에 리소스에 대한 참조를 저장하면 됩니다.

```kotlin
fun main() = runBlocking {
    runBlocking {
        repeat(100_000) { // Launch 100K coroutines
            launch {
                var resource: Resource? = null // Not acquired yet
                try {
                    withTimeout(60) { // Timeout of 60 ms
                        delay(50) // Delay for 50 ms
                        resource = Resource() // Store a resource to the variable if acquired
                    }
                    // We can do something else with the resource here
                } finally {
                    resource?.close() // Release the resource if it was acquired
                }
            }
        }
    }
// Outside of runBlocking all coroutines have completed
    println(acquired) // Print the number of resources still acquired
}
```

위 예제에서도 항상 0이 출력되고 자원이 유출되지 않는다.
