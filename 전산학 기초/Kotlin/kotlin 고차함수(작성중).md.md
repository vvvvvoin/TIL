# 고차함수

## null 접근 피하기

고차함수에서 null 타입이 될 수 있는 함수를 받을 수 있다.
그래서 다음과 같이 null인 아닌 것을 체크해서 사용할 수 있다.

```kotlin
fun foo(callback: (() -> Unit)?) {
  // ...
  if (callback != null) {
    callback()
  }
}
```

함수 타입이 invoke 메소드를 구현하는 인터페이스라는 사실을 활용하면 이를 더 짧게 만들 수 있다.
일반 메소드처럼 invok도 안전 호출처럼 `callback?.invoke()`처럼 호출할 수 있다.

다음 간단하게 `joinToString`을 구현한 함수에서 확인해보자.

```kotlin
fun <T> Collection<T>.joinToString(
    separator: String = ", ",
    prefix: String = "",
    postfix: String = "",
    transform: ((T) -> String)? = null,
): String {
    val result = StringBuilder()

    result.append(postfix)
    for ((index, value) in this.withIndex()) {
        if (index > 0) {
            result.append(separator)
        }

        val str = transform?.invoke(value) ?: value.toString()
        result.append(str)
    }
    result.append(postfix)

    return result.toString()
}

```

transform을 안전호출하여 null이 아닐 경우 인자로 받은 함수를 수행하고, `?:`연산자를 통해 null인 경우 toString으로 변환해주고 있다.



