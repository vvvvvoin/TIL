# Android Custom Lint

## Lint 린트?

린트를 사용하면 구조적 문제로 인해 Android 앱의 안정성과 효율성에 영향을 미치거나 코드 관리에 지장을 줄 가능성이 있는 코드를 찾을 수 있습니다.

예를 들어 XML 리소스 파일에 사용되지 않는 네임스페이스가 있다면 공간을 차지하고 불필요한 처리가 발생합니다. 지원 중단된 요소 또는 타겟 API 버전에서 지원하지 않는 API 호출의 사용과 같은 다른 구조적 문제가 발생하는 경우 코드가 올바르게 실행되지 않을 수 있습니다. 린트를 사용하면 이런 문제를 해결할 수 있습니다

> [이 문서](https://developer.android.com/studio/write/lint?hl=ko)를 한 번 읽고 와주세요.



이 문서에서는 린트가 무엇인지 보다는 어떻게 커스텀 린트를 만드는지에 대해 설명한다.



## Lint 구성

린트 구현하기 위해서는 크게 3가지 요소와 개념에 대해 알아야할 필요하다.

### 1 .IssueRegistry

- 이슈 레지스트리에서 자신이 원하는 이슈를 등록시킬 수 있다.
- api, issues를 override를 해야함
  - api: Int → The Lint API version this issue registry's checks were compiled.
  - issues: List\<Issue> → The list of issues that can be found by all known detectors.

### 2. Issue

이슈는 7가지 구성 요소를 갖는다.

- id : 이슈 고유의 식별 문자열
- brefDescription : 이슈에 대한 간단 요약 설명
- explanation : 이슈에 대한 전체적인 설명
- category : 이슈와 연관된 카테고리
  - Lint, Correctness, Security, Performance, Usability, Accessibility 등등
- priority : 이슈의 우선순위
- severity : 이슈의 심각도
  - FATAL, ERROR, WARNING, INFORMATIONAL, IGNORE
- implementation : 이슈를 검출하는 비즈니스 로직을 포함한 디텍터와 스코프를 지정함
  - 스코프 → 디텍터의 관심사

### 3. Detector

- 실제 이슈를 감지하는 로직을 담고 있다.

- 디텍터의 호출 순서

  1. Manifest Files
  2. Resource Files
  3. Java Sources
  4. Java Classes
  5. Gradle Files

  ...

- 디턱터의 관심사를 지정해 원하는 파일을 확인할 수 있도록 한다.

  - XmlScanner - xml 파일
  - SourceCodeScanner - java/kotlin 파일
  - ClassScanner - .class 파일
  - BinaryResourcesScanner - 리소르 파일
  - ResourceFolderScanner - 리소스 폴더
  - GradleScanner - gradle
  - Detector.UastScanner - Uast tree 검사





## 구현

- TextView, ImageView를 사용하면 AppCompatTextView, AppCompatImageView를 사용하라고 알려주고 수정할 수 있는 커스텀 린트를 만들어보자.

### 모듈 생성

- 린트가 사용될 모듈을 하나 생성할 수 있도록 한다.

  java / kotlin libaray를 선택

  <img src="https://user-images.githubusercontent.com/58923717/132083829-428babd8-dec6-4d2e-9a1d-194599c99687.png">

- 생성된 모듈의 build.gradle을 수정해 준다.

```groovy
plugins {
    id 'java-library'
    id 'kotlin'
}

java {
    sourceCompatibility = JavaVersion.VERSION_1_8
    targetCompatibility = JavaVersion.VERSION_1_8
}

dependencies {
    implementation fileTree(dir: 'libs', include: ['*.jar'])

    compileOnly "org.jetbrains.kotlin:kotlin-stdlib-jdk8:$kotlin_version"
    compileOnly "com.android.tools.lint:lint-api:27.1.2"
    compileOnly "com.android.tools.lint:lint-checks:27.1.2"

    testImplementation "com.android.tools.lint:lint:27.1.2"
    testImplementation "com.android.tools.lint:lint-tests:27.1.2"
    testImplementation "junit:junit:4.13"
}

jar {
    manifest {
        attributes("Lint-Registry-V2": "com.zoyi.channel.desk.check.IssueRegistry")
    }
}

```

- lint 라이브러리 버전은 Gradle plugin version 과 맞춰야 한다.

   (AGP는 "command + ; → project" 로 확인)

  - 만약 Gradle plugin version이 X.Y.Z이라면 린트 라이브러리 버전은 X+23.Y.Z가 되야 한다.
  - 즉, 7.0.0-alpha08을 사용한다면 30.0.0-alpha08을 사용하면 된다.

- Gradle 버전은 자바 버전과 연관되어 있으므로 잘 처리해줘야 한다.

- 아래 링크로 프로젝트 구조에 맞는 gradle버전을 알아야 한다.

> [Compatibility Matrix](https://docs.gradle.org/current/userguide/compatibility.html)

### 이슈, 이슈 레지스트리

- 이슈는 일반적으로 사용되는 디텍터 내부에 작성된다.
- 이슈와 이슈 레지스트리를 작성한다.
- 우선 이슈는 디텍터에서 관리해줄 수 있도록 먼저 Detector를 상속받고 소스코드 검사에 사용되므로 Scanner를 implement할 수 있도록 한다.

```kotlin
class AppCompactDetector : LayoutDetector() {
    companion object {
        val ISSUE = Issue.create(
                id = "appCompact",
                briefDescription = "you have to use appCompact",
                explanation = "you have to use appCompact",
                moreInfo = "",
                category = Category.CORRECTNESS,
                priority = 5,
                severity = Severity.ERROR,
                implementation = Implementation(AppCompactDetector::class.java, Scope.RESOURCE_FILE_SCOPE)
        )
		}
}
```

- 레이아웃 디텍터를 구현하고 implementatino의 scope를 Scope.RESOURCE_FILE_SCOPE 로 지정하였다.

  - 만약 SourceCodeScanner를 구현할 때 Scope.JAVA_FILE_SCOPE를 지정하게 될 것이다.

  ```kotlin
  implementation = Implementation(AppCompactDetector::class.java, Scope.JAVA_FILE_SCOPE)
  
  enum class Scope {
  	@JvmField
  	val JAVA_FILE_SCOPE: EnumSet<Scope> = EnumSet.of(JAVA_FILE)
  	/*
  	The analysis only considers a single Java or Kotlin source file at a time.
  	Issues which are only affected by a single Java/Kotlin source file can be
  	checked for incrementally when a Java/Kotlin source file is edited.
  	*/
  	JAVA_FILE
  ```

  - Java / Kotlin 모두 호환되는 것을 확인 할 수 잇다.

- 이제 린트가 무엇을 관심 갖을 지를 지정하고 언제, 무엇을 정해야한다.

```kotlin
class AppCompactDetector : LayoutDetector() {
    companion object {
        val ISSUE = Issue.create(
                id = "appCompact",
                briefDescription = "you have to use appCompact",
                explanation = "you have to use appCompact",
                moreInfo = "",
                category = Category.CORRECTNESS,
                priority = 5,
                severity = Severity.ERROR,
                implementation = Implementation(AppCompactDetector::class.java, Scope.RESOURCE_FILE_SCOPE)
        )

        const val IMAGE_VIEW = "ImageView"
        const val TEXT_VIEW = "TextView"
    }

    override fun getApplicableElements(): Collection<String>? {
        return listOf(IMAGE_VIEW, TEXT_VIEW)
    }
}
```

- getApplicableElements 은 layoutDetector가 어떤 요소(element)를 감지할지를 지정한다.
  - ImageView, TextView가 있을 경우 감지했다고 알려주게 된다.
- 이제 관심있는 요소가 무엇을 할때를 알아야한다.

```kotlin
class AppCompactDetector : LayoutDetector() {
    companion object {
        val ISSUE = Issue.create(
                id = "appCompact",
                briefDescription = "you have to use appCompact",
                explanation = "you have to use appCompact",
                moreInfo = "",
                category = Category.CORRECTNESS,
                priority = 5,
                severity = Severity.ERROR,
                implementation = Implementation(AppCompactDetector::class.java, Scope.RESOURCE_FILE_SCOPE)
        )

        const val IMAGE_VIEW = "ImageView"
        const val TEXT_VIEW = "TextView"
    }

    override fun getApplicableElements(): Collection<String>? {
        return listOf(IMAGE_VIEW, TEXT_VIEW)
    }

    override fun visitElement(context: XmlContext, element: Element) {
				
    }
}
```

- visitElement 를 정의해 린트가 관심있는 요소 imageView, textView에 방문할때(visitElement) 내부에 무엇을 할지 지정해준다.
- imageView, textView를 감지해서 방문했으면 곧바로 이에 대한 린트를 표시해줄 수 있도록 한다.

```kotlin
class AppCompactDetector : LayoutDetector() {
    companion object {
        val ISSUE = Issue.create(
                id = "appCompact",
                briefDescription = "you have to use appCompact",
                explanation = "you have to use appCompact",
                moreInfo = "",
                category = Category.CORRECTNESS,
                priority = 5,
                severity = Severity.ERROR,
                implementation = Implementation(AppCompactDetector::class.java, Scope.RESOURCE_FILE_SCOPE)
        )

        const val IMAGE_VIEW = "ImageView"
        const val TEXT_VIEW = "TextView"
    }

    override fun getApplicableElements(): Collection<String>? {
        return listOf(IMAGE_VIEW, TEXT_VIEW)
    }

    override fun visitElement(context: XmlContext, element: Element) {
        context.report(
                ISSUE,
                element,
                context.getNameLocation(element),
                "use appCompact widget",
        )
    }
}
```

- report를 통해 해당 이슈, 노드, 위치, 메시지를 넘겨서 실제 사용자가 린트(빨간, 노란 밑줄)를 확인할 수 있다.
- 추가적으로 곧 바로 fix해줄 수 있도록 다음과 같이 옵션을 줄 수 있다.

```kotlin
class AppCompactDetector : LayoutDetector() {
    companion object {
        val ISSUE = Issue.create(
                id = "appCompact",
                briefDescription = "you have to use appCompact",
                explanation = "you have to use appCompact",
                moreInfo = "",
                category = Category.CORRECTNESS,
                priority = 5,
                severity = Severity.ERROR,
                implementation = Implementation(AppCompactDetector::class.java, Scope.RESOURCE_FILE_SCOPE)
        )

        const val IMAGE_VIEW = "ImageView"
        const val APP_COMPACT_IMAGE_VIEW = "androidx.appcompat.widget.AppCompatImageView"
        const val TEXT_VIEW = "TextView"
        const val APP_COMPACT_TEXT_VIEW = "androidx.appcompat.widget.AppCompatTextView"
    }

    override fun getApplicableElements(): Collection<String>? {
        return listOf(IMAGE_VIEW, TEXT_VIEW)
    }

    override fun visitElement(context: XmlContext, element: Element) {
        val fix = fix()
                .replace()
                .text(element.tagName)
                .with(when (element.tagName) {
                    IMAGE_VIEW -> APP_COMPACT_IMAGE_VIEW
                    TEXT_VIEW -> APP_COMPACT_TEXT_VIEW
                    else -> ""
                })
                .build()

        context.report(
                ISSUE,
                element,
                context.getNameLocation(element),
                "use appCompact widget",
                fix
        )
    }
}
```

- fix()를 통해 LintFix.create() 객체를 받아 text()를 with()로 replace()하는 LintFix객체를 만들어 report의 마지막에 넣어주도록 한다.
  - LintFix는 기본적으로 null이다.
- 그러면 결과적으로 다음과 같이 된다.

<Img src="https://user-images.githubusercontent.com/58923717/132084028-a85300d4-42f9-440a-ba36-8862e8eb040c.png" />

- 하지만 아직 레지스터가 app모듈 린트로 지정해주지 않았기에 동작하지 않는다.

### App

- 이제 실제로 만들어진 모듈을 프로젝트(app)에 사용될 수 있도록 gradle을 수정한다.
- build.gradle dependencies에 다음을 추가

```groovy
dependencies {

    lintChecks project(':[YOUR_LINT_MODULE_NAME]')

}
```

- setting.gradle 에 다음을 추가 (안드로이드 스튜디오에서 자동적으로 추가해줌)

```groovy
include ':[YOUR_LINT_MODULE_NAME]'
```

- 그리고 build →  clean project → make project를 하면 린트가 나타나는 것을 확인할 수 있다.



## Debug

- 위 과정을 완벽히 수행하고 make project 후 린트가 나타나지 않을 때
- 우선 작성한 린트가 등록되었는지 1차적으로 확인할 필요가 있다.
- "command + ," → Editor → Inspections → Android → Lint에서 등록한 이슈의 briefDescription가 있는지 확인해야 한다.

<img src="https://user-images.githubusercontent.com/58923717/132084093-fd304390-c5d4-4614-9db9-41440460188a.png"/>

- 만약 없다면 AGP버전과 린트 버전이 일치하는데 확인한다.
- AGP버전을 업데이트 후 다시 테스트 해본다.
- 만약 AGP버전을 올려 다음과 버그가 발생한다면 이는 등록된 이슈가 있다.

```
A problem occurred evaluating project ':[YOUR_LINT_MODULE]'.
> Failed to apply plugin 'kotlin'.
   > Gradle#projectsEvaluated(Action) on build '[YOUR_PROEJCT]' cannot be executed in the current context.
```

- 이슈

  [Sign in - Google Accounts](https://issuetracker.google.com/issues/170656529)

- 해결책

  [Gradle build tools 4.1.0 failing sync in Android Studio when there is a lintCheck dependency - Stack Overflow](https://stackoverflow.com/questions/64582833/gradle-build-tools-4-1-0-failing-sync-in-android-studio-when-there-is-a-lintchec)

- 위 방법으로도 린트가 나타나지 않는다면 우선 터미널로 린트를 수행해서 결과가 나타나는지 확인할 수 있다.

- 그리고 린트 결과를 html로 받아 볼 수 있다.

- 터미널 프로젝트 위치에서 다음 명령어를 수행한다.

```
./gradlew lint[YOUR_BUILD_VARIANTS]
```

- 만약 빌드 중에 오류가 발생한다면 일반적으로 gradle version과 자바 버전이 호환안되서 어류가 발생한다.
- 터미널 프로젝트 루트에서 ./gradlew --version 을 입력

```
./gradlew --version

------------------------------------------------------------
Gradle 6.7.1
------------------------------------------------------------

Build time:   2020-11-16 17:09:24 UTC

Kotlin:       1.3.72
Groovy:       2.5.12
Ant:          Apache Ant(TM) version 1.10.8 compiled on May 10 2020
JVM:          16.0.2 (Amazon.com Inc. 16.0.2+7)
OS:           Mac OS X 10.15.7 x86_64
```

[Compatibility Matrix](https://docs.gradle.org/current/userguide/compatibility.html)

- 위 링크에서 확인하면 6.7.1 버전에서 JVM16 은 호환되지 않아 빌드에 실패한다.

- 호환성에 맞게 자바 버전을 변경하고 다시 린트를 터미널에서 빌드시킨다.
- 이후에 project_directory → app → build → report 에서 결과파일을 확인할 수 있다.
- html로 결과를 받았지만 프로젝트내에서 린트가 표시되지 않는다면 gradle 버전을 올려본다.



## 추가

- 간단한 로직같은 경우는 큰 문제가 되지 않을 수 있다.
- 하지만 리소스 할당하고 해제와 같은 중요한 부분에서는 적절하게 린트 처리되어야 프로젝트의 완성도를 높일 수 있다.
- 리소스를 해제와 관련된 부분에서는 CleanUpDetector가 린트 처리해주고 있다.
- recycle(), commit(), release(), cloase() 이러한 메서드 호출이 필요한 이슈를 처리해준다.
  - ex) Preference에서 edit후에 commit(), apply() 메서드를 호출해야한다.
- 중요한 이슈가 처리되는 만큼 CleanUpDetector를 참조할 필요가 있다.

- 또한 CleanUpDetector에서는 기존가 다르게 DataFlowAnalyzer 를 이용하여 처리하고 있다.

**DataFlowAnalyzer**

- 기존 AbstractUastVisitor에서는 데이터의 흐름을 분석하는데 한계를 극복하게 도움을 주는 클래스이다.
- 추적할 인스턴스를 받아서 해당 인스턴스와 관련된 것만을 호출받을 수 있다.
- 변수 선언, 코틀린 Scoping (apply, let, also etc...) selfReturn (빌더패턴) 등의 다양한 흐름을 관심있는 객체에 대한 결과를 호출해줄 수 있도록 도움을 준다.
- 관심있는 메서드에서 호출되거나 리턴되거나 인자로 들어가거나에 대한 케이스를 처리할 수 있게 된다.



## 테스트

- Lint를 만들면서 해당 린트가 적절하게 작성되었는지 애매한 부분들이 존재한다.
- 그래서 반드시 테스트코드를 작성해서 검사를 해야한다.
- 특히, tree구조로 린트를 작성하면 여러상황에 대응할 수 있을 수 있지만 그 만큼 예외처리를 적절히 해줘야한다.
- 그렇기 때문에 린트로 현재 프로젝트에 안나타났다고 잘 작성된 코드라고 보기 어렵다.
- 테스트 케이스를 작성하는 부분은 어렵지 않다.
- 해당 소스코드를 `"""` 넣어 작성해 소스를 만들어 실행시키면 된다.
- 그리고 디텍터에 로그값을 추가하여 테스트 수행을 통해서 로그값도 확인 할 수 있다.

```kotlin
class CustomLintTest {

    @Test
    fun test01() {
        val src: LintDetectorTest.TestFile = LintDetectorTest.kotlin(
                """
<?xml version="1.0" encoding="utf-8"?>
<FrameLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">

    <WebView
        android:id="@+id/webView"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

    <TextView
	    android:id="@+id/textView"
        android:layout_width="match_parent"
        android:layout_height="match_parent"/>

</FrameLayout>

            """.trimIndent()
        ).within("src")

        lint().files(src)
                .allowMissingSdk().issues(Detector.ISSUE)
                .run()
                .expectErrorCount(1)
    }
}
```

> 테스트 패키지가 존재하지 않는다면 린트모튤 오른쪽 클릭 -> New -> Directory 에서 언어에 맞는 패키지 추가



## 결론

- 작성일 기준으로도 아직 베타버전이긴하다.
- 그래서 딥한 로직을 체크하는 부분에서 무조건 신뢰하는 것에는 무리이다.
- 하지만 간단한 컨벤션, 로직을 점검하는데에는 큰 무리없이 동작시킬 수 있음.
- 안드로이드 오픈 소스 프로젝트에서 여러 디텍터를 참고하여 다양한 커스텀 린트를 작성할 수 있다.

