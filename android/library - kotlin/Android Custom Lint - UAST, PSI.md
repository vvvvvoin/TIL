# Android Custom Lint - UAST, PSI

## UAST? PSI?

- 소스코드 표현이 어떻게 구현되어 있는지에 대한 정보를 갖고 있고 이를 기반으로 소스코드에서 Lint를 해줄 부분들을 정의할 수 있게 해준다.

### UAST (Universal Abstact Syntax Tree)

Java/Kotlin이 상관없이 하나의 표현식으로 나타낼 수 있는 구조로 만들어 준다.

기본적인 것은 Abstact Syntax Tree와 유사하고, Java/Kotlin을 모두 처리할 수 있어 Universal이 붙는다.

[추상 구문 트리 - 위키백과, 우리 모두의 백과사전](https://ko.wikipedia.org/wiki/추상_구문_트리)

<img src="https://user-images.githubusercontent.com/58923717/132084270-f6c66743-a005-475b-90ab-31b50b8e2ce4.png">

### PSI (Program Structure Interface) - 적극 사용 권장

- IntelliJ에서 만든 모든 언어 모델링에 사용될 수 있는 AST 추상화 구조이다.
- UAST는 단순하게 문법적 구조만 제공하지만 PSI 는 보다 세부적인 언어의 특정정보를 제공해준다.
- 어떤 클래스에 속해있는지? 리턴 타입, 파라미터가 어떻게 되는지? 공백이 있는지?와 같은 보다 세부정보를 파악할 수 있음
  - class가 private, inner, enum 등 이 있는지 여부, 메서드간 간격이 얼마나 되는지와 같은 세부정보까지 알 수 있다.
- 실제 다음코드가 어떻게 표현되는지 plugin PSIViewer로 확인해보자
  - plugins에서 받으면 우측 상단 Gradle탭 하단에 새롭게 PsiViewer 탭이 생김

[PSI Viewer | IntelliJ IDEA](https://www.jetbrains.com/help/idea/psi-viewer.html)

<img src="https://user-images.githubusercontent.com/58923717/132084290-0c1e0149-79ec-4098-bd83-d07ac154776a.png">

- 가장 안쪽의 자식 노드의 DOT_QUALIFIED__EXPRESSION 내부 부터 차근차근 들여다 보자
  - PEFERENCE_EXPRESSION → App
    - PsiElement(IDENTIFIER)
  - PsiElement(Dot) → .
  - CALL_EXPRESSION → getService()
    - PEFERENCE_EXPRESSION → PsiElement(IDENTIFIER)
    - VALUE_ARGUMENT_LIST → PsiElement(LPAR), PsiElement(RPAR)
  - PsiElement(Dot) → .
  - CALL_EXPRESSION → touch()
  - PsiElement(Dot) → .
  - CALL_EXPRESSION → call()
  - PsiElement(Dot) → .
  - CALL_EXPRESSION → bind()
- 위와 같이 표현되고 있고 각 expression에는 자식 expression이 존재할 수도 있다. (PsiElement같은) 이러한 구조가 트리 형태로 클래스 전체를 표현할 수 있다.
- call_expression 이 메서드를 사용하는 것을 알 수 있다.
- 이러한 것을 기반으로 psiViewer를 통해 정보를 확인하고 원하는 커스텀 린트를 만들 수 있다.

## 결론

- PSI 뷰어를 이용한다면 기존 코드를 분석하는데 큰 도움이 된다.
- 여려 형태의 코드스타일에 대응할 수 있고 커스텀 린트를 만드는데 필수적이다.