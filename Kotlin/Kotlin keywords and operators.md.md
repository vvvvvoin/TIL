# Kotlin keywords and operators

- 자주 사용되고 자주 보이는데 어떤 기능을 갖는지 헷갈리는 것들을 정의한다.

## Modifer keywords

- **infix : infix notation(삽입 표기)**로 함수를 호출할 수 있도록 해준다.

함수에 `infix` 예약어를 사용하면 삽입표기를 가능하게 해준다. 단, 몆가지 조건을 만족해야 한다.
  1. 확장함수이고나 멤버함수여야 한다.
  2. 하나의 매개변수를 갖어야 한다.
  3. 매개변수는 `varargs`가 안되고, 기본값을 가져서는 안된다.

```kotlin
infix fun Int.shl(x: Int): Int { ... }

// calling the function using the infix notation
1 shl 2

// is the same as
1.shl(2)
```

infix 함수는 항상 두 개의 리시버가 요구 되며, 매개변수가 명시되어야 한다. `infix notation`에서 현재 리시버에는 명시적으로 `this`를 사용하도록 한다.

```kotlin
class MyStringCollection {
    infix fun add(s: String) { /*...*/ }

    fun build() {
        this add "abc"   // Correct
        add("abc")       // Correct
        //add "abc"        // Incorrect: the receiver must be specified
    }
}
```



- **inline** : 컴파일러가 함수를 `inline`것으로 알려주고, 호출한 곳에 람다를 전달한다

고차함수를 사용하면 특정한 런타임 패널티가 있다. 각 함수는 `object`이고, `closure`를 포획한다. `closure`는 변수의 스코프이고, 함수내부에서 접근할 수 있다. 메모리 허용범위와 vitual call은 런타임에 오버헤드를 발생시킨다.

그러나, 이러한 것들의 대부분은 람다식에서 `inline`함으로써 오버헤드가 발생된다. 아래의 함수는 좋은 상황에서의 예시이다. `lock()` 함수는 함수호출 위치에 내부에 쉽게될 수 있다.

```kotlin
lock(l) { foo() }
```

오브젝트 함수로 생성하는 것 대신에, 컴파일러가 다음 코드를 수행할 수 있다.

```kotlin
l.lock()
try {
  foo()
} finally {
  l.unlock()
}
```

lock()함수에 `inline`를 사용함으로서 컴파일러가 위처럼 만들 수 있다.

```kotlin
inline fun <T> lock(lock: Lock, body: () -> T): T { ... }
```

`inline`은 함수자체와 람다에 영향을 준다. 이러한 모든 것들은 호출시점에서 내부에 인라인된다.

인라인을 사용하면 코드가 보다 많아질 수 있다. 그러나 합리적인 이유로써 inline하게 된다면, 성능이 좋아질 것이다. (특히, 루프 내부에서 `megamorphic`호출 시점에서)

> https://ionutbalosin.com/2019/03/kotlin-explicit-inlining-at-megamorphic-call-sites-pays-off-in-performance/



internal

in, out

reified
