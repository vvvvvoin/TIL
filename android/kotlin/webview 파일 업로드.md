# WebView 파일 업로드

- 웹뷰에서 파일업로드하는 방법에 대해 소개한다.
- 나아가 사진업로드 / 영상업로드를 할 경우 카메라앱과 파일탐색기를 같이 보여줘서 작업 할 수 있도록 로직을 구현한다.
- 안드로이드 5.0미만에서는 파일업로드 핸들링이 달라서 여러 예외처리를 해줘야 한는데 굳이 킷캣을 지원해야 할까라는 의문이 있었고 API 21기준으로 작성하였다.

## WebView 세팅

- 웹뷰 세팅을 수정에 `allowFileAccess` 값을 `true`로 설정해줘야 한다.

```kotlin
webview.apply {
  settings.apply {
    // add another your webview setting
    
    // add this code
    allowFileAccess = true
  }
}
```

- 그리고 `WebChromeClinet`를 정의해주고 `onShowFileChooser`  메서드를 오버라이딩 한다.

```kotlin
webview.apply {
	webChromeClient = object : WebChromeClient() {
		override fun onShowFileChooser(
		        webView: WebView?,
		        filePathCallback: ValueCallback<Array<Uri>>?,
		        fileChooserParams: FileChooserParams?
		): Boolean {
				// add your another onShowFileChooser method code
		    return true
		}
}
```

- 오러라이딩 메서드 매개변수의 간략하게 소개한다.
  - filePathCallback : 업로드하고자 하는 파일을 이 콜백의 `onReceiveValue` 메서드를 실행하여 비동기적으로 파일을 업로드시킨다.
  - fileChooserParams : 웹에서 선택한 `<input>`태그의 `accept` 값을 받아온다.
    - MIME 타입 혹은 파일 확장자값이 넘어온다.
- 오버라이딩 메서드에서 모든 로직을 작성할 수 있지만 보다 깔끔한 코드를 위해 해당 로직들을 새롭게 클래스를 만든다.
- 새롭게 정의하는 클래스에는 어떤 타입의 파일을 업로드할지 구분하고 `activity`에서 실행한 `intent`를 반환시키는 역할을 수행한다.

## Manifest 설정

- 카메라, 비디오 앱을 실행시켜 파일을 저장하기 위해서 casheDire를 이용할 것이다.
- 이를 위해서 몇가지 설정을 해줘야 한다.
- res -> xml(없다면 생성) 에 `provider_paths.xml`파일을 생성준다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<paths>
  <cache-path name="image" path="." />
</paths>
```

- 그리고 해당 파일을 manifest에 등록해준다.

```xml
<provider                                                 
    android:name="androidx.core.content.FileProvider"     
    android:authorities="${applicationId}.provider"       
    android:exported="false"                              
    android:grantUriPermissions="true">                   
                                                          
    <meta-data                                            
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/provider_paths" />         
</provider>
```

- 추가적으로 다음도 추가해준다.
  - Android 11 에서는 다른 앱과 상호작용하기위한 쿼리가 변경되었다.
  - queryIntentActivities, resolveActivty와 같은 다른 앱으로 부터 결과를 리턴하는 `packageManager` 메서드는 manifest에 queries태그를 기반으로 필터링 된다.

```xml
<queries>
    <intent>
        <action android:name="android.media.action.IMAGE_CAPTURE" />
    </intent>
</queries>
```

> 참고
>
> https://developer.android.com/about/versions/11/privacy/package-visibility?hl=kco
>
> https://newbedev.com/android-11-r-return-empty-list-when-querying-intent-for-action-image-capture

## WebView file uploade module

- `WebViewUploadModule`이라는 클래스를 정의하고 다음 전역변수를 추가하고 초기화할 수 있도록 한다.

```kotlin
private var filePathCallback: ValueCallback<Array<Uri>>? = null
private var imageFilePath: String? = null
private var videoFilePath: String? = null

fun getChooserIntent(
    context: Context,
    filePathCallback: ValueCallback<Array<Uri>>?,
    fileChooserParams: WebChromeClient.FileChooserParams?
): Intent {
	this.filePathCallback?.onReceiveValue(null)
  this.filePathCallback = filePathCallback
}
```

- 이제 module에서 `fileChooserParams`값을 통해 웹에서 요구하는 파일 타입을 구분하고 필터링하여 확장자값을 반환시키는 메서드를 정의한다.

```kotlin
    private fun getMimeTypesFromAcceptTypes(acceptTypes: Array<String>?): Array<String> {
        return (acceptTypes
            ?.mapNotNull { acceptType ->
                when {
                    // 확장자, MIME Type 경우를 구분시킴
                    acceptType.startsWith(".") -> MimeTypeMap.getSingleton().getMimeTypeFromExtension(acceptType.substring(1))
                    else -> acceptType
                }
            }
            // acceptType 을 지정하지 경우를 필터링
            ?.filter { it.isNotBlank() }
            ?.takeIf { it.isNotEmpty() }
        // acceptType 타입이 없을 경우 모든 MIME 타입으로 설정
            ?: listOf("*/*"))
            .toTypedArray()
    }

```

- 타입으로부터 이미지, 영상이 포함될 경우 관련 앱을 실행위한 intent를 초기화 시켜준다.


```kotlin
val uploadType = getMimeTypesFromAcceptTypes(fileChooserParams?.acceptTypes)
                                                                            
var imageIntent: Intent? = null                                             
var videoIntent: Intent? = null                                             
                                                                            
uploadType.forEach {                                                                   
    if ((it.contains("jpg") || it.contains("image/*")) && imageIntent == null) {      
        imageIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)                         
    } else if ((it.contains("mp4") || it.contains("video/*"))&& videoIntent == null) {
        videoIntent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)                         
    }                                                                                 
}                                                                                                                                                               
```

- 초기화된 인텐트로 부터 수행된 결과를 담을 파일을 지정해줄 수 있도록 한다.

```kotlin
var imageFile: File? = null                                                               
if (imageIntent?.resolveActivity(context.packageManager) != null) {                       
    try {                                                                                 
        imageFile = createTempFile(".jpg", context.cacheDir)
    } catch (ex: Exception) {                                                             
    }                                                                                     
                                                                                          
    if (imageFile != null) {                                                              
        imageFilePath = "file:" + imageFile.absolutePath                                  
        imageIntent?.putExtra(MediaStore.EXTRA_OUTPUT, getUriFromFile(context, imageFile))
    }                                                                                     
}                                                                                         
                                                                                          
var videoFile: File? = null                                                               
if (videoIntent?.resolveActivity(context.packageManager) != null) {                       
    try {                                                                                 
        videoFile = createTempFile(".mp4", context.cacheDir)
    } catch (ex: Exception) {                                                             
    }                                                                                     
                                                                                          
    if (videoFile != null) {                                                              
        videoFilePath = "file:" + videoFile.absolutePath                                  
        videoIntent?.putExtra(MediaStore.EXTRA_OUTPUT, getUriFromFile(context, videoFile))
    }                                                                                     
}                                                                                         
```

```kotlin
private fun getUriFromFile(context: Context, file: File): Uri {                      
    return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {                     
        FileProvider.getUriForFile(context, "${context.packageName}.provider", file) 
    } else {                                                                         
        Uri.fromFile(file)                                                           
    }                                                                                
}                                                                                    
```

- 이제 파일탐색기 intent를 정의하는데 이전에 받은 mime타입을 지정해 준다.

```kotlin
val contentSelectionIntent = Intent(Intent.ACTION_GET_CONTENT).apply {
    addCategory(Intent.CATEGORY_OPENABLE)                             
    type = "*/*"                                                      
    putExtra(Intent.EXTRA_MIME_TYPES, uploadType)                     
}                                                                     
```

> type에는 MIME타입이 들어가는데 extra로 EXTRA_MIME_TYPES를 넣어 지정해줄 경우 type을 \*/*로 지정해줘야 한다.

- 마지막으로 카메라 앱을 수행할 수 있도록 해준고 해당 intent를 리턴시켜준다.

```kotlin
return Intent(Intent.ACTION_CHOOSER).apply {                              
    putExtra(Intent.EXTRA_INTENT, contentSelectionIntent)                
                                                                         
    val intentList = mutableListOf<Intent>()                             
    arrayOf(imageIntent, videoIntent).forEach { intent ->                
        intent?.also { intentList.add(it) }                              
    }                                                                    
    if(intentList.size > 0){                                             
        putExtra(Intent.EXTRA_INITIAL_INTENTS, intentList.toTypedArray())
    }                                                                    
}                                                                        
```

- 그리고 전역에 webViewUploadModule 객체를 생성 후, webview `onShowFileChooser`에서는 다음과 같이 작성하면 된다.

```kotlin
override fun onShowFileChooser(                                                 
    webView: WebView?,                                                          
    filePathCallback: ValueCallback<Array<Uri>>?,                               
    fileChooserParams: FileChooserParams?                                       
): Boolean {                                                                    
                                                                                
    startActivityForResult(                                                     
        webViewUploadModule.getChooserIntent(                                   
            context,                                                            
            filePathCallback,                                                   
            fileChooserParams                                                   
        ),                                                                      
        9999
    )                                                                           
                                                                                
    return true
}                                                                               
```


- webViewFileUploadModule에 intent로 수행된 결과를 처리할 수 있도록 handleResult를 정의해준다.


```kotlin
fun handleResult(requestCode: Int, resultCode: Int, data: Intent?) {      
    if (requestCode == 9999 && resultCode == AppCompatActivity.RESULT_OK) {
        val results = getResultUri(data)?.let { arrayOf(it) }             
        if (results != null) {                                            
            filePathCallback?.onReceiveValue(results)                     
        }                                                                 
    } else {                                                              
        filePathCallback?.onReceiveValue(null)                            
    }                                                                     
    filePathCallback = null                                               
}                                                                         
```
```kotlin
private fun getResultUri(data: Intent?): Uri? {                    
    var result: Uri? = null                                        
                                                                   
    if (TextUtils.isEmpty(data?.dataString)) {                     
        arrayOf(imageFilePath, videoFilePath).forEach { path ->    
            if (path != null) {                                    
                Uri.parse(path).also { uri ->                      
                    if (File(uri.path.toString()).totalSpace > 0) {
                        result = uri                               
                        return@forEach                             
                    }                                              
                }                                                  
            }                                                      
        }                                                          
    } else {                                                       
        val filePath = data?.dataString                            
        result = Uri.parse(filePath)                               
    }                                                              
                                                                   
    return result                                                  
}                                                                  
```

- 결과를 반환할 수 있도록 activity에 onActivityResult를 정의해준다.

```kotlin
override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
    webViewUploadModule.handleResult(requestCode, resultCode, data)              
                                                                                 
    super.onActivityResult(requestCode, resultCode, data)                        
}                                                                                
```

