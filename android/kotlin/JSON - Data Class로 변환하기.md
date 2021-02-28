# JSON -> Data Class로 변환하기

- 모바일에서 Restful API를 이용하여 다양한 데이터를 받고 안드로이드에서 다룰 수 있는 VO, DTO, DataClass형태로 변환시켜줘야 한다.
- 이때 보통 GSON을 사용하여 변환하게 된다.
- GSON을 사용하기 위해서는 JSON을 VO객체로 반환될 수 있도록 정확한 구조와 이름으로 정의되야한다.

## 사용법

<div><img src="https://user-images.githubusercontent.com/58923717/108966713-dc329400-76c1-11eb-9f1d-a5cd8cea6ba7.JPG"</div>

- 위 사진의 JSON을 변환해본다.
- data class를 정의하는데 이는 사용자가 원하는 아무 클래스 이름을 정의하면 된다.

```kotlin
data class SampleData()
```

- JSON에 처음항목이 `response`항목이 보이고 다음에 `{` 중괄호로 다음 데이터가 여러개 있다.
- 이는 `response`라는 항목이 `numFound`, `start` 등의 다른 항목을 갖는 것을 의미한다.
- 다음과 같이 data class를 정의할 수 있다.

```kotlin
data class SampleData(
    var response : Response
){
    data class Response(
        var numFound : Int,
        var start : Int,
        var maxScore : Double,
        var docs : ArrayList<Docs>
    )
}
```

- `Response`라는 data class를 `{}`내부에 새롭게 정의할 수 있다.
- 여기서 docs항목은 `List`타입으로 정의 되었는데 이를 쉽게 구분할 수 있는 방법은 `docs`항목 다음에 값이 `[` 대괄호에 위치하면 이는 리스트형태로 표현된다는 것을 의미한다.
- `docs`는 `id`, `journal` 등의 항목을 갖고 있으므로 `Response` data class 내부에(`{}`) 다시 `docs` data class를 다음과 같이 만든다.

```kotlin
data class SampleData(
    var response : Response
){
    data class Response(
        var numFound : Int = 0,
        var start : Int = 0,
        var maxScore : Double = 0.0,
        var docs : ArrayList<Docs>
    ){
        data class Docs(
            var id : String,
            var journal : String,
            var eissn : String,
            var publication_date : String,
            var article_type : String,
            var author_display : ArrayList<String>,
            var abstract : ArrayList<String>,
            var title_display : String,
            var score : Double
        )//end Docs
    }//end Response
}// end SampleData
```

- `author_display`항목은 눈으로 봐도 여러 개의 데이터가 일렬로 위치한 것을 통해 쉽게 List타입으로 묶어야 한다는 것을 알 수 있다.
- 하지만 `abstract`항목 또한 `[`대괄호로 시작하므로 List타입으로 만들어줘야 한다.
- `[`대괄호를 보지 못하고 String으로 변환하면 다음과 같은 오류가 발생한다.

> com.google.gson.JsonSyntaxException: java.lang.IllegalStateException: Expected a string but was BEGIN_ARRAY at line 15 column 21 path $.response.docs[0].abstract

- 배열이나 List타입으로 시작한다는 것을 알려준다.

## 결론

- 변환하는데 있어서 몇가지 주의사항만 알고 있다면 kotlin에서 제공하는 data class로 쉽게 변환할 수 있다.
- `[`대괄호로 시작하는 항목을 놓치지 않는다면 변환하는데 큰 무리가 없을 것이다.
- 또한 json 항목과 data class에서 정의하는 이름과 반드시 동일해야한다.
- 크롬 확장프로그램에서 JSON을 보기 좋게 변환해주는 프로그램이 있다면 보기 편할 것이다.

## 추가

- 하나의 data class에 여러 data class가 필요하다면 다음과 같이 하면 된다.

```kotlin
data class SearchData(
    var meta : Meta,
    var documents : ArrayList<Documents>
){
    data class Meta(
        var total_count : Int,
        var pageable_count : Int,
        var is_end : Boolean
    )//end Meta
    data class Documents(
        var authors : ArrayList<String>,
        var contents : String,
        var datetime : String,
        var isbn : String,
        var price : Int,
        var publisher : String,
        var sale_price : Int,
        var status : String,
        var thumbnail : String,
        var title : String,
        var translators : ArrayList<String>,
        var url : String
    )//end Documents
}//end SearchData
```

- `meta`, `documents` data class를 동시애 내부에 정의할 수 있다.

### NumberFormatException

- 파싱하면서 `NumberFormatException`가 일반적으로 발생하는 이유는 data class에는 정수값으로 저장하고 JSON항목이 존재할때는 정수이지만 해당 항목에 값이 없을 때는 이를 내부적으로 Integer.pareseInt("")를 하기 때문에 Exception이 발생한다.
  - data class의 값을 String타입으로 변환하면 해결됨