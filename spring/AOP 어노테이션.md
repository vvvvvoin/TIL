### 어노테이션 기반 AOP
#### 어노테이션 기반 AOP 설정
##### 어노테이션 사용을 위한 스프링 설정
- aop를 어노테이션으로 설정하려면 스프링 설정파일에 aop:aspectj-autoproxy 엘리먼트를 선언해야한다.
```XML
<aop:aspectj-autoproxy></aop:aspectj-autoproxy>
```
- aop 관련 어노테이션들은 어드바이스 클래스에 설정한다.
- 어드바이스 글래스에 선언된 어토네이션들을 스프링 컨터이너가 처리하게 하려면 반드시 어드바이스 객체가 생성되어 있어야 한다.
- 스프링 설정파일에 bean을 등록하거나 @Service 어노테이션을 사용하여 컴포넌트가 검색될 수 있도록 한다.

##### 포인트컷 설정
- xml 설정에서 포인트트컷을 선얼할때는 aop:pointcut 엘리먼트를 사용했다.
- 어노테이션 설정으로 포인트컷을 선얼할 때는 @Pointcut을 사용하며, 하나의 어드바이스 클래스 안에 여러개의 포인트컷을 선언할 수 있다.
- 여러 포인트컷을 식별하기 위한 식별자가 필요한데, 이때 '참조 메소드'를 사용한다.
- 참조 메소드는 메소드 몸체가 비어있는 로직없는 메소드 이다.
- 따라서 어떤 기능을 처리할 목적이 아닌 단순히 포인트컷 식별하는 이름으로만 사용된다.
```xml
<bean id="log" class="com.springbook.biz.common.LogAdvice"></bean>
<aop:config>
	<aop:pointcut expression="execution(* com.springbook.biz..*Impl.*(..))" id="allPointcut"/>
	<aop:pointcut expression="execution(* com.springbook.biz..*Impl.get*(..))" id="getPointcut"/>
	<aop:aspect ref="log">
		<aop:after pointcut-ref="getPointcut" method="printLog"/>
	</aop:aspect>
</aop:config> 
```

```java
@Service
public class LogAdvice {
	@Pointcut("execution(* com.springbook.biz..*Impl.*(..))")
	public void allPointcut() {	}
	
	@Pointcut("execution(* com.springbook.biz..*Impl.get*(..))")
	public void getPointcut() {}
	....
}
```
##### 어드바이스 설정
- 어드바이스 클래스에는 횡단 관심에 해당하는 어드바이스 메소드가 구현되어 있다.
- 이 어드바이스 메소드가 언제 동작할지 결정하는 어노테이션을 메소드 위에 설정하면 된다.
- 어드바이스 동작시점은 XML설정과 마찬가지로 다섯 가지가 제공된다
- 반드시 어드바이스 메소드가 결합될 포인트컷을 참조해야 한다.
- 포인터컷을 참조하는 방법은 어드바이스 어노테이션 뒤에괄호를 추가하고 포인트컷 참조 메소드를 지정하면 된다.
```java
@Service
public class LogAdvice {
	@Pointcut("execution(* com.springbook.biz..*Impl.*(..))")
	public void allPointcut() {	}
	
	@Before("allPointcut()")
	public void printLog() {
		System.out.println("[공통로그] 비지니스 로직 수행 전 동작");
	}
}
```
##### 애스팩트 설정
- AOP 설정에서 가장 중요한 애스팩트는 @Aspect를 이용하여 설정한다.
- @Aspect가 설정된 애스팩트 객체어는 반드시 포인트컷과 어드바이스를 결합하는 설저이 있어야 한다.
```java
@Service
@Aspect		//Aspect = Pointcut + Advice
public class LogAdvice {
	@Pointcut("execution(* com.springbook.biz..*Impl.*(..))")
	public void allPointcut() {}	//포인트컷
							//	+
	@Before("allPointcut()")		//어드바이스
	public void printLog() {
		System.out.println("[공통로그] 비지니스 로직 수행 전 동작");
	}
}

```
#### 어드바이스 동작 시점
- [이전코드][https://github.com/vvvvvoin/TIL/blob/master/spring/AOP%20JointPoint%EC%99%80%20%EB%B0%94%EC%9D%B8%EB%93%9C%20%EB%B3%80%EC%88%98.md)를 어노테이션으로 변형

##### Before 어드바이스

- 클래스 선언부에 @Service, @Aspect를 추가하여 클래스가 컴포넌트 스캔되어 애스팩트 객체로 인식하게 한다.
- allPointcut 참조 메소드를 추가하여 포인트컷을 선언한다
- 마지막으로 beforeLog 메소드 위에 @Before을 추가하여 allPointcut()으로 지정한 메소드가 호출할 때 Before형태로 동작하게 설정한다.

```java
package com.springbook.biz.common;

@Service
@Aspect
public class BeforeAdvice {
    @Pointcut("execution(* com.springbook.biz..*Impl.*(..))")
    public void allPointcut(){}
    
	@Before("allPointcut()")
	public void beforeLog(JoinPoint jp) {
		String method = jp.getSignature().getName();
		Object[] args = jp.getArgs();
		
		System.out.println("[사전처리] " + method + "메소드 ARGS 정보" + args[0].toString());
	}
}
```

##### After Returning 어드바이스
- After Returning 어드바이스는 비즈니스 메소드가 리턴한 결과 데이터를 다른 용도로 처리할 때 사용한다.
```java
package com.springbook.biz.common;

@Service
@Aspect
public class AfterReturningAdvice {
	@Pointcut("execution(* com.springbook.biz..*Impl.*(..))")
    public void getPointcut(){}
    
	@AfterReturning(pointcut = "getPointcut()", returning = "returnObj")
	public void afterLog(JoinPoint jp, Object returnObj) {
		String method = jp.getSignature().getName();
		if(returnObj instanceof UserVO) {
			UserVO user = (UserVO) returnObj;
			if(user.getRole().equals("Admin")) {
				System.out.println(user.getName() + " 로그인(Admin)");
			}
		}
		
		System.out.println("[사후처리] " + method + " 메소드 리턴값 : " + returnObj.toString());
	}
}
```
- xml설정에서는 returning속성을 사용하여 바인드 변수를 명확하게 지정할 수 있었다.
- 어노테이션 설정에서도 returning속성을 이용하여 바인드 변수를 지정할 수 있다.
```xml
<aop:aspect ref="afterReturning">
			<aop:after-returning method="afterLog" pointcut-ref="getPointcut" returning="returnObj"/>
</aop:aspect>
```
##### After Throwing 어드바이스
- After Throwing 어드바이스는 비즈니스 메소드 실행 도중에 예외가 발생했을 대 공통적인 예외 처리 로직을 제공할 목적으로 사용하는 어드바이스이다.
```java
package com.springbook.biz.common;

@Service
@Aspect
public class AfterThrowingAdvice {
	@Pointcut("execution(* com.springbook.biz..*Impl.*(..))")
    public void getPointcut(){}
    
	@AfterThrowing(pointcut = "allPointcut()", throwing = "exceptObj")
	public void exceptionLog(JoinPoint jp, Exception exceptObj) {
		String method = jp.getSignature().getName();
		System.out.println(method + "메소드 수행 중 발생된 예외 발생");
		
		if(exceptObj instanceof IllegalArgumentException) {
			System.out.println("부적합한 값이 입력되었습니다");
		}else if(exceptObj instanceof NumberFormatException) {
			System.out.println("숫자 형식이 아닙니다");
		}else if(exceptObj instanceof Exception) {
			System.out.println("오류가 발생했습니다.");
		}
	}
}
```
- xml설정에서와 마찬가지로 throwing속성을 이용하여 바인드 변수를 지정할 수 있다.
```xml
<aop:aspect ref="afterThrwing">
			<aop:after-throwing pointcut-ref="allPointcut" method="exceptionLog" throwing="exceptObj"/>
</aop:aspect>
```
##### After 어드바이스
- After 어드바이스는 예외 발생 여부에 상관없이 무조건 수행되는 어드바이스로서 @After어노테이션을 사용한다.
```java
package com.springbook.biz.common;

@Service
@Aspect
public class AfterAdvice {
	@Pointcut("execution(* com.springbook.biz..*Impl.*(..))")
    public void getPointcut(){}
    
	@After("allPointcut()")
	public void finallyLog() {
		System.out.println("[사후처리] 비지니스 로직 수행 무조건 동작");
	}
}
```
#####  Around 어드바이스
- Around 어드바이스는 하나의 어드바이스로 사전, 사후 처리를 모두 해결하고자 할 때 사용한다.
```java
package com.springbook.biz.common;

@Service
@Aspect
public class AroundAdvice {
	@Pointcut("execution(* com.springbook.biz..*Impl.*(..))")
    public void getPointcut(){}
    
	@Around("allPointcut()")
	public Object aroundLog(ProceedingJoinPoint pjp) throws Throwable {
		String method = pjp.getSignature().getName();
		StopWatch stopWatch = new StopWatch();
		stopWatch.start();
		
		Object obj = pjp.proceed();
		
		stopWatch.stop();
		
		System.out.println(method + "메소드 수행에 걸린 시간" + stopWatch.getTotalTimeMillis() + "ms초");
		return obj;
	}
}
```

> 어드바이스 메소드 중에서 유일하게 Around 메소드만 JoinPoint가 아닌 ProceedingJoinPoint 객체를 매개변수로 받는다

#### 외부 Pointcut 참조하기
- xml설정으로 포인트컷을 관리했을 때는 스프링 설정 파일에 포인트컷을 여러개 등록했다.
- 애스팩트를 설정할 때 pointcut-ref 속성으로 특정 포인트컷을 참조할 수 있었기 때문에 포인트컷을 재사용할 수 있었다.
- 하지만 어노테이션 설정으로 변경하고부터는 어드바이스 클래스마다 포인트컷 설정이 포함되면서, 비슷하거나 같은 포인트컷이 반복 선언되는 문제가 발생한다.
- 스프링은 이런 문제를 해결하고자 포인트컷을 외부에 독립된 클래스에 따로 설정하도록 한다.
- 시스템에서 사용할 모든 포인트컷을 Pointcut Common클래스에 등록한다.
```java
package com.springbook.biz.common;

@Aspect
public class PointcutCommon {
	@Pointcut("execution(* com.springbook.biz..*Impl.*(..))")
	public void allPointcut() {}
	
	@Pointcut("execution(* com.springbook.biz..*Impl.get*(..))")
	public void getPointcut() {}
}

```
- 이렇게 정의된 포인트컷을 참조하려면 클래스 이름과 참조 메소드 이름을 조합하여 지정해야한다.
```java
package com.springbook.biz.common;

@Service
@Aspect
public class BeforeAdvice {
	@Before("PointcutCommon.allPointcut()")
	public void beforeLog(JoinPoint jp) {
		String method = jp.getSignature().getName();
		Object[] args = jp.getArgs();
		
		System.out.println("[사전처리] " + method + "메소드 ARGS 정보" + args[0].toString());
	}
}
```
- 포인트컷에 대한 소스는 삭제되었고 @Before 어노테이션에서 PointcutCommon 클래스의 allPointcut() 메소드를 참조하고 있다.































































