# Kotlin -  class

- 코틀린에는 data class, enum class, sealed class가 존재한다.

## data class

- data class는 데이터를 담는 클래스이다.
- VO 클래스와 기능이 같다
- 하지만 코틀린에서의 data class를 선언해주면 다음 기능을 자동적으로 추가해준다
  - getter/setter
  - toString, hashCode, equals 오버라이딩
- 다음과 같이 data class를 만들 수 있다

```kotlin
data class Student(
	val index : Int,
    var name : String? = null,
    var number : String
)
```

- 그리고 data class는 상속할 수 없으며 모든 생성자에는 val, var이어야 한다.

## enum class

- 기존 C와 JAVA에서의 enum과 같은 기능을 한다.

```kotlin
enum class Status { 
    SUCCESSFUL, ERROR, LOADING 
}

//다음과 같이 data class와 같이 사용할 수 있다
data class Data<T>(
    var responseType: Status,
    var data: T? = null,
    var error: Exception? = null
)
```

## sealed class

- sealed class는 여러 클래스를 하나로 묶은 클래스이다.

- 다음과 같이 만들 수 있다.

```kotlin
sealed class Result<out R > {
    class Success<out T >(val data: T) : Result<T>()
    class Failure(val exception: String) : Result<Nothing>()
}

....

when(someData){
	is Result.Success -> {
		//sucess처리
	}
	is Result.Failure -> {
        //failure처리
	}
}
```

- `Result` sealed class에 Success, Failure 두가지의 클래스가 들어 갔다
- 그리고 someData가 어떤 Result의 클래스로 들어올지 구분하여 값을 처리해 줄 수 있다.
- 하지만 sealed class가 아닌 inner class로도 처리할 수 있는데 왜 사용할까?
  - inner class를 사용할때 when에서는 컴파일러에게 해당 값에 올 수 있는 경우에 대해 모두 처리를 해줘야한다.
    - else문을 만들어 줘야한다.
  - 하지만 sealed class로 하게 될 경우 컴파일러가 when에 올 수 있는 경우를 예측할 수 있어 처리에 용이하다.