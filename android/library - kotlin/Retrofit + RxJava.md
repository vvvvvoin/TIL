## Retrofit + RxJava
- 기존에 만든 Retrofit을 참고하길 바란다
### dependencies
```
implementation 'com.squareup.retrofit2:retrofit:2.6.2'
implementation 'com.squareup.retrofit2:converter-gson:2.6.2'
implementation 'com.squareup.retrofit2:adapter-rxjava2:2.6.2'
implementation 'io.reactivex.rxjava2:rxandroid:2.1.1'
implementation 'io.reactivex.rxjava2:rxjava:2.2.13'
```
### Interface
- 기존의 인터페이스
```kotlin
interface kakao {
    @GET("/kakao/introduce/vision")
    fun getData() : Call<String>
}
```
- Rxjava + retrofit
```kotlin
interface kakao {
    @GET("/kakao/introduce/vision")
    fun getData() : Single<String>
}
```
- 원래는 `Call<T>` 형태의 비동기 결과객체를 반환받는데 adapter-rxjava2를 추가하였기 때문에 ReactiveX에서 제공하는 Observable의 한 종류변환하여 반환할 수 있습니다. ([출저](https://eclipse-owl.tistory.com/24))
- 기존의 인터페이스 사용법과 유사하다

### 구현
```kotlin
val retrofit: BoardService = Retrofit.Builder()
            .baseUrl("http://175.196.190.80:8080/")
            .addConverterFactory(GsonConverterFactory.create())
            .addCallAdapterFactory(RxJava2CallAdapterFactory.create())//새롭게 추가된 코드
            .build()
            .create(BoardService::class.java)

retrofit.getData()
			.subscribeOn(Schedulers.io())
			.observeOn(AndroidSchedulers.mainThread())
			.subscribe({item ->
				Log.d(TAG, "성공")
				Log.d(TAG, item.toString())
			}, { throwable ->
				Log.d(TAG, "실패")
				Log.d(TAG, throwable.toString())
			})
```

- Retrofit생성시에 addCallAdapterFactory 설정을 추가한다
- retrofit의 getData() 메소드를 실행할때
  - 네트워크 통신시 UI Thread를 이용할 경우 오류가 발생하기에 subscribeOn()을 통해 Single 연산을 처리할 IO Thread를 설정
  - 네트워킹 실패, 성공을 처리할 subscribe() 메소드를 통해 UI에 전달하기 위해 observeOn()의 매핑값을 AndroidSchedulers.mainThread()로 설정
  - ReactiveX에서 사용될 Scheduler는 다양한 종류가 있고 [여기](http://reactivex.io/documentation/ko/scheduler.html)를 참조한다
  - subscribe 내부에 네트워킹 처리의 성공과 실패에 대해 처리한다

