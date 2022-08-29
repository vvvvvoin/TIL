# RecylcerView

- 리싸이클러뷰를 다루면서 몇 가지 궁금한점과 배운것이 있었고 이를 정리하였다.



## attachToRoot

- 리싸이클러뷰 아이템 객체를 생성하는 과정중에 inflate를 수행하면서 파라미터에 왜 attachToRoot에 false를 주는가?

```kotlin
fun newInstance(parent: ViewGroup): View {
    return ItemHolder(LayoutInflater.from(parent.context).inflate(R.layout.view_holder, parent, false))
}
```

- 결론부터 말하면 true, false를 주는 차이는 parent에 addView(childView) 를 나중에 수행할지에 대한 파라미터 값이다.
- true일 경우 곧바로 수행되고 false일 경우 수행되지 않는다.
- 일반적으로 잘못된 생각은 attachToRoot가 false일 경우 부모뷰에 자식뷰가 추가되지 않는다는 것이다.
- 즉, false, true 모두의 경우 자식뷰가 부모에 추가된다.
- 이는 그저 attach time에 대한 시간차이이다.
- 그리고 부모뷰에 자식뷰가 추가되지 않는 경우에는 attachToRoot를 true로 하면안된다. 
- true로 할 경우 자식 뷰의 2번째 파라미터인 viewGroup에 자동 추가된다.
  - 만약 루트 파라미터가 LinearLayout일 경우 인플레이트한 뷰(자식뷰)는 자동적으로 해당 뷰의 자식으로 들어간다.
- 그러나 false일 경우 인플레이시 어떤 뷰에다가도 attach되지 않는다.
- 또한 터치이벤트도 부모뷰가 수신받지 않는다.





### Visibility gone

- 리싸이클러뷰에서 각 홀더를 컨트롤할 일이 있다.
- 중간에 뷰를 잠시 가리기 위해 해당 Holder의 visibility를 gone시킬 것이다.
- 하지만 해당 홀더는 사라지지만 해당 위치에 여백이 남게 된다.

<div>
    <img src="https://i.stack.imgur.com/NxAN6.png"/>
</div>

- 일단 각 holder를 인플레이트 할 때 attachToRoot가 false이기 때문에 measured height가 계산이 되지 않는다.
- 그래서 root를 gone시키면 parent에서 뷰가 안잡히게 되고 기존에 가지고 있는 width, height를 반영시켜준다.
- 이를 해결하기 위해서는 root가 아닌 아이템을 포괄하는 레이아웃을 만들고 이 레이아웃 visility를 gone시켜주면 된다.
- 혹은 해당 홀더의 height를 0으로 만들어 주면 된다.