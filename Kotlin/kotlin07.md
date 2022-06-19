## value class

이름으로 의미를 전달하여 좀 더 이해가기 쉽게 만들 수 있다. 혹은 클래스 A 함수파라미터에 클래스 B만 오도록 강제하여 type-safety하게 만들 수도 있다. 이는 컴파일 타임에서의 에러를 방지할 수 있을 것이다.

Int, Boolean, Double 같은 primitive type들은 type-safety하지만 해당 의미를 실제로 전달하지 않는다.

Double같은 경우 섭씨온도, 킬로그램 단위의 무게 스크린 밝기의 퍼센트 단위등으로 나타나는 여러 척도가 된다. 우리는 Double이 부동소수점 숫자를 두 배의 정밀도로 다루고 있다는 것을 알지만 어떤 척도의 숫자인것은 알려주지 않는다. 이러한 이유로 semantic은 type-safety의 이점을 읽어버린다.

만약 화면에 밝기 수준을 나타내는 함수를 보면 다음과 같을 수 있다.

```kotlin
fun setDisplayBrightness(displayBrightness: Double) {}
```

Double의 타입을 갖는 특정 값으로 호출될 수 있지만 다른 의미를 갖는 다음과 같이 Double 값이 들어갈 수도 있다.

```kotlin
val weight: Double = 72.5
setDisplayBrightness(weight)
```

이러한 프로그래밍 에러는 컴파일타임에서 알수가 없고 런타임에서 에러가 발생해여 할 수 있는 부분들이다.

### 해결책

위에서 말한 문제를 해결하기에는 다음과 같은 방법들이 있다.

- data class
- type aliases
- value classes

#### data class

```kotlin
data class DisplayBrightness(val value: Double)

fun setDisplayBrightness(displayBrightness: DisplayBrightness) {}
```

- 장점
  - `DisplayBrightness`는 자체적으로 타입이면서 Double값을 가진다. 이제 `setDisplayBrightness(0.5)`같은 경우에 컴파일 에러가 발생할 것이다.
- 단점
  - 객체를 생성한다는 것인 비용적으로 보면 좋지 않다. primitive 값들은 stack에 빠르게 효율적으로 사용되지만, 객체는 heap에 쓰이고 이는 보다 많은 시간과 메모리를 사용한다.

#### type aliases

```kotlin
typealias DisplayBrightness = Double

fun setDisplayBrightness(displayBrightness: DisplayBrightness) {}
```

- 장점

  - 컴파일시점 언제든 `DisplayBrightness`는 기본적으로 Double로 교체된다. 왜냐면 `DisplayBrightness`타입은 Double과 동일한 타입이고 Double과 같은 최적화되고 빠른 처리 속도를 같는다. 만약 primitive와 type aliases를 비교해도 거의 동일한 수준의 결과를 갖는다.

- 단점

  - `DisplayBrightness`와 `Double`가 assignment-compatible(할당 호환성)갖는게 단점이지만 컴파일러가 이마저도 수용하게 된다.

    ```kotlin
    typealias DisplayBrightness = Double
    typealias Weight = Double
    
    fun setDisplayBrightness(displayBrightness: DisplayBrightness) {}
    
    fun callingFunction() {
        val weight: Weight = 85.4
      
        setDisplayBrightness(weight)
        setDisplayBrightness(76.2)
    }
    ```

#### value class

처음볼때는 data class와 유사하게 보일 수 있다. 다만 예약어가 다르며 어노테이션이 사용된다.

```kotlin
@JvmInline
value class DisplayBrightness(val value: Double)

fun setDisplayBrightness(displayBrightness: DisplayBrightness) {}
```

> @JvmInline이 요구되는 이유
>
> Kotlin/Native, Kotlin/JS backend에서는 기술적으로 value class를 지원하지만, Kotlin/JVM에서는 그렇지 않기 때문이다. JVM은 오직 빌드될때의 primitive 타입을 지원하기 때문이다.

- 장점

  - 컴파일러는 type alias와 같이 취급하지만 다른점이라면 value class는 코드가 컴파일러 되지 않는 assignment-compatible이 없다. 

    ```kotlin
    @JvmInline
    value class DisplayBrightness(val value: Double)
    
    fun setDisplayBrightness(displayBrightness: DisplayBrightness) {}
    
    fun callingFunction() {
        val weight: Double = 85.4
        setDisplayBrightness(weight) // compile error
    }
    ```

  - 위에 제시한 해결책들과 비교해서 primitive, type aliases와 동일한 성능을 갖는다.

  















