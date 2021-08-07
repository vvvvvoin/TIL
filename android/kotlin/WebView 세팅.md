# WebView 세팅

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



