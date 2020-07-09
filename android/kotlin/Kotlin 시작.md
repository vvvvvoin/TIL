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

### for and while
- for문을 이용하여 어레이리스트 값을 출력
```kotlin
fun forAndWhile(){
    val students = arrayListOf("kim", "seo", "cho")
    for(name in students){
        println("${name}")
    }
    
    //for문에 withIndex메소드를 이용하여 순서를 매핑시킬 수 있다
    for((index, name) in students.withIndex()){
        println("${index+1}번째 학생 이름은 ${name}입니다")
    }
    //1번째 학생 이름은 kim입니다
	//2번째 학생 이름은 seo입니다
	//3번째 학생 이름은 cho입니다
    
    //1 부터 10 까지 순차적으로 누적시키기
    var sum : Int = 0;
    for(i in 1..10){
        sum += i
    }
    
    //1 부터 10 까지 2번씩 끊어서 누적시키기
    var sum : Int = 0;
    for(i in 1..10 step 2){
        sum += i
    }
    
    //10부터 1까지 순차적으로 누적시키기
    //10..1은 안됨
    var sum : Int = 0;
    for(i in 10 downTo 1){
        sum += i
    }
    
    //1부터 99까지 순차적으로 누적시키기
    var sum : Int = 0;
    for(i in 1 until 100){
        sum += i
    }
}
```
- while은 기존 문법과 유사하다
```kotlin
fun forAndWhile(){
	var index = 0;
	while(index < 10){
		println("현재 값 = ${index}")
		index++
	}
}
```

### Nullable and NonNull
```kotlin
fun nullCheck(){
    var name = "vvvvv"

    // ?
    //non-null type인 스트링에 null 값을 대입못하므로
    var nulllName1 : String = null //오류
    //? 연산자를 통해 Nullable로 변환한다
    var nullName2 : String? = null

    //일반적인 스트링 타입을 대문자로 변환하는 메소드
    var nameUpperCase = name.toUpperCase()
    //하지만 String값을 받는 nullNmaeUpperCase1 가 non-null String 이기에 대입못함
    var nullNmaeUpperCase1  = nullName2.toUpperCase() //오류
    //? 연산자를 사용하여 null이면 null반환 null이 아니면 메소드를 실행
    var nullNmaeUpperCase2  = nullName2?.toUpperCase()


    // ?:
    //lastName이 null이면 "No lastName"를 반환 null아 아니라면 lastName 대입
    var lastName : String? = null
    var fullName = name + lastName?:"No lastName"

}

fun ignoreNUll(str : String?){
    //str은 nullable타입이 들어와 non-null 타입인 String에 대입될수 없다
    var notNull1 :String = str   //오류
    //하지만 !! 연산자를 씀으로서 String 타입인 것을  보증해줄 수 있다
    var notNull2 :String = str!!

    var address  : String? = "abcedfg"
    //address가 null이 아닐 경우 let함수를 실행
    address?.let {
        println(address)
    }

}
```

### class

```kotlin
fun main(){
    var person = Person()
    person.hello()
}

class Person{
    var name :String = "vvvvv"
    fun hello(){
        println("hello ${name}")
    }
}
```
- 클래스 이름옆에 생성자를 추가할 수 있다.
```kotlin
fun main(){
    var person = Person("vvvvv")
    person.hello()
}

class Person constructor(name : String){
    var name = name
    fun hello(){
        println("hello ${name}")
    }
}
```
- 생성자를 생략하고 사용가능하다
```kotlin
fun main(){
    var person = Person("bi")
    person.hello()
}

class Person (name : String){
    var name2 = name
    fun hello(){
        println("hello ${name2}")
    }
}
```
- 생성자에서 name값이 지정없이 Person객체가 생성되면 기본값으로 vvvv가 매핑된다
```kotlin
fun main(){
    var person = Person()
    person.hello()
}

class Person (name : String = "vvvvv"){
    var name2 = name
    fun hello(){
        println("hello ${name2}")
    }
}
```
- init()라는 메소드를 이용하여 객체가 만들어짐과 동시에 실행되는 주 생성자로 볼 수 있다
- 주 생성자와 마찬가지로 부생성자도 존재하는데
- 따로 클래스내부에 constructor를 이용하여 정할 수 있다
- 부생성자 옆 this는 주생성자의 name을 위임을 받아야한다
	- 위임받지 않을 경우 결과
	- "객체가 만들어짐과 동시에 실행됩니다"
	- "이름은 감자이고 나이는 55 이도다"
	- "hello vvvvv"
- name을 위임받지 않았기에 부생성자에서 name객체는 name2로 매핑될 수 없게된다
```kotlin
fun main(){
    var person = Person("감자", 55)
    person.hello()
}

class Person (name : String = "vvvvv"){
    init {
        println("객체가 만들어짐과 동시에 실행됩니다")
    }

    constructor(name : String = "vvvvv", age : Int = -1) : this(name){
        println("이름은 ${name}이고 나이는 ${age} 이도다")
    }

    var name2 = name
    fun hello(){
        println("hello ${name2}")
    }
}
```



### 접근제어
- public이 기본적으로 사용
- private은 정의된 파일 내부에서만 볼 수 있음
- internal은 동일한 모듈의 모든 곳에서 볼 수 있음
- protected는 최상위 선언에는 사용할 수 없음

### 모듈
- 모듈은 함꼐 컴파일 된 Kotlin파일 세트
- IntelliJ IDEA module, maven project, gradle source set.....

### 비교연산자
- '==' 실제 값을 비교해서 동일함을 비교
- '===' 주소값을 비교해서 동일함을 비교

### 상속
- 클래스 선언무에 open이 있어야 선언될 수 있고
- 상속받는 클래스 또한 open이 있어야 한다.





































































