# effective kotlin

## 가변성 제한

코틀린에서는 클래스, 객체, 함수 등으로 구성된 모듈로 프로그램을 설계한다. 이러한 요소 중 일부는 상태를 가질 수 있다. 예를들어 `var`, mutable 객체를 사용하여 상태를 가질 수 있다.

`var`, mutable 객체는 시간의 변화에 따라서 변화하는 요소를 표현하는데 괴장히 유용하지만, 상태를 적절하게 관리하는 것은 어렵다. 이는 몇 가지 이유가 존재한다.

1. 디버깅이 어려워진다. 상태를 갖는 부분들의 관계를 이해해야하며, 이를 추적하는 과정이 어려워진다. -> 만약 변경할 수 없는 상태, 값이었다면 간단하게 처리될 수 있다.
2. 가변성이 있으면 코드의 실행을 추론하기 어렵다. 시점에 따라 값이 변경되므로 현재 어떤 값을 갖고 있는지 알아야 하는 코드의 실행을 예측할 수 없다.
3. 멀티스레드 프로그램일 때는 적절한 동기화가 필요한다. 대부분의 프로그램이 멀티스레드 환경에서 동작하므로 변경이 일어나는 지점에서 충돌이 발생할 것이다.
4. 테스트가 어렵다. 이는 디버깅과 유사한 의미이며, 변경에 많을 수록 테스트에 대한 조합이 늘어나게 된다.
5. 상태 변경이 일어나면, 이러한 부분을 다른 부분에 알려줘야 한다.

물론 이러한 부분들을 혼자 개발한다면 관리하는데에 큰 어려움을 없을 것이다. 하지만 프로그램은 혼자가 아닌 팀 단위로 개발하기 때문에 변경 가능한 부분에 의한 일관성 문제, 복잡성 증가에 대한 문제를 처리하는데 중요할 것이다.

### 코틀린에서 가변성 제한

코틀린은 사변성을 제한할 수 있도록 설계되어 있어 immutable 객체를 만들거나 프로퍼티를 변경할 수 없게 막는 것이 굉장히 쉽다.

#### 읽기 전용 프로퍼티 val

`val`을 사용하여 읽기 전용 프로퍼티를 만들 수 있다. 이렇게 선언된 프로퍼티는 값 처럼 동작하며, 일반적인 방법으로 값이 변화지 않는다. 읽기전용 프로퍼티가 완정히 변경 불가능한 것은 아니다. 읽기 전용 프로퍼티가 mutable객체를 담고 있다면 다음과 같이 내부적으로 변화될 수는 있다.

```kotlin
val list = mutableListOf(1, 2, 3)
list.add(4)
```

코틀린 프로퍼티는 기본적으로 캡슐화되어 있고, 추가적으로 사용자가 정의 접근자 get, set를 가질 수 있다. 이러한 특성으로 코틀린은 API를 변경하거나 정의할 때 굉장히 유연하다.

`val`은 읽기 전용 프로퍼티지만, immutable을 의미하는 것은 아니다. 또한 이는 getter, delegate로 정의할 수 있다. 만약 완전히 변경할 필요가 없다면 `final` 프로퍼티를 사용하는 것이 좋다. `val`은 정의 옆에 상태가 바로 적히므로 코트의 실행을 예측하는 것이 간단하다. 또한 스마트 캐스트등의 추가적인 기능을 활용할 수 있다.

```kotlin
val name: String = "Martin"
val surname: String? = "Bruce"

val fullName: Stirng?
  get() = name?.let{ "$it $surname" }

val fullName2: String? = name?.let{ "$it $surname" }

fun main() {
  if (fullName != null) {
    println(fullName.length) // error
  }
  
  if (fullName2 != null) {
    println(fullName2.length)
  }
}
```

`fullName` 은 게터로 정의했으므로 스마트 캐스트할 수 없다. **게터를 활용하므로** **값을 사용하는 시점에 name에 따라서 다른 결과가 나올 수 있기 때문**이다. `fullName2`처럼 지역 변수가 아닌 프로터티가 final이고 사용자 저으이 게터를 갖지 않을 경우 스마트 캐스트 할 수 있다.

#### 가변 켈렉션과 읽기 전용 켈렉션 구분하기

코틀린에서는 읽고 쓸 수 있는 컬렉션과 읽기 전영 칼렉션으로 구분된다. 이는 켈렉션 설계된 방식 덕분이다. MutableIterable, MutableCollection, MutableSet, MutableList 인터페이스는 읽고 쓸 수 있는 컬렉션이다. mutable이 붙은 인터페이스는 대응되는 읽기 전용 인터페이스 Iterable, Collection, Set, List를 상속받아 변경을 위한 메서드들을 추가한 것이다. 읽기 전용 프로티가 게터만 갖고, 읽고 쓰기 전용 프로퍼티가 게터와 세터를 모두 가지던 것과 비슷하게 동자가한다.

읽기 전용 컬렉션이 내부의 값을 변경할 수 없다는 의미는 아니다. 대부분의 경우에는 변경할 수 잇다 읽기 전용 인터페이스가 이를 지원하지 않으므로 변경할 수 없다. 예를 들어 Iterable\<T>.map, filter 함수는 ArrayList를 리턴한다.

```kotlin
inline fun <T, B> Iterable<T>.map(
  transformation: (T) -> B,
): List<R> {
  val list = ArrayList<B>()
  for (element in this) {
    list.add(transformation(element))
  }
  return list
}
```

이러한 컬렉션을 진짜로 불변하게 만들지 않고, 읽기 전용으로 설계한 것은 중요하다. 이로 인하여 더 많은 자유를 얻을 수 있기 떄문이다. 내부적으로 인터페이스를 사용하고 있지만, 실제 컬렉션을 리턴할 수 있다. 따라서 플랫폼 고유의 컬렉션을 사용할 수 있다.

이는 코틀린이 내부적으로 immutable하지 않은 컬렉션을 외부적으로 immutable하게 보이게 만들어서 얻어지는 안정성이다. 그런데 다운 캐스팅을 할 때 문제가 된다. 실제로는 허용되지 안 되는 문제이다. 리스트를 읽기 전영으로 리턴하면, 이를 읽기전용으로만 사용해야한다. 하지만 컬렉션 다운캐스팅은 이러한 것을 위반하고 추상화를 무시하는 행위이다.

```kotlin
val list = listOf(1, 2, 3)

// wrong
if (list is MutableList) {
  list.add(4)
}


Exception in thread "main" java.lang.UnsupportedOperationException
	at java.base/java.util.AbstractList.add(AbstractList.java:153)
	at java.base/java.util.AbstractList.add(AbstractList.java:111)
```

위 코드는 실행 결과는 플랫폼에 따라 다르다. 자바에서는 `listOf`는 `Array.ArrayList` 인스턴스를 리턴하고 List인터페이스에서 add, set 같은 메서드를 제공한다. 그래서 코틀린의 MutableList로 변경할 수 있다, 하지만 `Arrays.ArrayList`는 이러한 연상을 구현하고 있자않아 오류가 발생한다. 이는 언제는 변경될 수 있는 동작일 수 있다. 하지만 지금은 아니기 때문에 코틀린에서 읽기 전용 컬렉션을 mutable 컬렉션으로 다운 케스틍해서는 안된다. 읽기 전용을 mutable로 변경해야 한다면 copy를 통해서 새로운 mutable 컬렉션을 만들어야 한다.

#### 데이터 클래스의 copy

String, Int는 내부적인 상태를 변경하지 않는 immutable 객체를 많이 사용하는데 이유가 있다.

1. 한 번 정의된 상태가 유지되므로, 코드를 이해하기 쉽다.
2. immutable 객체는 공유했을 때도 충돌이 없으므로 병렬 처리에 안전하다.
3. 참조는 변경되지 않으므로 쉽게 캐시할 수 있다.
4. 방어적 복사본을 만들 필요가 없다. 깊은 복사를 따로 하지 않아도 된다.
5. immutable 객체는 다른 객체를 만들 때 활용하기 좋다.
6. set, map의 키로 사용할 수 있다. mutable객체는 이러한 것을 사용할 수 없는데, 이는 set, map이 내부적으로 해시 테이블을 사용하고, 해시 테이블은 처음 요소를 넣을 때 요소의 값을 기반으로 버킷을 결정하기 때문이다. 따라서 요소에 수정이 일어나면 해시 테이블 내부에서 요소를 찾을 수 없게 되어 버린다.

### 다른 종류의 변경 가능 지점

변경할 수 있는 리스트를 만들어야 한다고 한다면 다음 처럼 두 가지 선택지가 있다.

```kotlin
val list1: MutableList<Int> = mutableListOf()
var list2: List<Int> = listOf()
```

두 객체 모두 변경할 수 있지만 방법이 다르다.

```kotlin
list.add(1)
list2 = list2 + 1
```

두 가지 모두 정삭적으로 동작하지만 장단점이 있다. 첫 번째 코드는 구체적인 리스트 구현 내부에 변경 가능 지점이 있다. 멀티스레드 처리가 이루어질 경우 내부적으로 적절한 동기화가 되어 있는지 확실하게 알 수 없으므로 위험하다. 두 번째 코드는 프로퍼티 자체가 변경 가능 지점이기 때문에 멀티스레드 처리의 안전성이 더 좋다고 할 수 있다.

###  변경 가능 지점 노출하기 말기

상태를 나타내는 mutable 객체를 외부에 노출하는 것은 굉장히 위험합니다.

```kotlin
data class User(val name: Stirng)

calss UserRepository {
  private val storeUsers: MutableMap<Int, String> = mutableMapOf()
  
  fun loadAll(): MutableMap<Int, String> {
    return storeUsers
  }
}
```

loadAll 함수를 이용하여 private 상태인 UserRepository를 수정할 수 있다. 이러한 것들은 돌발적인 수정이 일어날 때 위험할 수 있다. 이럴 처리하는 방법은 두 가지이다. 리턴되는 mutable 객체를 복제하는 것이다. 이를 방어젝 복제라고 한다.

```kotlin
class UserHolder {
  private val user: MutableUser()
  
  fun get(): MutableUser {
    return user.copy()
  }
}
```

혹은 가변성을 제한하는 읽기 전용인 슈퍼타입으로 업케스트히여 가변성을 제한할 수 있다.

```kotlin
data class User(val name: Stirng)

calss UserRepository {
  private val storeUsers: MutableMap<Int, String> = mutableMapOf()
  
  fun loadAll(): Map<Int, String> { // mutableMap -> Map
    return storeUsers
  }
}
```

