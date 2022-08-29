# ExoPlayer

### 이슈1

- ViewPager, ViewPager2 에서 expoplayer를 사용할 때 주의해야할 점이 있다.
- 각 holder(item)에서 exoplayer가 레이아웃 영역을 벗어나서 다른 아이템에 겹쳐서 보이는 문제가 있다.

> https://github.com/google/ExoPlayer/issues/5714

- 기본적으로 playerView의 `AspectRatioFrameLayout.RESIZE_MODE_FIT` 값을 갖고 있기 때문에 레이아웃에 맞게 나오지만 설정에 따라 `RESIZE_MODE_ZOOM`을 사용할 때 해당 문제가 발생한다.
- 이때에는 playerView에 다음 속성`app:surface_type="texture_view"`을 추가해준다.

```xml
    <com.google.android.exoplayer2.ui.PlayerView
        android:id="@+id/player"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:surface_type="texture_view"/>
```

