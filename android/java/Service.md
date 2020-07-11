## Service
> 화면이 없는 Activity

 - App이 실행되고 있더라도 무조건 화면에 무언가가 Activity에 보여지는 것은 아님
	 - 대표적으로 카톡, 음악 플레이어
 - 시각적으로 보이지 않기 때문에 백그라운드에서 로직처리하는 것을 이용

### Life Cycle
- Service와 비교되는 Activity와 LifeCycle은 다음과 같다

- Activity
> onCreate -> onStart -> onResum -> onPause -> onStop -> onDestory
- Service
> onCreate -> onStart -> onResum -> onPause -> onStop -> onDestory

### Service 생성
- Service는 Activity와 마찬가지로 `new - Service - Service`형태로 생성한다
- 생성시 자동적으로 Manifest에 생성됨
- 2가지 설정이 존재
	- Exported는 Service를 다른 App에 제공하겠다는 의미
	- Enabled는 Service를 사용가능한 형태로 생성할 것이라는 의미

#### 생성
- 생성하고자 하는 Service를 `Service.class`에 기입한다
```java
Intent i = new Intent(getApplicationContext(), Service.class);
```
- Intent에 전달하고자 하는 데이터를 추가한다
```java
i.putExtra("messsage", "hello wolrd");
```
- Service 시작
```java
startService(i);
```
### onCreate()
> 객체가 생성될 때 호출

### onStartCommand()
> 실제 Service동작을 수행하는 Method
> onCreate() 가 호출 후 바로 호출됨
- 서비스 객체가 존재하면 `onCreat`없이 `onStartCommand`가 호출됨

- 1초 간격으로 1부터 10까지 Log를 출력해보자
	- Activity에서 수행하는 것과 같은 Thread를 사용한다
	- Service class 내에 전역변수로 Thread를 선언한다
	- onCreate에 다음코드를 작성한다
```java
private Thread myThread = new Thread(new Runnable() {
    @Override
    public void run() {
        for(int i = 1; i <= 10; i++){
            try {
                Thread.sleep(1000); // 1초
                Log.i("ServiceExam", "현재 숫자는 : " + i);
            } catch (Exception e){
                Log.i("ServiceExam", e.toString());
            }
        }
    }
});
```


- Thread생성후 `onStartCommand`에 Thread를 시작한다.

- 위의 코드를 다시 실행하기 위해 Service를 호출하면 Thread가 `onStartCommand`를 호출하여 숫자카운팅을 하것 같지만 못한다.
	- 이는 Thread가 `run`후 정려되면 dead상태가 되기 때문이다.
	- dead된 thread는 다시 실행시킬 수 없다
	- 다시 실행시키기 위해서는 Thread를 다시 생성하여 실행하는 것이다
- 이를 해결하기 위해 Thread객체를 `onStartCommand`에 객체를 선언하고 실행시키면 된다.
	```java
	@Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        //1초 간격으로 1 부터 10 까지 숫자를 로그로 출력
        myThread = new Thread(new Runnable() {
            @Override
            public void run() {
                for(int i = 0; i< 100; i++){
                    try {
                        Thread.sleep(1000);
                        //sleep을 하려고 할때 만약 interrupt가 걸리면 exception발생
                        Log.i("service", "현재 숫자는 : " + i);
                    }catch (Exception e){
                        Log.i("service", e.toString());
                        break;
                    }
                }
            }
        });
        myThread.start();
	```
- 하지만 Thread를 생성하징낳고 로직코드를 `onStartCommand`에 넣으면 Activity UI는 멈추게 된다.
- 그렇다면 Activity에서 Thread를 생성하면 되는거 아닌가???
	
	- 의도치 않게 앱이 강제로 종료되었을때, Activity는 죽어서 다시 실행시킬 수 없지만 Service는 특정처리를 진행하면 죽어도 다시 살아나 실행될 수 있기 때문이다.


[Example](https://github.com/vvvvvoin/MC_Android/blob/master/app/src/main/java/com/example/androidlectureexample/Example15Sub_LifeCycleService.java)을 참고한다.



























