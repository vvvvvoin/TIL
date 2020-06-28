### <bean> 엘리먼트 속성
#### 1. init-method
- Servlet 컨테이너는 web.xml 파일에 등록된 Servletㅍ클래스의 객체를 생성할 때 디폴트 생성자만 인식
- 따라서 생성자로 Servlet 객체의 멤버변수를 초기화 할수 없음
- 그래서 서블릿은 init() 메소드를 overring하여 멤버변수를 초기화함
- 스프링 컨테이너 역시 스프링 설정 파일에 등록된 클래스를 객체 생성할때 디폴트 생성자를 호출
- 초기화 작업이 필요하면 <bean>엘리먼트에 init-method 속성 사용한다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
	http://www.springframework.org/schema/beans/spring-beans.xsd">
	<!-- test class -->
	<bean id="test" class="com.test.cases.Test" init-method="initMethod"></bean>
</beans>
```
```java
package com.test.cases;

public class Test {
	public void initMethod() {
		System.out.println("객체 초기화 작업을 처리합니다.");
	}
	....
}
```
#### 2.destoryt-method
init-method와 마찬가지로 destoryt-method을 이용하여 객체 삭제전 호출될 임의에 메소드를 만들 수 있다.
```java
package com.test.cases;

public class Test {
	public void initMethod() {
		System.out.println("객체 초기화 작업을 처리합니다.");
	}
	public void destroyMethod() {
		System.out.println("객체 삭제전 작업을 처리합니다.");
	}
	....
}
```
```xml
<bean id="test" class="com.test.cases.Test" init-method="initMethod" destroy-method="destroyMethod"/>
```
#### 3. lazy-init
- ApplicationContext 를 이용한 컨테이너는 즉시 로딩방식으로 동작한다
- 그런데 자주 사용하지 않는 어떤 <bean>은 메모리를 차지하고 시스템에 부담을 줌
- 이러한 <bean>을 사용되는 시점에 객체를 생성하도록 lazy-init 속성을 제공한다
```xml
<bean id="test" class="com.test.cases.Test" lazy-init="true"/>
```
#### 4. scope
- 수많은 객체가 생성되는 중 하나만 생성돼도 상관없는 객체들이 존재한다.
- 그렇기에 하나만 생성해도 되는 객체이면 주소를 복사하여 다음과 같이 재사용할 수 있다.
```java
package com.test.cases;

public class Test {
	public static void main(String[] args) {
		TestCase cast1 = new TestCase();
		TestCase cast2 = case1;
		TestCase cast3 = cast2;
	}
}
```
- 하지만 이런식으로 프로그래밍하기에는 매우 어렵다.
- 결국 하나의 객체만 생성되도록 해야하는데 이것을 디자인 패턴 중 하나인 Singleton으로 해결할 수 있다.
- 그리고 컨테이너가 이러한 기능을 제공한다.
- <bean> 엘리먼트에 scope속성을 사용한다
```xml
<bean id="test" class="com.test.cases.Test" scope="singleton"/>
```
```java
package com.test.cases;

public class Test {
	public static void main(String[] args) {
		TestCase cast1 = new TestCase();
		TestCase cast2 = new TestCase();
		TestCase cast3 =new TestCase();
	}
}
```
- 객체를 여러번 생성해도 하나의 객체만 생성되게 된다.
- 반면에 여러번에 객체를 생성해할 대에는 scope의 값을 'prototype'을 사용한다면 여러개의 객체가 생성된다.