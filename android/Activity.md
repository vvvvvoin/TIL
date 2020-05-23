## Activity

> app을 구성하는 화면

### Activity 생성

 - New - Activity - 원하는 Activity
 	원하는 Activity 생성시 Layout을 구성하는 XML과 함께 Activity가 생성됨
- 일부 Activity가 에러일 경우
	File - invalidate Cashed / restart를 이용하여 개발환경을 초기화한다

### Manifest
 - manifests폴더에는 AndroidManifest.xml이 존재
 - Android App의 전체적인 설정(퍼미션, 서비스 등)을 잡는 XML형식의 파일
 - 새로운 Activity, Service를 추가하면 자동적으로 추가됨

### Class
- Activity를 생성하면 자동적으로 AppCompactActivity를 상속받은 class가 생성된다
- Class 내에 다양한 컴포넌트들을 설정하고 실질적인 로직이 구현이 된다.


## XML

### Drawable
Android applicaiton에 실질적으로 사용되는 이미지 파일을 XML파일 형태로 저장한다

### Layout
> 안드로이드 화면에 보여지는 위젯의 위치, 크기, 스타일을 설정을 할 수 있는 폴더이다
- Activity생성시 자동적으로 XML파일이 이곳에 생성이 되어진다.
- 실제 안드로이드 화면을 보면서 화면 디자인을 할 수 있지만, XML파일 형식을 함께 보면서 하는 보다 정확하고, 권장되어지는 방법이다.
#### LinearLayout
- 기본적으로 다른 Layout으로 구성되어 있지만, 사용하기 편리한 LinearLayout을 사용한다
- LinearLayout은 기본적으로 `weidth, height, orientation`이 기본적으로 XML형태로 정의 되어져야 한다.
- 자동생성 `Ctrl + spacecBar`를 적절히 이용하여 XML형식을 맞출 수 있도록 한다.

### View & ViewGroup
view
View는 안드로이드 화면에 보여지는 여러 Component를 나타낸다
 - TextVIew, Button, ListVIew 등
ViewGroup
ViewGroup는 위에서 설명한 LinearLayout과 같는 Layout를 지칭한다.

### Values
- Android application은 유지보수에 편리성을 위해 Values폴더내에 XML형식으로 ID와 Value로 이루어진 형태로 존재한다.
- component, color, string에 대한 것을 미리 정의하여 Values폴더에 정의된 ID로 값을 지정하고 추후 업데이트에 Values폴더에 정의된 값들만을 변경하여 유지보수를 편리하게 할 수 있도록 한다.
















