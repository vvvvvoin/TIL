# Doamin layer

도메인 계층은 UI, data 계층 사이에 존재한다. 추가적으로 구글에서 제시하는 아키텍처 가이드에서는 선택사항이다.

<img src="https://developer.android.com/static/topic/libraries/architecture/images/mad-arch-domain-overview.png" />

도메인 계층은 복잡한 비즈니스 로직이나 여러 ViewModel 에서 사용되는 간단한 비즈니스 로직을 캡슐화한 계층이다.

도메인 계층으로 몇가지 이점이 존재한다.

- 코드 중복 제거
- 도메인 레이어를 사용하는 클래스의 가독성 향상
- 앱 테스트 가능성 증가
- 책임을 나눔으로써 로직이 큰 클래스를 제거

클래스를 간단하고 가볍게 유지하는 각 UseCase 는 단일 기능에 대한 책임을 가지게 하고 수정 불가능한(Immutable) 값을 사용하게 해준다.

> 여기서 추천하고 권장하는 방법은 광범위하게 적용될 수 있고, 프로젝트를 더 쉽게 테스트하고 폼질 좋게 해줄 수 있습니다. 그러나 당신이 하는 프로젝트의 요구사항에 맞게 취급해야합니다.



## Naming conventions

이 가이드에서는 useCase 에 대한 이름을 담당하는 단일 행위로 이름을 지정합니다. 컨벤션은 다음과 같습니다.

행위 + 명사/무엇 (Optional) + UseCase

예를 들어 `GetManagerUseCase`, `LongOutUserUseCase`, `UpdateLatestNewsWithAuthorsUseCase` 과 같습니다.



## Dependencies

일반적인 앱 아키텍처에서는 UseCase 는 UI 계층의 ViewModels 과 Data 계층의 Repository 사이에 적합한 클래스입니다. 이 의미는 UseCase 클래스는 일반적으로 Repository 클래스에 의존적이며 Repository 클래스와 같은 방법으로 UI 계층에서도 callback 과 Corotuine 으로 통신합니다. 이에 대한 세부설명은 추후 다른 문서에서 해보겠습니다.

예를 들어, NewsRepository 와 AuthorRepository 로 부터 데이터를 가져오는 UseCase 클래스를 만들어야 한다면 다음과 같이 조합해서 사용할 수 있습니다.

```kotlin
class GetLatestNewsWithAuthorsUseCase(
  private val newsRepository: NewsRepository,
  private val authorsRepository: AuthorsRepository
) { /* ... */ }
```

UseCase 는 재사용가능한 로직이기 때문에 다른 UseCase 에 사용될 수 있습니다. Doamin 계층에서 다양한 수준의 UseCase 를 가지는 것은 일반적입니다. 예를 들어 특정 화면에 TimeZone 이 적용된 적절한 메시지를 표시하기 위해서라면 `FormatDateUseCase` 를 사용하여 UseCase 를 정의할 수 있습니다.

```kotlin
class GetLatestNewsWithAuthorsUseCase(
  private val newsRepository: NewsRepository,
  private val authorsRepository: AuthorsRepository,
  private val formatDateUseCase: FormatDateUseCase
) { /* ... */ }
```

<img src="https://developer.android.com/static/topic/libraries/architecture/images/mad-arch-domain-usecase-deps.png"/>



## Call UseCase in Kotlin

코틀린에서는 `operator` 접근자 중 `invoke()` 메서드를 정의해서 호출할 수 있는 UseCase 클래스 객체를 만들 수 있습니다.

```kotlin
class FormatDateUseCase(userRepository: UserRepository) {

    private val formatter = SimpleDateFormat(
        userRepository.getPreferredDateFormat(),
        userRepository.getPreferredLocale()
    )

    operator fun invoke(date: Date): String {
        return formatter.format(date)
    }
}
```

위 예시처럼 `invoke()` 메서드는 클래스의 객체로 함수인 것처럼 호출할 수 있습니다. `invoke()` 메서드는 특정 매개변수를 받거나 특정 타입을 반환하는 형태같이 제한적이지 않다. `invoke()` 를 오버로드하여 다른 형태로 만들 수 있다. 아래 예시처럼 호출할 수 있습니다.

```kotlin
class MyViewModel(formatDateUseCase: FormatDateUseCase) : ViewModel() {
    init {
        val today = Calendar.getInstance()
        val todaysDate = formatDateUseCase(today)
        /* ... */
    }
}
```

`invoke()` 에 대해 좀 더 자세히 알기 위해서는 [코틀린 문서](https://kotlinlang.org/docs/operator-overloading.html#invoke-operator)을 확인해주세요.



## Lifecycle

UseCase 는 자체적인 생명주기가 없습니다. 대신에 UseCase 가 사용되는 클래스에 맞춰지게 됩니다. 이 말은 UI 계층이나 Service, `Application` 같은 단에서 사용되고 사용한 생명주기에 맞춰진다는 것을 의미합니다. 그리고 UseCase 는 수정 가능한(Mutable) 값을 포함하지 않기 때문에 UseCase 가 사용되는 모든 부분에서 새롭게 객체를 생성해야합니다.



## Threading

Domain 계층의 UseCase 는 반드시 메인 스레드로 부터 안전하게 호출되어야 합니다. 만약 UseCase 가 오랫동안 수행해야하는 작업을 하게 될 경우 적절한 스레드로 변경해야 합니다. 그러나 이런 행동을 하기전에 오랫 동안 수행되는 작업을 다른 계층에 더 잘 배치되도록 해야합니다. 일반적으로 복잡한 계산이 Data 계층에서 발생하므로 재사용성과 캐쉬를 활용해야합니다. 예를 들어 앱에서 여러 화면에서 재사용하기 위해 캐쉬하기 위해서는 리소스가 많이 드는 작업은 도메인보다는 데이터 계층으로 옮겨야 합니다.

아래 예에서는 백그라운드 스레드로 작업을 수행하는 UseCase 입니다.

```kotlin
class MyUseCase(
    private val defaultDispatcher: CoroutineDispatcher = Dispatchers.Default
) {

    suspend operator fun invoke(...) = withContext(defaultDispatcher) {
        // Long-running blocking operations happen on a background thread.
    }
}
```



## Common tasks

#### Reusable simple business logic

UI 계층에 있는 재사용 가능한 비즈니스 로직은 UseCase 로 캡슐화해야합니다. 그러면 해당 로직이 사용되는 부분에서 쉽게 변화를 적용시킬 수 있습니다. 그리고 이런 분리로 해당 로직을 테스트할 수 있게 해줍니다.

위 예로 말한 `FormatDateUseCase` 를 고려해보면 날짜 형식을 취급하는 비즈니스 요구사항이 미래에 바뀌게 된다면 하나의 중앙집권화된 부분을 변경하면 된다. 결과적으로 하나의 재사용 가능한 유즈케이스가 잘 정의되어 있다면 요구사항 변경 대응에 쉬워지게 됩니다.

> 위 예제는 static 한 Util 클래스를 만들어서 대체할 수 있습니다. 그러나 Util 클래스는 매번 찾기 어렵고 기능도 알아내기 어렵기 때문에 추천하지는 않습니다. 게다가 UseCase 는 base 클래스를 스레드, 에러 처리와 같은 공통 기능을 공유하여 큰 규모의 프로젝트에 도움이 될 수 있습니다.

#### Combine repositories

만약 당신이 뉴스 앱을 만들고 있다고 한다면 Data 계층에는 `NewsRepository`, `AuthorsRepository` 가 있을 것입니다. `NewsRepository` 에서 가져올 수 있는 `Article`  모델 클래스에 저자의 대한 이름만 포함하지만 요구사항에 따라 저자에 대한 정보도 필요로할 수 있습니다. 저자의 대한 정보는 `AutorsRepository` 로 부터 얻을 수 있을 것입니다.
<img src="https://developer.android.com/static/topic/libraries/architecture/images/mad-arch-domain-multiple-repos.png" />

다양한 Repository 를 사용하는 로직은 복잡해지게 때문에 `GetLatestNewsWithAuthorsUseCase` 라는 클래스를 만들어서 ViewModel 에서 추상화하여 좀 더 가독성을 높일 수 있습니다. 이런 분리로 테스트를 좀 더 쉽게 만들고 다른 기능에서 재사용할 수 있게 해줍니다.

```kotlin
/**
 * This use case fetches the latest news and the associated author.
 */
class GetLatestNewsWithAuthorsUseCase(
  private val newsRepository: NewsRepository,
  private val authorsRepository: AuthorsRepository,
  private val defaultDispatcher: CoroutineDispatcher = Dispatchers.Default
) {
    suspend operator fun invoke(): List<ArticleWithAuthor> =
        withContext(defaultDispatcher) {
            val news = newsRepository.fetchLatestNews()
            val result: MutableList<ArticleWithAuthor> = mutableListOf()
            // This is not parallelized, the use case is linearly slow.
            for (article in news) {
                // The repository exposes suspend functions
                val author = authorsRepository.getAuthor(article.authorId)
                result.add(ArticleWithAuthor(article, author))
            }
            result
        }
}
```

위 로직은 `news` 목록에 모든 아이템을 나타냅니다. 그래서 Data 계층은 메인 스레드에 안전하게 동작해야 합니다. 왜냐하면 얼마나 많은 아이템을 가져와서 처리할 줄 모르기 때문입니다. 그래서 `default dispatcher` 를 사용하여 백그라운드에서 처리할 수 있도록 한 것입니다.



## Other consumers

UI 계층으로부터 떨어트려 놓은 것은 Domain 계층이 Service 나 Application 클래스같은 여러 클래스로 부터 재사용할 수 있게 해줍니다. 게다가 TV 나 Wear 같은 플랫폼에서 앱과 같은 코드베이스를 사용할 수 있게 한다면, UI 계층은 앞서 언급한 Domain 계층의 모든 이점을 얻기 위해 UseCase 를 재사용 할 수 있습니다.



## Data layer acces restriction

Domain 계층을 구현할 때 고려해야 할 또 다른 사항은 UI 계층으로 Data 계층에 대한 직접 접근을 허용해야하는지 아니면 Domain 계층을 통해 강제로 모든 것을 받을지를 허용해야하는지 여부입니다.

<img src="https://developer.android.com/static/topic/libraries/architecture/images/mad-arch-domain-data-access-restriction.png" />

이런 제한의 장점은 UI 계층이 Domain 계층을 무시하지 않도록 방지하는 것입니다.

그러나 잠제적인 중요한 단점은 Data 계층으로부터 간단한 함수를 추가할 때마다 UseCase 를 추가해야하는 점이며, 이는 복잡한을 증가시켜 이점이 얻을 수 없다.

필요할 때에 UseCase 를 추가하는 것은 좋은 접근 방법이다. UI 계층이 독점적으로 UseCase를 통해 data 를 접근한다면 이는 합리적일 수 있습니다.

궁극적으로 Data 계층에 대한 접근 제한은 개별 코드베이스와 엄격한 규칙을 선호하는지 아니면 보다 유연한 접근 방식을 선호하는지에 따라 결정된다.



## Testing

[일반적인 테스트 가이드라인](https://developer.android.com/training/testing)은 Domain 계층을 테스트할 때 적용된다. UI 테스트에는 개발자가 일반적으로 fake repository 를 사용한는데 이는 Domain 계층을 테스트할 때에서 fake repository 를 사용하는 것이 좋습니다.







### References

https://developer.android.com/topic/architecture/domain-layer#lifecycle
