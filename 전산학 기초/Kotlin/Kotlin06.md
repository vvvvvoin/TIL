# Kotlin 08

## 스프레드 연산자 

- 가변 길이 인자는 메소드를 호출할 때 원하는 개수만큼 값을 진아로 넘기면 자바 컴파일러가 배열에 그 값들을 넣어주는 기능이다.
- 자바에서는 배열을 그냥 검기면 되지만 코틀린에서는 배열을 명시적으로 풀어서 배열의 각 원소가 인자로 전달되게 해야한다.
- 이러한 작업을 `*` (스프레드) 연산자가 작업을 해준다.

```kotlin
fun main(args: Array<String>) {
	val list = listOf("args: ", *args)
  println(list)
}
```

> list에는 String타입만 들어가게 되고 args를 *연산자 없이 넣어주게 될 경우 주소값이 저장된다.

## 확장함수

- 확장 함수를 만들려면 추가하려는 함수 이름 앞에 그 함수가 확장할ㄹ래스의 이름을 덧붙이기만 하면 된다.
- 클래스 이름을 **수신 객체 타입**이라 부르며 확장 함수가 호출되는 대상이 되는 값을 **수신 객체**라고 부른다.

```kotlin
// 수신객체 타입 : String
// 수신객체 : this (생략가능)
fun String.lastChar() : Char = this.get(this.length - 1)
```

- 어떤 클래스를 확장한 함수와 그 클래스의 멤버 함수의 이름과 시그니처가 같다면 멤버함수가 우선순위가 더 높아 멤버함수가 호출된다.

## 내부 클래스 - inner

- 우선 간단한 코드를 봐보자

```kotlin
interface State: Serializable

interface View {
  fun getState: State
  fun restoreState(state: State) {}  
}
```

```java
public class Button implements View {
  @Override
  public State getCurrentState() {
    return new ButtonState();
  }
  @Override
  public restoreState(State state) { /../ }
  
  public class ButtonState implements State { /../ }
}
```

- 해당 클래스는 NotSerializableException: Button 오류가 발생한다.
- 이는 자바에서 다른 클래스 안에 정의한 클래스는 자동으로 내부 클래스가 된다.
- 그래서 ButtonState 클래스 바깥쪽 Button 클래스에 대한 참조를 묵시적으로 포함한다.
- 그 참조로 인해 ButtonState를 직렬화할 수 없는 것이다.
- Button을 직렬화할 수 없으므 버튼에 대한 잠초가 ButtonState의 직렬화를 방해한다.
- 이 문제를 해결하기 위해서는 ButtonState를 static클래스로 선언하면 해당 클래스를 둘러싼 바깥 클래스에 대한 무시적인 참조가 사라진다.
- 코틀린에서도 중첩된 클래스가 기본적으로 동작하는 방식은 정반대이다.

```kotlin
class Button : View {
  override fun getCurrentState(): State = ButtonState()
  override fun restorState(stateL State) { /../ }
  class ButtonState: State { /../ } // ButtonState는 자바의 정적 중첩 클래스와 대응한다.
}
```

- 코틀린 중첩 클래스에 아무런 변경자가 붙지 않으면 자바 static 중첩 클래스와 같다.
- 이를 내부 클래스로 변경해서 바깥 클래스에 대한 참조를 포함하기 위해서는 `inner` 변경자를 붙여야 한다.

## 클래스 생성자 괄호

- 클래스를 정의할 때 별도로 생성자를 정의하지 않으면 컴파일러가 자동으로 아무일도 하지 않고 인자가 없는 디폴트 생성자를 만들어 준다.
- 생성자는 아무런 인자를 받지 않지만 만약 해당 클래스(B)를 상속한 하위 클래스(A)는 반드시 해당 클래스(B)의 생성자를 호출해야 한다.

```kotlin
class A: B()
```

- 이 규칙으로 기반 클래스의 이름 뒤에는 꼭 빈 괄호가 들어간다.

> 당연하겠지만 생성자 인자가 있다면 반드시 괄호안에 인자가 들어간다.

## 데이터 클래스의 프로퍼티

- 데이터 클래스의 프로퍼티가 반드시 `val`일 필요는 없다
- 원한다면 var프로퍼티를 사용할 수 있지만 데이터 클래스의 모든 프로퍼티를 읽기 전용으로 만들어서 데이터 클래스를 불변(immutable) 클래스로 만들라고 권장한다.
  - HashMap 등의 컨테이너에 데이터 클래스 객체를 담을 경우 불변성은 필수적이다.
  - 데이터 클래스 객체를 키로 하는 값을 컨테이너에 담은 다음에 키로 쓰인 데이터 객체의 프로퍼티를 변경하면 컨테이너 상태가 잘못 될 수 있다.
  - 불변 객체를 통해 프로그램에 대해 쉽게 추론할 수 있다.
  - 불변 객체를 사용하는 프로그램에서는 스레드가 사용 중인 데이터를 다른 스레드가 변경할 수 없으므로 스레드를 동기화해야 할 필요가 줄어든다.

## 클래스 위임, by

- 대규모 객체지향 시스템을 설꼐할 때 시스템을 취약하게 마드는 문제는 구현 상속의 의해 발생한다.
- 하위 클래스가 상위 클래스의 메서드 중 일부를 오버라이드하면서 서로간의 의존하게 된다.
- 시스템이 변함에 따라 상위 클래스의 구현이 바뀌거나 상위 클래스에 새로운 메서드를 정의하면 하위, 상위 클래스간 코드가 정상적으로 작동하지 않는 문제가 생길 수 있다.
- 이러한 문제점을 보완하기 위해서 코틀린에서는 모든 클래스를 기본적으로 `final`로 취급하고 상속을 염두하고 있는 경우에만 `open`을 붙여 클래스를 확장할 수 있게 한다.
- 그렇지만 이런 종종 상속을 허용하지 않는 클래스에 새로운 동작을 추가해야할 경우가 있다.
- 이때 사용하는 일반적인 방법은 `Decorator`패턴이다.
  - 상속을 허용하지 않는 클래스(기존 클래스) 대신 사용할 수 있는 새로운 클래스(데코레이터)를 만들되 기존 클래스와 같은 인터페이스를 데코레이터가 제공하게 만들고, 기존 클래스를 데코레이터 내부에 필드로 유지하는 것이다.
  - 이 때 새로 정의해야 하는 기능은 데코레이터의 메서드에 새로 정의하고 기존 기능이 그래도 필요한 부분은 데코레이터의 메소드가 기존 클래스의 메소드에게 요청을 전달한다. (필드 내부에 있으니)

- Collection 인터페이스를 구현하면서 아무 동작도 벼경하지 안흔 데코레이터를 다음과 같이 만들 수 있다.

```kotlin
class DelegatingCollection<T> : Collection<T> {
   // 기존 클래스
    private val innerList = arrayListOf<T>()
  
   // 데코레이터의 인터페이스
    override val size: Int = innerList.size
    override fun contains(element: T): Boolean = innerList.contains(element)
    override fun containsAll(elements: Collection<T>): Boolean = innerList.containsAll(elements)
    override fun isEmpty(): Boolean = innerList.isEmpty()
    override fun iterator(): Iterator<T> = innerList.iterator()
}
```

- 인터페이스를 구현할 때 by키워드를 통해 그 인터페이스에 대한 구현을 다른 객체에 위임 중이라는 사실을 다음과 같이 명시할 수 있다.

```kotlin
class DelegatingCollection<T>(
    innerList : Collection<T> = ArrayList<T>()
) : Collection<T> by innerList { }
```

- 기존과 다르게 클래스 안에 있던 모든 메서드 정의가 없어졌다.
- 컴파일러가 그런 전달 메소드를 자동으로 생성하며 자동 생성한 코드의 구현은 DelegatingCollectiond에 있던 구현과 비슷하다.

- 이를 통해 보일러 플레이트 코드를 줄이고 관리 포인트를 일원화시켜 코드 유지보수를 용이하게 해준다.

## 람다 포획 변수

- 람다안에서 사용하는 외부 변수를 `람다가 포획한 변수`라고 한다.
- 함수안에 정의된 로컬 변수의 생명주기는 함수가 반환되면 끝나게 된다.
- 하지만 어떤 함수가 자신의 로컬 변수를 포획한 람다를 반환하거나 다른 변수에 저장한다면 로컬 변수의 생명주기와 함수의 생명주기가 달라질 수 있다.
- 포획한 변수가 있는 ㄹ마다를 저장해서 함수가 끝난 뒤에 실행해도 람다의 본문코드는 여전히 포획한 변수를 읽거나 쓸 수 있다.
- 파이널 변수를 포획한 경우에는 람다코드를 변수 값과 함께 저장한다.
- 파이널이 아닌 변수를 포획한 경우에는 변수를 특별한 래퍼로 감싸 나중에 변경하거나 읽을 수 있기 하여 래퍼에 대한 참조를 람다 코드와 함께 저장한다.

```kotlin
// 변경 가능한 변수를 포획하는 클래스
class Ref<T> (var value: T)

val counter = Ref(0)
// 변경 불가능한 변수를 포획했지만 그 변수가 가리키는 객체의 필드 값을 바꿈
val result = { counter.value++ }
```

## all, any

- 어떤 조건을 모두 만족시키는 경우 `all`, 하나라도 만족할 경우 `any`를 사용한다.
- 그리고 어떤 조건에 대해 `!all`을 수행한 결과와 그 조건의 부정에 대해 `any`를 수행한 결과는 같다. (드모르간의 법칙)
- 반대로 `!any`를 수행한 결과와 그 조건의 부정에 대해 all과 같다.
- 그러므로 `all`, `any`에는 `!`를 붙이지 않는게 가독성에 좋다.

## count, size

- 람다식에 조건에 맞는 컬렉션의 갯수를 구하려할 때 `count`, `size`를 사용할 수 있다.

```kotlin
people.filter { it.age >= 27 }.size
people.count{ it.age >= 27}
```

- 둘의 결과는 같겠지만 `filter`는 중간 컬렉션이 생긴다.
- 반면 `count`는 조건엘 만족하는 원소의 개수만을 추적하지 조건을 만족하는 원소를 따로 저장하지 않는다.
- 결과적으로 다음과 같은 예에서는 `count`가 더 효율적이다.



