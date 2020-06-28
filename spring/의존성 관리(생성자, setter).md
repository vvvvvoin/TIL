### 의존성 관리
#### 스피링의 의존성 관리 방법
- 스프링은 IoC를 다음 두가지 형태를 지원
	- Dependency Lookup
		- 컨테이너가 애플리케이션 운용에 필요한 객체를 생성하고 클라이언트는 컨테이너가 생성한 객체를 검색하여 사용하는 방법
		- 실제론 개발 과정에서 사용되지 않음
	- Dependency Injection
		- 객체 사이의 의존관계를 스피링 설정 파일에 등록된 정보를 바탕으로 컨테이너가 자동으로 처리
		- 의존성 설정을 바꿀때에는 프로그램 코드를 수정하지 않음
		- 스프링 설정파일 수정만으로 변경사항을 적용시킬 수 있음
		- 유지보수에 유리함
		- 이러한 Dependency Injection은 두가지로 나뉨
			- Setter Injection
			- Constructor Injection



#### Constructor Injection 생성자 인젝션

- 스피링 컨테이너는 XML 설정 파일에 등록된 클래스를 찾아서 객체 생성할 때 기본적으로 매개변수가 없는 기본 생성자를 호출
- 하지만 컨테이너가 기본 생성자 말고 매개변수를 가지는 다른 생성자를 호출할  수 있다.
- 이를 생성자 인젝션, Constructor Injection으로 처리한다.
- 생성자 인젝션을 사용하면 생성자의 매개변수로 의존관계에 있는 객체의 주소 정보를 전달할 수 있다.
```java
public class SamsumgTV implements TV{
	private SonySpeaker speaker;
	
	public SamsumgTV() {
		System.out.println("==== samsungTV(1) 객체 생성");
	}
	
	public SamsumgTV(SonySpeaker speaker) {
		System.out.println("==== samsungTV(2) 객체 생성");
		this.speaker =speaker;
	}

	public void initMethod() {
		System.out.println("객체 초기화 작업");
	}
	public void destroyMethod() {
		System.out.println("객체 삭제전에 처리할 로직");
	}

	public void powerOn() {
		System.out.println("samsungTV 전원컨다. 가격은 " + price + " 원");
	}

	public void powerOff() {
		System.out.println("samsungTV 전원끈다");
	}

	public void volumeUp() {
		speaker.volumeUp();
	}

	public void volumeDown() {
		speaker.volumeDown();		
	}
}
```
```java
public class SonySpeaker   {
	public SonySpeaker() {
		System.out.println("===== SonySpeaker 객체 생성");
	}

	public void volumeUp() {
		System.out.println("sonySpeaker 소리 올리다");
	}

	public void volumeDown() {
		System.out.println("sonySpeaker 소리 줄이다");
	}
}
```
```xml
<bean id="tv" class="polymorphism.SamsumgTV">
		<constructor-arg ref="sony"></constructor-arg>
</bean>
<bean id="sony" class="polymorphism.SonySpeaker"></bean>
```

- id='tv'이고 클래스가 'SamsumgTV'인 생성자는 'sony'라는 'id'를 갖는 <bean>을 참조한다.
- id='sony'이고 클래스가 SonySpeaker <bean>을 만든다
- 실제 SonySpeaker클래스는 Speaker 클래스를 implements하고 있다.
- 그래서 SamsumgTV 클래스의 변수 private Speaker speaker 는 SonySpeaker를 받을 수 있다.



##### 다중 변수 매핑 (생성자 파라미터가 2개 이상일때)

```java
public class SamsumgTV implements TV{
	private SonySpeaker speaker;
	private int price;
	
	public SamsumgTV() {
		System.out.println("==== samsungTV(1) 객체 생성");
	}
	
	public SamsumgTV(SonySpeaker speaker) {
		System.out.println("==== samsungTV(2) 객체 생성");
		this.speaker =speaker;
	}
	public SamsumgTV(SonySpeaker speaker, int price) {
		System.out.println("==== samsungTV(3) 객체 생성");
		this.speaker =speaker;
		this.price = price;
	}
```
```xml
<bean id="tv" class="polymorphism.SamsumgTV">
		<constructor-arg ref="sony"></constructor-arg>
		<constructor-arg value="3000000"></constructor-arg>
</bean>
<bean id="sony" class="polymorphism.SonySpeaker"></bean>
```
- <constructor-arg value="3000000">을 추가한다.
- 고정된 문자열이나 정수같은 기본형 데이터는 value 속성을 이용한다



- 추가적으로 index속성을 이용하여 몇 번째에 변수가 매핑되는지 지정할 수 있다.
- index는 0부터 시작한다.
```xml
<bean id="tv" class="polymorphism.SamsumgTV">
		<constructor-arg index="0" ref="sony"></constructor-arg>
		<constructor-arg index="1" value="3000000"></constructor-arg>
</bean>
<bean id="sony" class="polymorphism.SonySpeaker"></bean>
```

##### 의존관계 매핑
- 위의 예제에서는 SonySpeaker를 이용하였다.
- 하지만 유지보수 측면에서 본다면 다른 스피커또한 사용될 것이고 자바코드를 수정하게 될것이다
- 이런 문제를 해결하기 위해 부모객체인 Speaker 인터페이스를 추가한다.

```java
public interface Speaker {
	void volumeUp();
	void volumeDown();
}
```
- 스피커를 implements한 클래스는 override할 수 있도록 한다.
```java
public class SonySpeaker implements Speaker {
	public SonySpeaker() {
		System.out.println("===== SonySpeaker 객체 생성");
	}
	@Override
	public void volumeUp() {
		System.out.println("sonySpeaker 소리 올리다");
	}
	@Override
	public void volumeDown() {
		System.out.println("sonySpeaker 소리 줄이다");
	}
}
```
- SamsumgTV 클래스는 SonySpeaker에서 Speaker로 변경
```java
public class SamsumgTV implements TV{
	private Speaker speaker;
	
	public SamsumgTV() {
		System.out.println("==== samsungTV(1) 객체 생성");
	}
	
	public SamsumgTV(Speaker speaker) {
		System.out.println("==== samsungTV(2) 객체 생성");
		this.speaker =speaker;
	}
	....
}
```
- XML 파일에 다른 스피커 클래스(apple speaker)를 추가한다
```xml
<bean id="tv" class="polymorphism.SamsumgTV">
		<constructor-arg index="0" ref="apple"></constructor-arg>
		<constructor-arg index="1" value="3000000"></constructor-arg>
</bean>
<bean id="sony" class="polymorphism.SonySpeaker"></bean>
<bean id="apple" class="polymorphism.AppleSpeaker"></bean>
```

- 결과적으로 자바코드는 수정하지 않고도 xml파일을 수정함으로서 유지보수 측면에서 유리해젔다.
- 다시 SonySpeaker를 사용하기 위해서는 xml파일 생성자 'ref'의 값을 다시 'sony'로만 변경하면 된다.


#### Setter Injection 새터 인젝션
- Setter 메소드를 호출하여 의존성 주입을 처리하는 방법
- constructor, setter 두 가지 방법 모두 멤버변수를 원하는 값으로 설정하는 목적이다
- 결과는 동일하므로 어떤 방법을 써도 무방하다.
- 다만, 대부분 Setter 인젝션을 사용한다
> Setter 메소드가 제공되지 않은 클래스에서만 생성자 인젝션을 사용
> 
```java
public class SamsumgTV implements TV{
	private Speaker speaker;
	private int price;
	public SamsumgTV() {
		System.out.println("==== samsungTV(1) 객체 생성");
	}

	public void setSpeaker(Speaker speaker) {
		System.out.println("setSpeaker 호출");
		this.speaker = speaker;
	}

	public void setPrice(int price) {
		System.out.println("setPrice 호출");
		this.price = price;
	}
	...
}
```
```xml
<bean id="tv" class="polymorphism.SamsumgTV">
	<property name="speaker" ref="apple"></property>
	<property name="price" value="3000000"></property>
</bean>
<bean id="sony" class="polymorphism.SonySpeaker"></bean>
<bean id="apple" class="polymorphism.AppleSpeaker"></bean>
```

- Setter 인젝션을 이용하려면 <property> 엘리먼트를 사용한다
- <property> 엘리먼트의 name속성 값이 호출하고자 하는 메소드 이름이다.
- 즉, name 속성값이 speaker라고 설정되어 있으면 호출되는 메소드는 "setSpeaker"이다
- 변수이름 첫글자를 대분자로 바꾸고 set을 붙인 메소드를 호출한다.

##### p 네임스페이스
- Setter 인젝션을 설정할때 p 네임스페이스를 사용하면 좀더 효율적으로 의존성 주입이 가능
- 다음과 같이 p 네임스페이스를 체크한다

![p네임스페이스](image/p네임스페이스.jpg)

```xml
<bean id="tv" class="polymorphism.SamsumgTV" p:speaker-ref="sony" p:price="3000000"></bean>
<bean id="sony" class="polymorphism.SonySpeaker"></bean>
<bean id="apple" class="polymorphism.AppleSpeaker"></bean>
```

> p:를 치고 자동완성 키를 눌르면 실제 SamsumgTV클래스의 setter메소드가 나와 정확한 입력을 할 수 있게 해준다.













