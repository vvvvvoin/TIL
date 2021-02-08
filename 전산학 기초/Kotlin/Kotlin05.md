# Kotlin

### Scope Functions

#### let

```kotlin
fun <T, R> T.let(block: (T) -> R) : R
```

- `let`함수는 매개변수화된 타입 T의 확장함수이다.
- 자기 자신을 받아서 R을 반환하는 람다식을 사용할 수 있다.

```kotlin
T?.let { ... }
```

- 위와 같이 `let`에 `non-null`만 들어올 수 있도록 사용할 수도 있다.

#### with

```kotlin
fun <T, R> with(receiver: T, block: T.() -> R) : R
```

- `with`는 일반 함수이기 때문에 객체 receive를 직업 입력받는다.
- 객체를 사용하기 위해서는 두 번재 파라미터 블록을 받는다.
- `T.()`를 람다 리시버라 하며, 입력을 받으면 함수내에서 `this`를 사용하지 않고도 입력받은 객체의 속성을 변경할 수 있다.

#### run

```kotlin
fun <T, R> T.run(block: T.() -> R) : R
```

- `run`은 `with`처럼 인자로 람다 리시버를 받고, 반환 형태도 비슷하다.
- 그러나 T의 확장함수라는 점에서 차이가 있다.
- 어떤 값을 계산할 필요가 있거나 여러 개의 지역변수 범위를 제한할 때 사용한다.

#### apply

```kotlin
fun <T> T.apply(block: T.() -> Unit) : T
```

- `appply`는 T의 확장함수로 블럭 함수의 입력을 람다 리시버로 받았기 때문에 블록 안에서 객체의 프로퍼티를 호출할때 it, this를 사용할 필요없다.
- `run`과 유사하지만 블럭에는 return값을 받지 않으며 자시자신인 T를 반환한다는 점에서 다르다.

#### also

```kotlin
fun <T> T.also(block : (T) -> Unit) : T
```

- `apply`와 유사하지만 블럭 함수의 입력으로 람다 리시버를 받지 않고 this로 받는다.
- `apply`와 마찬가지로 T를 반환한다.

### lateinit var? lazy?

- 두 방식 모두 늦은 초기화를 위한 방법이다.
- 일반적으로 곧바로 필요한 경우가 아닐 경우 바로 객체를 생성하면 메모리 측면에서 손해를 본다.
- 그래서 늦은 초기화를 통해 보완시킬 수 있다.
- 반변에 null로써 값을 초기화하는 방법이 있지만 이는 해당 참조변수를 null-able로 되고 null값이 들어가 잘못된 접근으로 `NullPointerException`이 발생할 수 있어 안전하지 못하다.

#### lateinit var

- `var`에서만 사용가능
- `null`초기화 안됨
- 기본형에 사용할 수 없음
- 초기화전에 접근할 수 없음
- mutable타입

#### lazy

- `val`에서만 사용가능
- 초기화를 위해서 함수명을 적어줘야한다.
- 기본형에 사용가능
- 사용될 경우 객체가 생성되고 다시 호출할 경우 생성된 객체를 재사용
- immutable타입

```kotlin
fun main() {
    lateinit var a : initTest
    val b : Int by lazy {
        println("lazy init")
        10000
    }
    println("main start")
    a = initTest()
    println(b)
    println(b)
    println("main end")
}

class initTest{
    init {
        println("init complete")
    }
}
//결과
//main start
//init complete
//lazy init
//10000
//10000
//main end
```

- 변수 a를 main start가 출력된 이후에 초기화할 수 있음을 볼 수 있다.
- 변수 b는 처음 호출되는 `println`문에서 초기화가 진행되고 다음 호출에는 생성된 객체를 재사용하게 된다.

