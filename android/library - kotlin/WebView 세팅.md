# WebView

## WebView 세팅

- 안드로이드 웹튜에는 다양한 세팅 값들이 존재한다.

```kotlin
binding.webView.apply {

    with(settings) {
        javaScriptEnabled = false			// 자바스크립트 허용 유무
        setSupportMultipleWindows(false)	// 새창 띄우기 허용 유무
        loadWithOverviewMode = false		// 컨텐츠가 웹뷰보다 클 경우 스크린사이즈에 맞춤
        useWideViewPort = false				// html viewpoert 메타 태그 지원
        setSupportZoom(false)				// zoom 허용 유무
        builtInZoomControls = false			// 화면 확대 / 축소 허용 유무
        displayZoomControls = false			// 화면 확대 / 축소 컨트롤로 표시 유무
        domStorageEnabled = false			// 로컬 저장소 허용 유무
        cacheMode = WebSettings.LOAD_NO_CACHE
        // LOAD_DEFAULT 기본 캐시 모드 사용
        // LOAD_NORMAL (deprecateed)
        // LOAD_CACHE_ELSE_NETWORK 캐시가 만료될지라도 이용가능하면 캐쉬된 자원을 사용
        // LOAD_NO_CACHE 캐시 사용 안함
        // LOAD_CACHE_ONLY 네트워크를 사용하지 않고 캐시에서 로드함

    }                                                        
```

- html viewpoert (useWideViewPort) - 데스크탑에서 보여지는 화면의 크기를 모바일에 맞게 보여질 수 있도록 \<meta>태그를 이용하여 실제 렌더링 되는 영역을 구분할 수 있도록하고 있고 webview에서 이와 관련된 태그를 지원할지 설정할 수 있다.

## WebView Client

- webview clinet에는 웹뷰를 좀 더 적극활용할 수 있도록 해주는 몇몇 메소드가 존재한다.

```kotlin
binding.webView.webViewClient = object : WebViewClient() {
    // override method
}
```

- onPageStared

	```kotlin
	override fun onPageStarted(view: WebView, url: String, favicon: Bitmap?)
	```
	
	- 페이지가 로딩될때 수행되는 메서드이다.
	- 로딩될때의 `view.title`를 통해 앱바의 타일틀 쪽에 보여줄 수 있다.
	
- onPageFinished

  ```kotlin
  override fun onPageFinished(view: WebView, url: String)
  ```

  - 페이지 로딩이 완려된 후 호출된다.
  - onPageStared와 동일하게 `view.title`를 이용하여 페이지 이름을 핸들링 할 수 있다.

- shoudOverrideUrlLoading

  ```kotlin
  override fun shouldOverrideUrlLoading(webView: WebView, url: String): Boolean
  ```

  - webview에서 클릭한 링크를 열기전에 수행되는 메서드이다.
  - 만약 플레이스토어 링크였다면 웹뷰로 플레이스토어가 아닌 플레이 스토어 앱을 열 수 있도록 핸들링 해줄 수 있다.

  ```kotlin
  override fun shouldOverrideUrlLoading(webView: WebView, url: String): Boolean {
      if(URLUtil.isNetworkUrl(url) && url.startsWith(PLAYSTORE_URL) == true) {
          startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
      }else{
          loadUrl(url)
      }
  }
  // PLAYSTORE_URL = "https://play.google.com/store/apps/details?id="
  ```
  
  - else문에 loadUrl이 있는데 만약 해당 url이 조건식에 맞지 않을 경우 loadUrl을 안해줄 경우 웹뷰에 페이지가 표시되지 않는다.

