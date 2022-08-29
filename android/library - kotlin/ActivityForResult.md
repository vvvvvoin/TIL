# ActivityForResult

- androidx의 업데이트 이후로 activity/fragment에는 다양한 변화가 존재했다.
- 그중에는 Activity Result과 관련된 몇몇 API에도 변화가 생겼다.
- 그 중에는 기존에 사용되는 `startActivityForResult()`, `onActivityResult()`, `onRequestPermissionsResult()` 가 deprecated가 되었고 이와 관련된 내용이 androix의 activity에 새로운 API가 추가되었다.

## Gradle

- activity 1.2.0-alpha02버전 부터 해당 새롭게 추가된 API를 사용할 수 있다.
- 안정화 버전 1.2.0버전을 사용한다.

```groovy
dependencies {
    def activity_version = "1.2.0"
    // Java language implementation
    implementation "androidx.activity:activity:$activity_version"
    // Kotlin
    implementation "androidx.activity:activity-ktx:$activity_version"
}
```

## 콜벡등록

- Activity Result는 다른 activity로 부터 intent, uri를 받아 사용하는데 사용되었다.
- 이를 Activity Result API에서 제공하는 `registerForActivityForResult()` API를 이용하여 결과 콜벡을 등록할 수 있다.
- `registerForActivityForResult`는 Activity/Fragment에서 동일하게 사용할 수 있다.
-  `registerForActivityForResult()` 크게 입력과 출력으로 나누어 볼 수 있다.
- 입력
  - `ActivityResultContract` 
    - 결과를 생성하는 데 필요한 입력 유형과 출력 유형을 정의한다.
    - 사진촬영, 권한요청 등과 같은 종류의 기본 인텐트 작업을 `계약`으로 지정할 수 있다.
    - 또한 맞춤 계약을 만들 수 있다.
  - `ActivityResultCallback` 
    - ActivityResultContract에서 정의된 출력 유형의 객체를 가져오는 onActivityResult() 메서드가 포함된 단일 메서드 인터페이스이다.
- 출력
  - `ActivityResultLauncher` : 정의된 계약과 콜벡을 통해 반환된 ActivityResultLauncher를 이용해 activity를 실행한다.
- 다음과 같이 정의할 수 있다.
- registerForActivityResult() 메서드에 `ActivityResultContracts.GetContent()` 계약을 등록하면 이와 관련된 콜벡은 uri를 다루게 된다.

```kotlin
val getContent : ActivityResultLauncher = registerForActivityResult(GetContent()) { uri: Uri? ->
    // Handle the returned Uri
}
```

- 다른 계약이나 별개의 콜벡을 원한다면 여러 activity 결과 호출이 있다면 `registerForActivityResult()`를 여러 번 호출하여 여러개의 `ActivityResultLauncher` 인스턴스를 등록할 수 있다.

> Activity/Fragment가 생성되기 전에 registerForActivityResult()를 호출하는 것은 안전하다.
>
> 단, LifeCycler이 CREATED에 도달할 때까지 ActivityResultLanuncer를 실행할 수 없다.

## ActivityResultLanuncer 실행

- `registerForActivityResult`를 이용해 계약과 콜벡을 등록해도 자체적으로 시작하지 않는다.
- 반환된 `ActivityResultLanuncer` 인스턴스를 이용해야 한다.
- `ActivityResultLanuncer `의 `lanuch()`를 호출하여 결과를 생성하는 프로세스를 시작한다.
- 그리고 해당 프로세스가 완료되고 반환된 결과들은 콜벡에서 받아 처리하게 된다.

```kotlin
val getContent = registerForActivityResult(GetContent()) { uri: Uri? ->
    Glide.with(context).load(uri).into(imageView)
}

private lateinit var imageView : ImageView

override fun onCreate(savedInstanceState: Bundle?) {
    // ...

    val selectButton = findViewById<Button>(R.id.select_button)
    imageView = findViewById<Button>(R.id.image_view)

    selectButton.setOnClickListener {
        // Pass in the mime type you'd like to allow the user to select
        // as the input
        getContent.launch("image/*")
    }
}
```

- 버튼을 클릭하면 전역에 정의된 `registerForActivityResult()`의 계약과 콜벡을 통해 생성된 `ActivityResultLanuncer` 를 `image/*`타입의 Activity를 `launch()`를 이용해 실행한다.
- 새롭게 실행된 Activity로 부터 받은 데이터 uri가 콜벡에서 정의된 Glide를 통해 이미지를 표시하게 된다.

> 프로세스와 activity가 lanuch()를 호출할 때와 onActivityResult 콜벡이 트리거디는 사이에 소멸될 수 있으므로, 결과를 처리하는 데 필요한 추가 상태는 이러한 API와 별도로 저장하고 복원해야 한다.

## 맞춤 계약

- `registerForActivityResult()`의 입력파라미터에 `ActivityResultContracts`를 지정할 수 있다.
- `ActivityResultContracts`클래스에는 미리 빌드된 여러 개가 존재하고 개발자가 원하는 유형의 API를 제공하여 맞춤 계약을 제공한다.
- `ActivityResultContracts`에 입력이 필요하지 않은 경우 입력 유형으로 `Void`를 사용하여 클래스를 정의해야 한다.
- 각 계약은 `createIntent()` 메서드를 구현해야한다.
- 이 메서드는 `Context`와 입력을 가져와 `startActivityForResult()`와 함께 사용할 `Intent`를 구성합니다.

- resultCode와 Intent에서 출력을 생성하는 parseReulst()도 구현해야 한다.

```kotlin
class PickRingtone : ActivityResultContract<Int, Uri?>() {
    override fun createIntent(context: Context, ringtoneType: Int) =
        Intent(RingtoneManager.ACTION_RINGTONE_PICKER).apply {
            putExtra(RingtoneManager.EXTRA_RINGTONE_TYPE, ringtoneType)
        }

    override fun parseResult(resultCode: Int, result: Intent?) : Uri? {
        if (resultCode != Activity.RESULT_OK) {
            return null
        }
        return result?.getParcelableExtra(RingtoneManager.EXTRA_RINGTONE_PICKED_URI)
    }
}
```

- 맞춤 계약이 필요하지 않다면 `StartActivityForResult`계약을 사용하면 된다.
- deprecated된 `startActivityForReulst`와 같은 기능을 수행할 수 있다.

```kotlin
profileImageView.setOnClickListener {    
    val intent = Intent()                       
    intent.type = "image/*"                     
    intent.action = Intent.ACTION_OPEN_DOCUMENT 
    requestActivity.launch(intent)              
}                                               

private val requestActivity = registerForActivityResult(
    ActivityResultContracts.StartActivityForResult()
) { activityResult ->
    // action to do something
    if(activityResult.resultCode == Activity.RESULT_OK){
    receivedProfileUri = activityResult.data?.data
    receivedProfileUri?.let {
        activity?.contentResolver?.takePersistableUriPermission(it, TASK_FLAG)

        Glide.with(context).load(receivedProfileUri).into(imageView)
        }
    }
}
```



