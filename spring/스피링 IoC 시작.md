#### 스피링 IoC 시작
##### 스피링 설정 파일 생성
- src/main/resource 소스 폴더에 Spring Bean Configuration File 선택
- FileName : applicationContext.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
	http://www.springframework.org/schema/beans/spring-beans.xsd">

</beans>
```
- <bean> 엘리먼트를 사용하여 클래스 하나당 하나의 <bean> 설정을 한다

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
	http://www.springframework.org/schema/beans/spring-beans.xsd">
	<!-- test class -->
	<bean id="test" class="com.test.cases"></bean>
</beans>
```
> ctrl + spaceBar를 이용하면 좀더 편리하게 사용가능
> 
##### 스피링 설정 파일 구동시키기
- java main class에서 Spring Bean Configuration파일을 불러와야한다.

```java
public class BoardServiceClient {	
	public static void main(String[] args) {
		AbstractApplicationContext container =
			new GenericXmlApplicationContext("applicationContext.xml");

	}
}
```

###### 스피링 컨테이너의 종류
- 스프링에서는 BeanFactory와 이를 상속한 ApplicationContext 두가지 유형의 컨테이너를 제공
- BeanFactory는 스프링 설정 파일에 등록된 <bean> 객체를 생성하고 관리하는 가장 기본적인 기능만 제공
-- 클라이언트 요청에 의해서만 <bean>객체가 생성되는 지연로딩 방식을 사용
-- Beanfactory를 사용할 일이 없다
- ApplicationContext 는 BeanFactory가 제공하는 기능이외에도 트랜잭션 기능을 지원
-- 즉시 로딩방식으로 동작함
-- 개발자 대부분이 ApplicationContext 유형의 컨테이너를 사용한다.
- ApplicationContext의 구현 클래스는 매우 다양하지만, 가장 많이 사용되는 클래스는 다음이다
-- GenericXmlApllicationContext : 파일 시스템이나 클래스 경로의 XML설정 파일을 로딩하여 작동하는 컨테이너
-- XmlWebApplicationContext : 웹 기반의 스프링 애플리케이션을 개발할 때 사용하는 컨테이너






























