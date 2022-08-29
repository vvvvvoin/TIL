# TimePicker 색상 적용

- 안드로이드 기본 위젯으로 TimePicker가 존재한다.
- 시계(Clock)로 나타나거나 스크롤(Spinner)로 시간을 지정할 수 있는 기능을 수행한다.

<div>
    <img src="https://user-images.githubusercontent.com/58923717/127728690-5a4c4f42-3b9c-41f7-89ba-b9450ceb19fa.png" width=400>
</div>


- 색상을 변경하기 위해서는 스타일을 적용시켜야 한다.

```xml
<style name="DateTimePickerStyle">
    <!-- Text color -->
    <item name="android:textColorPrimary">Red</item>
    <item name="android:textColorSecondary">Green</item>

    <!-- Controll, Divider color -->
    <item name="colorControlNormal">blue</item>
    <item name="colorAccent">Purple</item>
</style>                                                          
```
## Clock
<div>
    <img src="https://user-images.githubusercontent.com/58923717/127728867-ce4a8fca-7da3-4dfd-b5fd-066fcca68c0c.png"
</div>

## Spinner
<div>
    <img src="https://user-images.githubusercontent.com/58923717/127728875-021aebe5-714e-4794-8970-aa682d5d9cfc.png">
</div>
