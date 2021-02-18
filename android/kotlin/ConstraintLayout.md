# ConstraintLayout

## 배경

- 기존 linear를 사용하면 여러 태그를 사용하면서 계속 태그를 열는 과정에서 성능이 떨어지는 문제가 있었다.
- relative는 위젯간의 관계를 정의해서 여러 태그를 사용해서 성능문제는 없었지만 서로 위젯간에 겹치는 문제점이 있었다.
- 또한 기존 layout이 여러 디바이스에 마다 다른 화면크기에 대응할 layout가 마땅치 않았다.
- 이를 보완한 것이 `ConstraintLayout`이다.
- 다양한 디바이스 크기에 대응할 수 있고 조건을 걸어 레이아웃이 겹치는 문제를 해결하고 여러 태그를 사용하지 않아 성능문제에 대응한다.

## 사용방법

- Constraintlayout을 사용하는데 있어서 기준과 대상이 필요하다.
- 기준
  - 현재 위젯의 **어떤면**이 다른 위젯의 **어떤면**과 기준이 되는지
- 대상
  - 현재 위젯과 제약이 걸릴 다른 위젯이 필요하다.
  - 다른 위젯을 나타내기 위해서는 id가 필요하다.

- xml의 attribute가 다음과 같이 사용된다.
- `app:layout_constraintLeft_toLeftOf="parent"` 
- 현재 위젯의 **왼쪽면**이 다른 위젯(parent)의 **왼쪽**이 **parent**와 제약을 건다로 해석할 수 있다.
- 아래 xml을 통해 다음과 같은 결과를 얻는다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <androidx.appcompat.widget.AppCompatTextView
        android:id="@+id/textView1"
        android:layout_width="200dp"
        android:layout_height="100dp"
        android:text="text view 1"
        android:textSize="20dp"
        app:layout_constraintBottom_toTopOf="@+id/textView2"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <androidx.appcompat.widget.AppCompatTextView
        android:id="@+id/textView2"
        android:layout_width="200dp"
        android:layout_height="100dp"
        android:text="text view 2"
        android:textSize="20dp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/textView1" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

<div><img src="https://user-images.githubusercontent.com/58923717/108208686-b3b01480-716c-11eb-9f49-44360a444c06.JPG" height="500"></div>

- textView1이 위쪽, 왼쪽, 오른쪽을 부모와 제약을 걸고 아래쪽을 textView2위젯의 위쪽과 제약을 건다.
- textView2는 왼족, 오른쪽, 아래를 부모와 제약을 걸고 위쪽을 textView1위젯의 아래와 제약을 건다.

### chain

- 기본적으로 각 위젯, parent간에 간격은 `spread`라는 default chainStyle로 균등하게 나누어지게 된다.
- 이는 각 위젯간에 체인이 걸려있다고 말한다.
- 현재는 textView1, 2가 수직으로 체인이 걸려있고 이는 `app:layout_constraintVertical_chainStyle="spread"` 속성이 있는 것과 같다.

- 여기에 `packed`라는 속성을 부여하게 되면 다음과 같이 된다.

```xml
<androidx.appcompat.widget.AppCompatTextView            
    android:id="@+id/textView1"                         
    android:layout_width="200dp"                        
    android:layout_height="100dp"                       
    android:text="text view 1"                          
    android:textSize="20dp"                             
    app:layout_constraintBottom_toTopOf="@+id/textView2"
    app:layout_constraintLeft_toLeftOf="parent"         
    app:layout_constraintRight_toRightOf="parent"       
    app:layout_constraintTop_toTopOf="parent"           
    app:layout_constraintVertical_chainStyle="packed"/> 
                                                        
<androidx.appcompat.widget.AppCompatTextView            
    android:id="@+id/textView2"                         
    android:layout_width="200dp"                        
    android:layout_height="100dp"                       
    android:text="text view 2"                          
    android:textSize="20dp"                             
    app:layout_constraintBottom_toBottomOf="parent"     
    app:layout_constraintLeft_toLeftOf="parent"         
    app:layout_constraintRight_toRightOf="parent"       
    app:layout_constraintTop_toBottomOf="@+id/textView1"
    app:layout_constraintVertical_chainStyle="packed"/> 
```

<div><img src="https://user-images.githubusercontent.com/58923717/108208913-fb36a080-716c-11eb-8758-7cd0c2d44e97.JPG" height="500"></div>

- `packed`속성으로 두 위젯이 붙어있게 된다.
- 이러한 속성에 따른 기준은 수평방향일 경우 가장왼쪽에 있는 위젯이고 수직방향일 경우 가장 위쪽의 위젯이 기준이된다.

#### 다양한 ChainStyle

<div><img src="https://developer.android.com/training/constraint-layout/images/constraint-chain-styles_2x.png?hl=ko" ></div>

- 1번 방식이 spread chainStyle이다.
- 2번은 외부를 채운후 안쪽으로 채워나가는 형태이다.
- 3번은 packed방식인데 그외에도 너비의 크기를 0dp로 하여 `layout_constraintHorizontal_weight` 및 `layout_constraintVertical_weight`를 주어 다음과 같이 크기를 변경할 수도 있다.

```xml
<androidx.appcompat.widget.AppCompatTextView              
    android:id="@+id/textView1"                           
    android:layout_width="0dp"                            
    android:layout_height="100dp"                         
    android:background="#ffff00"                          
    android:text="text1"                                  
    android:textSize="30dp"                               
    app:layout_constraintHorizontal_weight="1"            
    app:layout_constraintHorizontal_chainStyle="spread"   
    app:layout_constraintBottom_toBottomOf="parent"       
    app:layout_constraintLeft_toLeftOf="parent"           
    app:layout_constraintRight_toLeftOf="@id/textView2"   
    app:layout_constraintTop_toTopOf="parent" />          
                                                          
<androidx.appcompat.widget.AppCompatTextView              
    android:id="@+id/textView2"                           
    android:layout_width="0dp"                            
    android:layout_height="100dp"                         
    android:background="#ff00ff"                          
    android:text="text2"                                  
    android:textSize="30dp"                               
    app:layout_constraintHorizontal_weight="3"            
    app:layout_constraintBottom_toBottomOf="@id/textView1"
    app:layout_constraintLeft_toRightOf="@id/textView1"   
    app:layout_constraintRight_toRightOf="parent"         
    app:layout_constraintTop_toTopOf="@id/textView1" />   
```

<div>
    <img src="https://user-images.githubusercontent.com/58923717/108312290-cfadc780-71f9-11eb-987d-b977c0d02cb6.JPG" height="500" >
</div>

- spread chainStyle을 사용했지만 위젯의 너비가 0dp이기 때문에 공백없이 채우게 되는데 weight를 사용하여 비율을 조정할 수 있다.
- linearlayout에서의 weight과 동일하다.

- 4번은 packed chainStyle일때 각 위젯마다 너비가 있을 경우 그림과 같이 배치된다.

### 제약된 위젯과 크기 맞추기

- textview1의 크기가 변화할때 제약을 통해 textview2도 textview1과 같이 크기를 맞출 수 있다.
- 수직방향으로 위젯이 위치했으므로 아래쪽 위젯을 위쪽 위젯의 left, right를 각각 다음과 같이 제약을 걸어준다.
- 그리고 width의 값은 textview1에 맞게 변화될 수 있도록 0dp로 설정한다.

```xml
<androidx.appcompat.widget.AppCompatTextView              
    android:id="@+id/textView1"                           
    android:layout_width="200dp"                          
    android:layout_height="100dp"                         
    android:text="text view 1"                            
    android:textSize="20dp"                               
    app:layout_constraintBottom_toTopOf="@+id/textView2"  
    app:layout_constraintLeft_toLeftOf="parent"           
    app:layout_constraintRight_toRightOf="parent"         
    app:layout_constraintTop_toTopOf="parent"/>           
                                                          
<androidx.appcompat.widget.AppCompatTextView              
    android:id="@+id/textView2"                           
    android:layout_width="0dp"                            
    android:layout_height="100dp"                         
    android:text="text view 2"                            
    android:textSize="20dp"                               
    app:layout_constraintBottom_toBottomOf="parent"       
    app:layout_constraintLeft_toLeftOf="@+id/textView1"   
    app:layout_constraintRight_toRightOf="@+id/textView1" 
    app:layout_constraintTop_toBottomOf="@+id/textView1"/>
```

<div><img src="https://user-images.githubusercontent.com/58923717/108209404-9a5b9800-716d-11eb-93ef-2b8169fa0ac8.JPG" height="500"></div>

- 이제는 textview2가 위와 같이 제약이 걸리게 되고 textview1의 width의 크기에 맞게 변화하게 된다.

### baseline

- baseline은 해당 위젯의 내용의 기본라인을 의미한다.
- baseline을 서로 맞추어 서로 크기가 다른 위젯의 내용을 맞춰줄 수 있도록 한다.
- 만약 소수점을 표현하는데 소수점밑 숫자를 작게 표현한다면 기존 linearlayout으로는 어려울 수 있다.
- 하지만 baseline을 통해 다음과 같이 만들 수 있다.

```xml
<androidx.appcompat.widget.AppCompatTextView                    
    android:id="@+id/textView1"                                 
    android:layout_width="100dp"                                
    android:layout_height="100dp"                               
    android:text="12345."                                       
    android:textSize="30dp"                                     
    app:layout_constraintBottom_toBottomOf="parent"             
    app:layout_constraintHorizontal_chainStyle="packed"         
    app:layout_constraintLeft_toLeftOf="parent"                 
    app:layout_constraintRight_toLeftOf="@+id/textView2"        
    app:layout_constraintTop_toTopOf="parent" />                
                                                                
<androidx.appcompat.widget.AppCompatTextView                    
    android:id="@+id/textView2"                                 
    android:layout_width="100dp"                                
    android:layout_height="100dp"                               
    android:text="6789"                                         
    android:textSize="20dp"                                     
    app:layout_constraintBottom_toBottomOf="@+id/textView1"     
    app:layout_constraintHorizontal_chainStyle="packed"         
    app:layout_constraintLeft_toRightOf="@id/textView1"         
    app:layout_constraintRight_toRightOf="parent"               
    app:layout_constraintTop_toTopOf="@+id/textView1"           
    app:layout_constraintBaseline_toBaselineOf="@id/textView1"/>
```

<div>
    <img src= "https://user-images.githubusercontent.com/58923717/108210895-6ed9ad00-716f-11eb-8bfd-4189218e3c87.JPG" height="500" width="200">
    <img src= "https://user-images.githubusercontent.com/58923717/108210887-6d0fe980-716f-11eb-8b4c-cbe2021021d1.JPG" height="500" width="200">
    <img src="https://user-images.githubusercontent.com/58923717/108210892-6da88000-716f-11eb-8ee8-153feaae39eb.JPG" height="500" width="200">
</div>

- 첫번째 사진은 `layout_constraintBaseline_toBaselineOf` 속성이 없을 경우 서로 크기가 다른 글자가 위치에 맞지 않음을 볼 수 있다.
- 두 번째, 세 번째 사진은 `layout_constraintBaseline_toBaselineOf`  속성을 통해 서로 크기가 다른 글자가 라인에 맞게 나타난 것을 확인할 수 있다.

### bias

- 위의 xml은 부모를 기준으로 되어있기 떄문에 가운데로 정렬이 되어있다.
- 이를 bias를 수평/수직을 주어 정렬의 기준을 바꿀 수 있는데 bias의 default값은 0.5이다
- 이 값이 0에 가까우면 왼쪽, 1에 가까우면 오른쪽으로 이동된다.

```xml
<androidx.appcompat.widget.AppCompatTextView               
    android:id="@+id/textView1"                            
    android:layout_width="100dp"                           
    android:layout_height="100dp"                          
    android:text="12345."                                  
    android:textSize="30dp"                                
    app:layout_constraintBottom_toBottomOf="parent"        
    app:layout_constraintHorizontal_chainStyle="packed"    
    app:layout_constraintLeft_toLeftOf="parent"            
    app:layout_constraintHorizontal_bias="0.3"             
    app:layout_constraintRight_toLeftOf="@+id/textView2"   
    app:layout_constraintTop_toTopOf="parent" />           
                                                           
<androidx.appcompat.widget.AppCompatTextView               
    android:id="@+id/textView2"                            
    android:layout_width="100dp"                           
    android:layout_height="100dp"                          
    android:text="6789"                                    
    android:textSize="20dp"                                
    app:layout_constraintBottom_toBottomOf="@+id/textView1"
    app:layout_constraintHorizontal_chainStyle="packed"    
    app:layout_constraintLeft_toRightOf="@id/textView1"    
    app:layout_constraintRight_toRightOf="parent"          
    app:layout_constraintTop_toTopOf="@+id/textView1" />   
```

<div>
    <img src= "https://user-images.githubusercontent.com/58923717/108212708-903b9880-7171-11eb-9861-7f8c316fe725.JPG" height="500">
</div>

- 0.5보다 작은 값으로 왼쪽으로 이동된것을 확인할 수 있다.

### 가시성에 따른 동작

- 사용자와 상호작용으로 어떠한 위젯이 갑자기 `gone`되면 어떻게 될까?

<div>
    <img src= "https://user-images.githubusercontent.com/58923717/108213803-c4fc1f80-7172-11eb-8ad9-cd22385f6cef.JPG" height="500">
    <img src= "https://user-images.githubusercontent.com/58923717/108213879-d47b6880-7172-11eb-8b96-e42e37cc4767.JPG" height="500">
</div>

- 오른쪽의 위젯이 위치를 고정하지 못하고 왼쪽으로 쏠리는 상황이 발생한다.
- 이때 `layout_goneMarginLeft`값을 주어 다른 위젯이 사라질때의 위치를 바로잡을 수 있도록 한다.

```xml
<androidx.appcompat.widget.AppCompatTextView               
    android:id="@+id/textView1"                            
    android:layout_width="100dp"                           
    android:layout_height="100dp"                          
    android:text="abc."                                    
    android:textSize="30dp"                                
    android:visibility="gone"                              
    app:layout_constraintBottom_toBottomOf="parent"        
    app:layout_constraintHorizontal_bias="0.3"             
    app:layout_constraintLeft_toLeftOf="parent"            
    app:layout_constraintRight_toLeftOf="@+id/textView2"   
    app:layout_constraintTop_toTopOf="parent" />           
                                                           
<androidx.appcompat.widget.AppCompatTextView               
    android:id="@+id/textView2"                            
    android:layout_width="100dp"                           
    android:layout_height="100dp"                          
    android:text="abc"                                     
    android:textSize="30dp"                                
    app:layout_constraintBottom_toBottomOf="@+id/textView1"
    app:layout_constraintLeft_toRightOf="@id/textView1"    
    app:layout_constraintRight_toRightOf="parent"          
    app:layout_constraintTop_toTopOf="@+id/textView1"      
    app:layout_goneMarginLeft="200dp" />                   
```

<div>
    <img src= "https://user-images.githubusercontent.com/58923717/108214367-6e431580-7173-11eb-8891-9ead5d89435b.JPG" height="500">
</div>

- 왼쪽 위젯이 사라져도 기존위치와 비슷하게 위치했음을 확인할 수 있다.

> app:layout_constraintHorizontal_chainStyle이 packed였다면 사라진 위젯의 width에 맞게 magie을 설정하면 기존위치와 정확히 일치시킬수 있다.

- 추가적으로 일반적으로 layout에 사용하는 magine을 사용할 수도 있는데 이는 packed를 사용했을때 각 위젯간의 여백을 지정할때 사용할 수 있다.
- 사용방식은 기존 linearlayout과 동일하다.

### Circular positioning

- B위젯이 A위젯을 기준으로 대각선 방향으로 위치해야할 경우도 존재한다.
- 이때는 A위젯을 기준으로 거리와 각도를 `app:layout_constraintCircle`로 조정해줄 수 있다.

```xml
<androidx.appcompat.widget.AppCompatTextView       
    android:id="@+id/textView1"                    
    android:layout_width="100dp"                   
    android:layout_height="100dp"                  
    android:text="text1"                           
    android:textSize="30dp"                        
    app:layout_constraintBottom_toBottomOf="parent"
    app:layout_constraintLeft_toLeftOf="parent"    
    app:layout_constraintRight_toRightOf="parent"  
    app:layout_constraintTop_toTopOf="parent" />   
                                                   
<androidx.appcompat.widget.AppCompatTextView       
    android:id="@+id/textView2"                    
    android:layout_width="100dp"                   
    android:layout_height="100dp"                  
    android:text="text2"                           
    android:textSize="30dp"                        
    app:layout_constraintCircle="@id/textView1"    
    app:layout_constraintCircleAngle="60"          
    app:layout_constraintCircleRadius="150dp"      
    app:layout_constraintBottom_toBottomOf="parent"
    app:layout_constraintLeft_toLeftOf="parent"    
    app:layout_constraintRight_toRightOf="parent"  
    app:layout_constraintTop_toTopOf="parent" />   
```

<div>
    <img src= "https://user-images.githubusercontent.com/58923717/108308639-6dea5f00-71f3-11eb-8563-e805f67816b6.JPG" height="500">
</div>

- text1을 기준으로 text2가 상단을 0도를 기준으로 시계방향으로 60도 만큼 이동되었고 150dp만큼 떨어저있음을 확인할 수 있다.
- text2의 제약이 모두 parent와 제약이 걸렸지만 이동된다.

### Guidelines

- parent나 다른 위젯으로 제약을 거는 것 외에도 안내선(Guidelines)을 추가해서 제약을 걸 수 있다.

```xml
<androidx.appcompat.widget.AppCompatTextView           
    android:id="@+id/textView1"                        
    android:layout_width="100dp"                       
    android:layout_height="100dp"                      
    android:text="text1"                               
    android:textSize="30dp"                            
    app:layout_constraintBottom_toBottomOf="parent"    
    app:layout_constraintLeft_toLeftOf="@id/guideline2"
    app:layout_constraintRight_toRightOf="parent"      
    app:layout_constraintTop_toTopOf="parent" />       
                                                       
<androidx.constraintlayout.widget.Guideline            
    android:id="@+id/guideline2"                       
    android:layout_width="wrap_content"                
    android:layout_height="wrap_content"               
    android:orientation="vertical"                     
    app:layout_constraintGuide_begin="80dp" />         
```

<div>
    <img src= "https://user-images.githubusercontent.com/58923717/108310572-ee5e8f00-71f6-11eb-9c85-34b2c0bcf12c.JPG" height="500">
</div>

- 안내선은 따로 드래그를 통해 이동시킬 수 있다.

> 참고 : [ConstraintLayout으로 반응형 UI 빌드  | Android 개발자  | Android Developers](https://developer.android.com/training/constraint-layout?hl=ko)