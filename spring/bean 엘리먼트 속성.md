### <bean> 엘리먼트 속성

#### init-method
- Servlet 컨테이너는 web.xml 파일에 등록된 Servlet 클래스의 객체를 생성할 때 디폴트 생성자만 인식
- 따라서 생성자로 Servlet 객체의 멤버변수를 초기화할 수 없음
- 그래서 Servlet은 init() 메소드를 재정의 하여 초기화

```xml
<bean id="tv" class="polymorphism.SamsumgTV" init-method="initMethod" ></bean>
```
```java
public class SamsumgTV implements TV{
	public SamsumgTV() {
		System.out.println("==== samsungTV 객체 생성");
	}
	
	public void initMethod() {
		System.out.println("객체 초기화 작업");
	}
    
    ....
```

#### destory-method
- 마찬가지로 스프링 컨테이너가 객체를 삭제하기 직전에 호출될 메소드를 정의할 수 있다
```xml
<bean id="tv" class="polymorphism.SamsumgTV" init-method="initMethod" destroy-method="destroyMethod"></bean>
```
```java
public class SamsumgTV implements TV{
	public SamsumgTV() {
		System.out.println("==== samsungTV 객체 생성");
	}
	
	public void initMethod() {
		System.out.println("객체 초기화 작업");
	}
    public void destroyMethod() {
		System.out.println("객체 삭제전에 처리할 로직");
	}
    ....
```
![bean element](image/bean 엘리먼트.jpg)

#### lazy-init
- 컨테이너를 구동하면 컨테이너가 구동되는 시점에 스프링 설정 파일에 등록된 <bean>들이 즉시 로딩방식으로 동작
- 하지만 어떤 <bean>은 자주 사용되지 않으면서 메모리를 많이 차지하여 시스템에 부담을 줌
- lazt-init 속성을 이용하여 클라이언트가 요청하는 시점에 생성하도록한다.

#### scope
- 개발 중 객체를 여러개를 만들게 된다.
- 하지만 어떤 클래스는 하나의 객체만 생성해야되는 경우가 존재한다.
- 이럴대 singleton pattern을 이용한다
- bean 엘리먼트에는 scope를 이용하여 singleton을 사용한디.

```xml
<bean id="tv" class="polymorphism.SamsumgTV" init-method="initMethod" destroy-method="destroyMethod" scope="singleton"></bean>
```
```java
public static void main(String[] args) {
		AbstractApplicationContext factory = new GenericXmlApplicationContext("applicationContext.xml");
		
		TV tv1 = (TV)factory.getBean("tv");
		TV tv2 = (TV)factory.getBean("tv");
		TV tv3 = (TV)factory.getBean("tv");
		
		factory.close();
	}
```
![singleton](image/singleton.jpg)
> singleton 이여서 객체를 여러번 요청해도 한번만 생성됨을 확인할 수 있다.








