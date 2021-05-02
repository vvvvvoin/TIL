## NestedScrollView

- 일반적으로 ScrollView에는 하나의 자식 뷰만을 가질 수 있기 때문에 레이아웃으로 묶어사용하게 된다.
- 또한 수직방향 스크롤만 지원하기 때문에 사용에 단점이 존재한다.
- 이를 보완하고 기존기능을 사용할 수 있는 것이 NestedScrollView이다.

### 사용용도

- 게시글
  - 일반적으로 게시판 게시글에 NestedScrollView를 적용할 수 있다.
  - 일반적인 게시글형태에 밑단에 RecyclerView가 댓글을 보는 형태로 들어갈 수 있다.
  - 이용자가 적당한 길이의 게시글을 읽고 스크롤로 내리면서 밑단에는 RecyclerView로 구성된 댓글창을 볼 수 있다.

- 이중 스크롤
- CoordinatorLayout, CollapsingToolbarLayout과 다음 처럼 사용되는 경우를 볼 수 있다.

<div>
    <img src="https://user-images.githubusercontent.com/58923717/115136298-e20d7b80-a059-11eb-827d-8ff1980ef6a3.gif"/ width="200">
</div>

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <com.google.android.material.appbar.AppBarLayout
        android:layout_width="match_parent"
        android:layout_height="200dp">

        <com.google.android.material.appbar.CollapsingToolbarLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:minHeight="100dp"
            app:layout_scrollFlags="scroll|exitUntilCollapsed">

            <androidx.appcompat.widget.Toolbar
                android:layout_width="match_parent"
                android:layout_height="50dp"
                app:title="TestAppBar" />

        </com.google.android.material.appbar.CollapsingToolbarLayout>

    </com.google.android.material.appbar.AppBarLayout>

    <androidx.core.widget.NestedScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:descendantFocusability="blocksDescendants"
        android:fillViewport="true"
        app:layout_behavior="@string/appbar_scrolling_view_behavior">

        <androidx.recyclerview.widget.RecyclerView
            android:id="@+id/recyclerView"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            app:layoutManager="androidx.recyclerview.widget.LinearLayoutManager"
            app:layout_behavior="@string/appbar_scrolling_view_behavior" />

    </androidx.core.widget.NestedScrollView>
    
</androidx.coordinatorlayout.widget.CoordinatorLayout>
```

> 컨텐츠의 최상위 레이아웃에 app:layout_behavior="@string/appbar_scrolling_view_behavior" 하나만 줘도 작동한다.

### 주의사항

#### recyclerView와 관련된

- NestedScrollView와 RecyclerView를 같이 사용하면 RecyclerView를 스크롤하면 NestedScrollView가 스크롤되는 문제가 발생한다.
- RecyclerView에 포커스가 맞춰지기 때문에 발생하는 문제이다.
- 해결책은 다음 속성을 RecylcerVIew레이아웃에 추가해주면 된다.

```xml
android:descendantFocusability="blocksDescendants"
```

- descendantFocusability : 해당 ViewGroup에 포커스를 하위뷰에 설정하는 속성
- blocksDescendants : ViewGroup에 포커스를 받지 못하는 값

#### 스크롤뷰와 관련된

- 앱바를 제외한 컨텐츠들은 스크롤이 되는 레이아웃으로 묶을 수 있다.
- 여기서 내부에 recycler뷰가 아니더라도 앱바의 collapsing이 동작하기 위해서는 nestedScroll로 사용해야한다.
- scrollView를 사용하면 동작안함
- swipeRefreshScrollView는 가능함
- 커스텀 하기위해서 컨텐츠를 카드뷰 안에 넣고 카드뷰에 `app:layout_behavior="@string/appbar_scrolling_view_behavior"`를 사용할 수도 있다.