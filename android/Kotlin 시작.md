## Kotlin 시작

- 코틀린은 메인함수는 다음과 같다
```kotlin
fun main(){

}
```

### 함수
- 기존 자바와는 다른 것을 볼 수 있다

Kotlin
```kotlin
fun helloWorld() : Unit{
	println("hello world")
}
```
Java
```java
void hellodWorld(){
	Sysatem.out.println("hello world");
}
```
- 우선 리턴타입이 아닌 fun이라는 값으로 함수를 나타낸다
- fun 다음은 함수명이 오고
- 리턴 타입이 void인 경우 함수명 다음 ": Unit"을 붙인다 (void 타입일 경우 생략가능)
- 파라미터가 있는 함수의 경우 다음과 같다.
Kotlin
```kotlin
fun add(a : Int, b : Int) : Int{
	return a + b;
}
```
Java
```java
int add(int a, int b){
	return a + b;
}
```
- 코틀린에 경우 파라미터에 변수명이 먼저나오고 타입이 뒤에 나타난다.
- 리턴 타입은 Int이므로 반드시 기재해준다
- 또한 코틀린은 자바에서의 int가 Int로 되어있다

### var, val

- val은 변할 수 없는 변수, 상수와 같다(= final)
```kotlin
fun test(){
	val a : Int = 100
	// val은 상수이므로 다음 코드는 오류가 발생한다
	a = 200
}
```
- var은 변할수 있는 변수이다
```kotlin
fun test(){
	var b : Int = 100
	a = 200
	
	//코틀린은 타입을 알아서 지정해주기에 
	//var c : Int = 100을 다음과 같이 쓸 수 있다.
	//val도 마찬가지
	var c = 100
	
	//스트링도 마찬가지다
	var name = "vvvvvoin"
}
```
- 단 var다음 만드시 타입을 정해줘야하는 경우는 값을 바로 지정해주는 것이 아닌 경우다

### String Template
- EL식과 같은 사용방법을 같는다

```kotlin
fun main(){
	val name = "vvvvvoin"
    println("my name is $name and I'm good")
    println("my name is ${name} and I'm good")
    println("my name is ${name}and I'm good")
	
}
```
- 같은 의미이지만 출력은 다음과 같다
```
my name is vvvvvoin and I'm good
my name is vvvvvoin and I'm good
my name is vvvvvoinand I'm good
```
- {}를 사용하여 구분하는것이 편리하다
- $단어를 쓰기 위해서는 "\" 사용하여 처리한다.
```kotlin
fun main(){
    println("this is 2\$s")

}
```
- {}안에 간단한 boolean 처리도 가능하다
```kotlin
fun main(){
    println("is this true ${1 == 0}")

}
```

### 조건식
- 코틀린에서도 일반적인 조건식을 다음과 같이 쓸 수 있다
```kotlin
fun maxWho(a : int, b : int) : int{
	if(a > b){
		return a
	}else{
		return b
	}
}
```
- 코틀린에서는 다음과 같은 간결한 형식으로도 표현이 가능하다.
```kotlin
fun maxWho2(a : Int, b : Int) = if(a>b) a else b
```
- 코틀린에서는 조건식으로 when이 새롭게 등장한다

```kotlin
fun checkNum(score : Int){
	when(score){
		0 -> println("0 입니다")
		1 -> println("1 입니다")
		2, 3 -> println("2 또는 3 입니다")
		//else는 반드시 작성하지 않아도 된다
		else -> println("모르겠습니다")
	}
}
```
- case문과 유사하지만 좀더 간편하게 사용이 가능하다
- 복수의 값도허용이 된다
- 또한 변수에 값을 지정할 수 있다
```kotlin
	var a = when(score){
		1 -> 3
		2 -> 50
		//이때에는 반드시 else를 넣어 변수 값을 지정해줘야 한다.
		else -> 444
	}
```
- 또한 숫자의 지정 범위가 광범위 할때 다음과 같이 해결한다.
```kotlin
	when(score){
		in 90..100 -> println("best")
		in 0..80 -> println("good")
		//이때에 else는 81~89사이의 값이다
		else -> println("good")
	}
```

### Array, List
- 어레이와 리스트는 자바와 다르게 선언이 된다
- 선언은 arrayOf, listOf로 선언한다
- 만약 값들이 Int, String등 다양하게 섞여있으면 any 타입으로 지정된다
```kotlin
fun arrayAndList(){
    val array = arrayOf(1, 2, "aaa")
    val list = listOf(1,  2, 44, "abce")

    array[0] = 3
    
    //list로 선언할 경우 mutableList가 아니라 읽기 전용이기에 값을 수정하지 못한다.
	list[1] = 3 //오류발생
	// 읽기 전용이기에 get을 통해서 값을 매핑할 수는 있다.
    var value = list.get(1)    
    
    //list에는 mutableList가 대표적으로 arrayList이다
    //읽기, 쓰기 모두 가능하다
    val arrayList = arrayListOf<Int>()
    arrayList.add(30)
    arrayList.add(40)
    //값 대입도 가능하다
    arrayList[0] = 20
}
```





















































































