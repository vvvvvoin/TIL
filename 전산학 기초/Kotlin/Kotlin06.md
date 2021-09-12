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