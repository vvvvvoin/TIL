# Kotlin

## listOf, arrayOf ?

- List는 ` inmutable` 이므로 변경이 불가능하다
- 변경하기 위해서는 `mutableListOf`로 선언해야한다.
- Array는 자바에서의 배열과 같기 떄문에 참조를 통해 변경가능하다.
- 마찬가지로 크기는 고정이기에 복사를 통해 크기를 키울 수 있다.

## 기본 자료형

- 코틀린에는 기본 자료형이 아닌 모두 객체로 이루어져있다.
- 그러나 코틀린을 컴파일 할 때 자바로 컴파일을 하고 자바 실행파일로 바꾸게 된다.
- 이때 객체를 기본자료형으로 쓸지  `wrapper클래스`로 할지를 정한다.
  - wraper : 자바에서 8개의 기본형을 객체로 다뤄야할 때 사용하는 클래스(Integer, Character, Double, .... )
    - 숫자 래퍼 클래스의 조상은 Number이다

## import

- 자바에서는 `import`를 할때 같은 이름의 클래스가 존재한다면 다른 것에는 패키지 명을 붙여서 사용해야 했다
- 코틀린에서는 다음과 같은 방법으로 사용할 수 있다.

```kotlin
import test1.abc
import test2.abc as abc2
```

## class

- kotlin에서는 클래스, 메소드들은 기본적으로 final로 선언된다.
- 그래서 다른 클래스를 상속받기 위해서는 부모 클래스 앞에 `open`이라는 예약어를 사용해야한다.
- 메소드를 오버라이딩 하기위해서도 해당 메소드에 `open`예약어를 사용해야한다.

```kotlin
open class Parent{
    open fun test(){
        print("parent")
    }
}
class Child : Parent(){
    override fun test() {
		print("child")
    }
}
```

## 연산자와 연산자 오버로딩

- kotlin에서는 산순, 단항, 비트 연산자를 내부적으로 오버로딩할 수 있는 함수가 제공된다.
- 클래스내에 연산자가 오버로딩되어 있다면 객체를 다루는데 편리해진다
  - 만약 `Coin`이라는 클래스에 멤버변수 5원과 10원이 있다
  - Coin 객체 두개를 생성하고 두 값을 더해 하나의 값으로 만들고 싶다면 연산자 오버로딩으로 쉽게 해결할 수 있다.
- 연산자 오버로딩을 하기 위해서는 `operator`예약어와 연산자에 맞게 지정된 메소드 명을 사용하여 오버로딩하도록 한다.

```kotlin
data class Coin(
    var five : Int,
    var Ten : Int
){
    operator fun plus(other : Coin) : Coin {
        return Coin(this.five + other.five, this.Ten+other.Ten)
    }
}

fun main(){
    var person1 = Coin(5, 10)
    var person2 = Coin(20, 5)
    //연산자 오버로딩으로 간단히 연산할 수 있게 된다.
    print(person1 + person2)
}
```

### invoke 연산자

- 함수를 호출할때 메소드 이름에 괄호를 붙여 상요하는데
- 글래스 객체도 invoke 연산자를 오버로딩하여 사용가능하다.

```kotlin
class School(val school : String){
    operator fun invoke(grade : Int, name : String) {
        println("${school} 에 다니는 ${grade} 학년 ${name} 입니다.")
    }
}

fun main(){
    val school = School("성포고등학교")
    school(3, "홍길동")
}
```

## null 처리

- 코틀린의 특징 중 하나가 컴파일 시점에서 `NullPointerException`을 처리할 수 있다.
- 객체가 null이 될 수 있게 해주는 `?연산자`와 null을 처리해주는 `?.`, `?:`, `!!` 연산자가 존재한다.

### ?연산자

- ?연산자는 null이 가능한 타입으로 만들어 준다.

```kotlin
fun main(){
    var a : Int = 10
    //a = null 불가능
    var b : Int? = 10
    b = null //가능
    b = a
}
```

- 컴파일 시점에서 `NullPointerException`을 방지해주는데 다음 예로부터 알 수 있다.

```kotlin
fun main(){
    var a : String? = "abcdef"
    println(a.length)	//컴파일 에러발생
}
```

- 변수 a가 null일 수도 있는데 `.length`는 null값이 들어오면 `NullPointerException`이 발생하게 된다.
- 그래서 컴파일 시점에서 해당 코드에 문제가 있다고 알려주게 된다.
- 혹은 미리 null인지 다음과 같이 확인하여 해당 코드를 실행시킬 수 있다.

```kotlin
if(a != null) println(a.length) // 가능
```

- a가 null이 아닌 것을 확인하여 if문 안에 a의 타입은 String으로 스마트 캐스트 되어 `.length`를 사용할 수 있게 된다.

### ?. 연산자

- 위에 예시에서 if문을 안쓰고 `?.`연산자를 이용할 수 있다.

```kotlin
fun main(){
    var a : String? = "abcdef"
    println(a?.length)
}
```

- a가 null이아니라면 다음 코드를 실행하고 아닐 경우 null을 반환한다.

### ?: 연산자

- `?:`연산자는 null이 아닌 경우와 null일 때의 경우의 결과값을 모두 정의하고 반환할 수 있다.

```kotlin
fun main(){
    var a : String? = null
    println(a?.length?:"not found")
}
```

- a가 null이 아니라면 lenght를 실행하고 null일 경우 `?:` 뒤에 코드를 실행하게 된다.

### !!연산자

- `!!`연산자는 해당 값이 null이 아니라는 것을 보장하게 한다.
- 즉 컴파일러가 null체크를 하지 않게 된다.
- 하지만 실제로 해당 값이 null이면 런타임시 `NullPointerException`가 발생한다.

```kotlin
fun main(){
    var a : String? = null
    //a는 null이지만 !!연산자를 통해 컴파일러가 null체크를 하지 않게 된다.
    println(a!!.length)	
}
```

## 가변인자

- 함수 매개변수에 `vararg`예약어를 사용하며 가변인자로 설정 할 수 있다.

```kotiln
fun test(vararg a : Int){
    for(i in a) print(i)
    println()
}
fun main(){
    test(1, 2, 3, 4, 5, 6, 7, 8)
    test(1, 2, 3)
    test(1)
    test()
}
```

