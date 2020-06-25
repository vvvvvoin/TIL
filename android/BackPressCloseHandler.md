### BackPressCloseHandler

- 흔히 두번 뒤로가기 버튼을 눌러 앱을 종료시킬때 사용
```java
public class BackPressCloseHandler {
    private long backKeyPressedTime = 0;

    private Toast toast;
    private Activity activity;

    public BackPressCloseHandler(Activity context) {
        this.activity = context;
    }

    public void onBackPressed() {
        if (System.currentTimeMillis() > backKeyPressedTime + 2000) {
            backKeyPressedTime = System.currentTimeMillis();
            showGuide();
            return;
        }
        if (System.currentTimeMillis() <= backKeyPressedTime + 2000) {
            activity.finish();
            toast.cancel();
        }
    }

    private void showGuide() {
        toast = Toast.makeText(activity, "\'뒤로\'버튼을 한번 더 누르시면 종료됩니다.",
                Toast.LENGTH_SHORT);
        toast.show();
    }
}
```
- System.currentTimeMillis(); 
	- 1970년 1월 1일로 부터의 현재까지의 1/1000초로 long타입으로 반환시킨다

- onBackPressed() method가 실행되면 최근 backKeyPressedTime과 현재시간을 비교한다
	- backKeyPressedTime 보다 2초 이상이 아닌 경우
		- backKeyPressedTime 를 현재시간으로 변경
		- Toast 메세지를 출력한다
	- backKeyPressedTime 보다 2초 이하인 경우
		 	- 해당 activity를 종료한다
- activity onCreate
```java
	private BackPressCloseHandler backPressCloseHandler;	

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.home_layout);
		
		backPressCloseHandler = new BackPressCloseHandler(this);
	}
```
- activity의 onBackPressed()에서 onBackPressed()를 를행
```java
	@Override
	public void onBackPressed() {
		backPressCloseHandler.onBackPressed();
	}
```

> onBackPressed() 정의하면 super.onBackPressed();가 자동적으로 매핑되는데 지워야한다
>
> 안그러면 뒤면 백 버튼을 클릭된걸로 인식되고 onBackPressed()의 activity.finish();가 실행되는듯



참고 : [https://javacan.tistory.com/entry/close-androidapp-by-successive-back-press](https://javacan.tistory.com/entry/close-androidapp-by-successive-back-press)