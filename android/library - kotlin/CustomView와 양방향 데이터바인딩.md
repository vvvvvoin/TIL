# Custom View

- 잘 만들어진 뷰는 사용하지 쉬운 인터페이스로 특정 기능 집합을 갭슐화하고 CPU, 메모리, 시스템 자원 등을 효율적으로 사용하는 특징이 있다.
- 그러나 잘 만들어진 뷰, 클래스가 되기 위해서는 다음 사항을 만족해야 한다.
  - Android 표준 준수
  - Android XML 레이아웃에서 작동하는 맞춤 스타일 속성 제공
  - 접근성 이벤트 전송
  - 여러 Android 플랫폼과 호환
- 안드로이드에서는 이러한 요구사항을 충족하는 뷰를 만드는데 도움이 되는 기본 클래스와 XML태그를 제공한다.

## 커스텀 뷰의 서브클래스 만들기

- 안드로이드에서 정의된 모든 뷰 클래스는 `View`를 구현한다.

```kotlin
class MyCustomView : View {
    constructor(context: Context) : super(context)
    constructor(context: Context, attrs: AttributeSet) : super(context, attrs)
    constructor(context: Context, attrs: AttributeSet, defStyleAttr: Int) : super(context, attrs, defStyleAttr)
    ....
}
```

- 뷰 클래스는 개발자가 직접 객체를 만들어 사용하는 것이 아닌 안드로이드 intent가 객체를 만들고 관리하기 때문에 생성자를 규격에 맞게 만들어줘야 한다.
- 이러한 번거로움을 줄여주기 위해서 코틀린은 `@JvmOverloads`라는 어노테이션을 통해 간결하게 오버로딩을 지원한다.

```kotlin
class MyCustomView @JvmOverloads constructor(
    context: Context, attrs: AttributeSet, defStyleAttr: Int
) : View(context: Context, attrs: AttributeSet, defStyleAttr: Int) {
    ....
}
```

- 그 후에는 각 위젯을 정의하고 프러퍼티를 지정하여 Activity/Fragment에서 다룰 수 있도록 만든다.
- 또한 DataBinding을 이용해 다음과 같이 binding 인스턴스를 정의해준다.

```kotlin
class MyCustomView @JvmOverloads constructor(
    context: Context, attrs: AttributeSet, defStyleAttr: Int
) : View(context: Context, attrs: AttributeSet, defStyleAttr: Int) {
    val myCustomViewBinding: MyCustomViewBinding = MyCustomViewBinding.inflate(LayoutInflater.from(context), this, true)
    
    init {
        //todo
    }
}
```
## MyCustomView.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">

    <androidx.constraintlayout.widget.ConstraintLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content">

        <androidx.appcompat.widget.AppCompatImageView
            android:id="@+id/imageView1"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:src="@drawable/ic_hambuger_button"
            app:layout_constraintBottom_toBottomOf="parent"
            app:layout_constraintHorizontal_chainStyle="packed"
            app:layout_constraintHorizontal_weight="1"
            app:layout_constraintLeft_toLeftOf="parent"
            app:layout_constraintRight_toLeftOf="@+id/editText"
            app:layout_constraintTop_toTopOf="parent" />

        <androidx.appcompat.widget.AppCompatEditText
            android:id="@+id/editText"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:gravity="left|center"
            android:hint="검색어를 입력하세요"
            android:textColor="#000000"
            android:textColorHint="#59000000"
            android:singleLine="true"
            app:layout_constraintBottom_toBottomOf="@+id/imageView1"
            app:layout_constraintHorizontal_weight="5"
            app:layout_constraintLeft_toRightOf="@+id/imageView1"
            app:layout_constraintRight_toLeftOf="@+id/imageView2"
            app:layout_constraintTop_toTopOf="@+id/imageView1"/>

        <androidx.appcompat.widget.AppCompatImageView
            android:id="@+id/imageView2"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:src="@drawable/ic_search"
            app:layout_constraintBottom_toBottomOf="@+id/editText"
            app:layout_constraintHorizontal_weight="1"
            app:layout_constraintLeft_toRightOf="@+id/editText"
            app:layout_constraintRight_toRightOf="parent"
            app:layout_constraintTop_toTopOf="@+id/editText" />

    </androidx.constraintlayout.widget.ConstraintLayout>
</layout>
```

<div>
    <img src="https://user-images.githubusercontent.com/58923717/108588311-cb211480-739b-11eb-8e4d-4a63c3c9781f.JPG" height=500>
</div>

- 위에 XML을 통해 검색바 위젯을 만들 수 있다.

## 커스텀 뷰로 양방향 데이터 바인딩 수행하기

- 일반적인 `EditText`를 검색바에 사용하면 `singleLine`속성을 사용하게 된다.
- 검색하고자 하는 내용이 길어지면 처음 작성한 글이 옆으로 밀려 사라지게 되는데 이를 양방향 데이터바인딩으로 보완할 수 있다.

### ViewModel

- 우선 입력을 다룰 수 있는 변수를 ViewModel에 선언해준다.

```kotlin
class MyViewModel() : BaseViewModel() {

    val searchQuery = MutableLiveData<String>()

    init { 
        searchQuery.value = "" 
    }

}
```

### XML

- 그리고 원하는 XML에 검색바 위젯을 다음과 같이 추가한다.

```xml
<data>                                                                  
                                                                        
    <variable                                                           
        name="viewModel"                                                
        type="com.example.mvvm_template.viewModel.MyViewModel" />       
                                                                        
</data>                                                                 

<com.example.mvvm_template.view.ui.customview.MyCustomView
    android:id="@+id/searchBar"                        
    android:layout_width="match_parent"                
    android:layout_height="wrap_content"               
    android:layout_marginHorizontal="10dp"             
    android:clickable="true"                           
    android:focusable="true"                           
    app:layout_constraintBottom_toTopOf="@id/button"   
    app:layout_constraintHorizontal_bias="0.526"       
    app:layout_constraintHorizontal_chainStyle="packed"
    app:layout_constraintLeft_toLeftOf="parent"        
    app:layout_constraintRight_toRightOf="parent"      
    app:layout_constraintTop_toTopOf="parent"          
    app:flexibleText="@={viewModel.searchQuery}"/>     
```

- attribute값은 사용자가 원하는데로 사용하고 bindingAdapter에서 지정한 이름을 사용하면 된다.

### BindingAdapter

- 그리고 bindingAdapter에 다음과 같이 3가지 메서드를 만든다.

```kotlin
@BindingAdapter("flexibleText")
fun setEditTextText(
    view : MyCustomView,
    text : String
){
    val length = text.length
    when {
        (length in 0..12) -> {view.myCustomViewBinding.editText.setTextSize(Dimension.SP, 40F)}
        (length in 13..25) -> {view.myCustomViewBinding.editText.setTextSize(Dimension.SP, 20F)}
        else -> {view.myCustomViewBinding.editText.setTextSize(Dimension.SP, 10F)}
    }
}

@BindingAdapter("flexibleTextAttrChanged")
fun setEditTextBindingListener(view: MyCustomView, listener: InverseBindingListener) {
    view.myCustomViewBinding.editText.addTextChangedListener(object : TextWatcher {
        override fun afterTextChanged(s: Editable?) {
            listener.onChange()
        }
        override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {        }

        override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {        }
    })
}

@InverseBindingAdapter(attribute = "flexibleText", event = "flexibleTextAttrChanged")
fun getEditTextText(view: MyCustomView): String {
    return view.myCustomViewBinding.editText.text.toString()
}
```

#### setEditTextText

```kotlin
@BindingAdapter("flexibleText")
fun setEditTextText(
    view : SearchBar,
    text : String
){
    val length = text.length
    when {
        (length in 0..12) -> {
            view.myCustomViewBinding.editText.setTextSize(Dimension.SP, 40F)
        }
        (length in 13..25) -> {
            view.myCustomViewBinding.editText.setTextSize(Dimension.SP, 20F)
        }
        else -> {
            view.myCustomViewBinding.editText.setTextSize(Dimension.SP, 10F)
        }
    }
}
```

- text의 길이에 따라 view의 myCustomViewBinding에 접근해 커스텀 뷰가 가지는 EditText를 가져와 Text의 크기를 지정한다.

> 일반적인 단방향 데이터바인딩을 했을 경우와 동일하다

#### setEditTextBindingListener

```kotlin
@BindingAdapter("flexibleTextAttrChanged")
fun setEditTextBindingListener(view: MyCustomView, listener: InverseBindingListener) {
    view.myCustomViewBinding.editText.addTextChangedListener(object : TextWatcher {
        override fun afterTextChanged(s: Editable?) {
            listener.onChange()
        }
        override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {        }

        override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {        }
    })
}
```

- bindingAdapter 어노테이션에 들어가는 이름에 `AttrChanged`를 붙이는 것이 원칙이다.
- InverseBindingListener는 xml이 빌드될 때 다음과 같이 등록된다.

```java
 private androidx.databinding.InverseBindingListener searchBarflexibleTextAttrChanged = new androidx.databinding.InverseBindingListener() {
        @Override
        public void onChange() {
            // Inverse of viewModel.searchQuery.getValue()
            //         is viewModel.searchQuery.setValue((java.lang.String) callbackArg_0)
            //InverseBindingAdapter인 getEditTextText메서드를 통해 값을 전달
            java.lang.String callbackArg_0 = com.example.mvvm_template.view.ui.MainBindingAdapterKt.getEditTextText(searchBar);
            // localize variables for thread safety
            // viewModel.searchQuery
            androidx.lifecycle.MutableLiveData<java.lang.String> viewModelSearchQuery = null;
            // viewModel.searchQuery.getValue()
            java.lang.String viewModelSearchQueryGetValue = null;
            // viewModel
            com.example.mvvm_template.viewModel.MyViewModel viewModel = mViewModel;
            // viewModel != null
            boolean viewModelJavaLangObjectNull = false;
            // viewModel.searchQuery != null
            boolean viewModelSearchQueryJavaLangObjectNull = false;

            viewModelJavaLangObjectNull = (viewModel) != (null);
            if (viewModelJavaLangObjectNull) {
                viewModelSearchQuery = viewModel.getSearchQuery();
                viewModelSearchQueryJavaLangObjectNull = (viewModelSearchQuery) != (null);
                if (viewModelSearchQueryJavaLangObjectNull) {
                    viewModelSearchQuery.setValue(((java.lang.String) (callbackArg_0)));	//viewModel에 값 설정
                }
            }
        }
    };
```

- getEditTextText 메서드로 String값을 받아 ViewModel의 데이터를 세팅해준다.
- 이때 onChange메서드가 호출되는 것이다.

#### getEditTextText

```kotlin
@InverseBindingAdapter(attribute = "flexibleText", event = "flexibleTextAttrChanged")
fun getEditTextText(view: SearchBar): String {
    return view.searchBarBinding.editText.text.toString()
}
```

- setEditTextText가 값을 지정해주는 거라면 getEditTextText는 view로부터 data를 가져오는 getter역할을 수행한다.
- @InverseBindingAdapter 어노테이션 속성값 중 attribute에는 setEditTextText의 bindingAdapter를 event에는 InverseBindingListener를 호출하도록 한다.

### 결과

<div>
    <img src="https://user-images.githubusercontent.com/58923717/108588977-6e275d80-739f-11eb-9558-8e32f2b019ee.png" height=500 width=250 >
    <img src="https://user-images.githubusercontent.com/58923717/108588979-6ebff400-739f-11eb-9728-54d9c63f5769.png" height=500 width=250 >
    <img src="https://user-images.githubusercontent.com/58923717/108588980-6f588a80-739f-11eb-89b5-05191a33f598.png" height=500 width=250 >
</div>

- 입력을 받을 때마다 자동적으로 글자 크기가 변화하는 것을 확인할 수 있다.

> 참조 : [[Android\] 안드로이드 양방향 데이터 바인딩](https://salix97.tistory.com/276)

