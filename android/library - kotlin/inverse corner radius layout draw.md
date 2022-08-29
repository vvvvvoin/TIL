# inverse round corner layout draw

- 안드로이드에서는 canvas, paint, draw, path 등과 같은 클래스를 이용해서 다양한 레이아웃 모양을 만들 수 있다.
- 기본적으로 제공하는 것들을 이용해서 다음과 같은 레이아웃을 만들 수도 있다. 

<img width="153"  src="https://user-images.githubusercontent.com/58923717/161370109-dcb716ca-1e3f-4cc5-b473-e2b7fefe9d82.png">

- 보통은 카드뷰를 이용하여 위와 같은 형태를 만들고 elevation을 추가하여 더 다채롭게 뷰를 만들 수 있다.
- 하지만 아래와 같은 경우는 어떻게 만들 수 있는 걸까?

<img width="140"  src="https://user-images.githubusercontent.com/58923717/161370107-5c6feb82-98eb-48ba-a53c-e1a4067b704c.png">

- 아주 간단하게 생각하면 다음처럼 뷰 계층을 만들면 가능하다.

  \<FrameLayout

  ​	android:backgroundColor="@color/teal_700">

  ​	\<CardView

  ​		app:cardBackgroundColor="@color/White">

- 그렇다면 이렇게 되면 어떻게 만들 수 있을까?
<div>
<img width="301" alt="스크린샷 2022-04-02 오후 3 35 14" src="https://user-images.githubusercontent.com/58923717/161370274-c1aa34cd-c636-4c0d-9bb7-f74712944c0d.png"/>
<img width="300" alt="스크린샷 2022-04-02 오후 3 41 34" src="https://user-images.githubusercontent.com/58923717/161370620-5462353d-55cf-48a4-aa8e-106c89867b7d.png"/>
</div>


- 시각적으로 잘 보여주기 위해 테두리를 나타냈지만 실제로는 존재하지 않는다.
- 위 예시에서 처럼 구현하고 카드뷰 안쪽에 흰색배경에 뷰를 두어 안보이게 만들어야 할까? 해당 레이아웃이 여러 곳에서 사용된다면 매번 특정한 뷰를 추가해야할 것이다.
- 그럼 커스텀뷰로 만들면 되지 않을까? 좋은 방법이다. 다만, 뷰 계층이 생기고 작게나마 성능에 영향을 끼친다는 점이 있고, 근본적인 해결책이 아니라고 생각된다.
- 처음부터 위와 같이 뷰를 그릴 수 있으면 좋을거 같고, 각 꼭지점 마다 옵션을 주어 on/off할 수 있다면 좋을거 같다.

## How

- 기본적으로 rect, oval, roundRect, circle등 기본적인 모양을 그릴 수 있도록 제공된다.

<img width="153" alt="스크린샷 2022-04-02 오후 3 28 48" src="https://user-images.githubusercontent.com/58923717/161370109-dcb716ca-1e3f-4cc5-b473-e2b7fefe9d82.png">

- 위 그림은 roundRect을 이용해서 그릴 수 있는데 다음과 같이 할 수 있다.

```kotlin
private var w = 0
private var h = 0

private val roundPath = Path()
private val paint = Paint().apply {
    style = Paint.Style.FILL
    isAntiAlias = true
    color = Color.WHITE
}

override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
    super.onSizeChanged(w, h, oldw, oldh)

    if (this.w != w || this.h != h) {
        this.w = w
        this.h = h

        invalidate()
    }
}

override fun dispatchDraw(canvas: Canvas) {
    val count = canvas.save()
    val rect = RectF(0f, 0f, w.toFloat(), h.toFloat())
    roundPath.reset()
    // 50f 는 따라 옵션을 주어 받을 수 있도록 만들어 준다.
    roundPath.addRoundRect(rect, FloatArray(8) { 50f }, Path.Direction.CW)
    roundPath.close()

    canvas.drawPath(roundPath, paint)
    super.dispatchDraw(canvas)
    canvas.restoreToCount(count)
}
```

- 그럼 가운데가 구명뚤린 뷰는 어떻게 만들 수 있을까?
- 기존 roundPath에서 rectPath에 구멍을 뚫으면 된다.

```kotlin
override fun dispatchDraw(canvas: Canvas) {
    val count = canvas.save()
    val rect = RectF(0f, 0f, w.toFloat(), h.toFloat())
    
    val rectPath = Path().apply { 
        addRect(rect, Path.Direction.CW)
    }
    
    roundPath.reset()
    roundPath.addRoundRect(rect, FloatArray(8) { 50f }, Path.Direction.CW)
    roundPath.op(rectPath, Path.Op.REVERSE_DIFFERENCE)
    roundPath.close()
	  rectPath.close()

    canvas.drawPath(roundPath, paint)
    super.dispatchDraw(canvas)
    canvas.restoreToCount(count)
}
```

- 그리고 roundRect에서 각 꼭지점 radius를 조정하면 특정 부분만 표시되는 뷰를 그릴 수 있게 된다.

