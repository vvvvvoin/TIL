# RxJAVA Map을 이용하여 받아오 데이터 처리하기

- RestAPI를 사용하다보면 요청에 맞는 응답으로 정상적으로 처리되거나 오류가 발생할 수 있다.
- 그리고 데이터를 확인할때 해당 데이터가 오류가 발생했는지 구분을 해줘야한다.

- 이를 Mapper와 sealed class를 이용하여 기존에 받은 결과의 성공, 실패 여부를 확인하여 map을 통해 데이터를 타입에 맞게 반환시키는 것을 해본다.

## sealed class

- RestAPI의 성공과 실패 여부를 구분하기 위해 sealed class를 만든다.

```kotlin
sealed class Result<out R > {
    class Success<out T >(val data: T) : Result<T>()
    class Failure(val exception: String) : Result<Nothing>()
}
```

## Mapper

- map() 메소드에 사용될 mapper 두 가지를 만든다.

### abstract mapper

- 우선 추상 매퍼 클래스를 다음과 같이 선언한다.
- RestAPI에서 리턴타입을 Rsponse로 받아 성공여부와 서버 오류를 구분하여 처리할 수 있도록 한다.
- 여기서는 retrofit의 response를 받는다.

```kotlin
abstract class NetworkMapper<R> {
    fun map(data: retrofit2.Response<R>): Result<R> {
        // 받은 data가 성공이면 해당 body(내용물)을 mapTo 메소드로 처리
        return if (data.isSuccessful) {
            data.body()?.let {
                mapTo(it)
            } ?: run {
                Result.Failure("server")
            }
        } else {
            Result.Failure("network")
        }
    }

    abstract fun mapTo(data: R): Result<R>
}
```

### object mapper

- 그리고 추상 클래스를 구현한 object를 만든다.
- mapTo 실제 사용될 데이터의 타입에 맞게 작성한다.

```kotlin
object LogDataMapper : NetworkMapper<String>() {
    override fun mapTo(data: String): Result<String> {
        return if (data.isNotEmpty()) {
            Result.Success(data)
        } else
            Result.Failure("server")
    }
}
```

## Service

- abstract mapper를 만들때 Response타입으로 값을 반환시킨다.

```kotlin
interface MyService {
@GET("EarthCommunity/doorDataTransform")
fun getLogData( @Query("token") token: String) : Single<Response<String>>
```

## DataSource

```kotlin
fun getLogData(token : String): Single<Result<String>> {
    return api.getLogData(token).map(LogDataMapper::map)
}
```

- Retrofit객체를 정의 후 `MyService`는 `Single<Response<String>>` 을 반환하게 되있다
- 하지만 map을 통해 반환 타입은 `Result`라는 sealed class로 바뀌게 된다.
- 이후 기존 RxJava와 retrofit 처리에서 Result의 클래스를 when으로 분류하여 처리할 수 있다.

```kotlin
when(it){
	is Result.Success -> {
		_logData.value = it.data!!
	}
	is Result.Failure -> {
        //예외처리
		it.exception
	}
}
```



