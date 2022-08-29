# Compose

공유객체의 속성을 쓰기, viewModel에서 식별 가능한 요소 업데이트같은 공유 환경설정에서 읽기와 같이 비용이 많이 드는 작업을 실행해야 하는 경우 백그라운드 코루틴에서 작업을 실행하고 값 결과를 Composable 함수에 매개변수로 전달합니다.
composable 함수에서는 공유환경 설정에 대한 읽거나 쓰면 않된다.

 UI 트리를 재구성하는 작업은 컴퓨팅 성능 및 배터리 수명을 사용한다는 측면에서 컴퓨팅 비용이 많이 들 수 있고 Compose는 이 *지능적 재구성*을 통해 이 문제를 해결한다. 다만 함수내에 공유환경 설정에 대한 읽거나 쓰기를 통해 예측할 수 없는 동작이 발생할 수 있다.



Composable function을 만들 때 고려해야 할 점은 아래 세 가지입니다.

빨라야 한다.
멱 등원(idempotent) 이어야 한다
side-effects과 연관되어서는 안 된다. (side-effects : App단의 상태를 변경하는 행위)



- 구성 가능한 함수는 순서와 관계없이 실행할 수 있습니다.
- 구성 가능한 함수는 동시에 실행할 수 있습니다.
- 재구성은 최대한 많은 수의 구성 가능한 함수 및 람다를 건너뜁니다.
- 재구성은 낙관적이며 취소될 수 있습니다.
- 구성 가능한 함수는 애니메이션의 모든 프레임에서와 같은 빈도로 매우 자주 실행될 수 있습니다.



앱의 상태는 시간이 지남에 따라 변할 수 있는 값입니다. 이는 매우 광범위한 정의로서 Room 데이터베이스부터 클래스 변수까지 모든 항목이 포함됩니다. (이러한 변경을 side-effects라고 할 수 있다)



StateHoisting을 하기 위한 규칙

**여러 Composable이 하나의 state를 공용으로 읽어 간다면 그 Composable들 중 가장 낮은 공통 상위 요소에 위치시킵니다.** 즉 예제에서 사용한 name을 A, B, C composable에서 사용한다면, A, B, C의 공통 부모 composable 중에 depth가 가장 낮은 (A, B, C와 가장 근접한) 공통 부모 composable에 state를 위치시켜야 합니다. 최소 공배수의 개념이라고 보면 될 것 같네요.

State should be hoisted to at least the lowest common parent of all composables that use the state (read).

**State는 변경될 수 있는 가장 높은 수준으로 끌어올려야 합니다. State에 쓰는 작업은 가장 상위 레벨에 위치해야 합니다.** 쉽게 말해 MVVM 패턴이라면 ViewModel에 state가 위치해야 합니다. 최대 공약수의 개념이라고 하면 될 것 같습니다. (더 헷갈리려나요?)

State should be hoisted to at least the highest level it may be changed (write).

**어떤 이벤트에 대한 응답으로 변경되는 state가 한 개가 아니라면, 같이 변경되는 state들은 같이 hoisting 되어야 합니다.**

If two states change in response to the same events they should be hoisted together.



Composable 함수가 재호출되고 recomposing의 여부를 결정하는 상태를 함수 내부가 아닌 외부로 노출시키는 작업을 state hoisting 이라고 합니다



스테이트풀한 composable은 어떤 면에서 테스트하기 어렵다는 것일까?



recomposition은 부분별하게 되지 않는다.

1. 이미 호출되어 있는 composable들과 비교하여 이전에 호출했던 것과 아닌 것을 구분합니다.
2. 호출되어야 하는 대상이지만 이전에 호출된적이 없다면 recomposable에 의해서 호출됩니다.
3. 반대로 이미 호출되었던 composable이라면 recomposition하지 않습니다. 하지만 이전에 호출된 상태라도 param이 변경된 composable이라면 recomposition 대상이 됩니다.



리스트를 반복해서 아이템을 그릴 경우에 호출순서를 식별자로서 사용하게 되고 마지막에 추가된 아이템이 있다면 전부가 아닌 마지막만 그리게 된다. 단, 정렬 순서가 변경되거나 첫 번째 아이템이 추가되면 호출순서가 변경되므로 전체가 다시 recomposition이 되게 된다. 이를 key를 이용하여 유니크한 값으로 recomposition을 제한할 수 있다.



Skipping if the inputs haven't changed
recomposition의 대상을 Skip 하기 위해서는 아래 조건을 모두 만족해야 합니다.

1. 이전에 이미 호출된 적이 있다
2. param이 stable type이다.
3. 이 stable한 type의 param이 변경되지 않았다. (equals 로 비교시 값이 동일하다)

일반적으로 primitive type, String, lamda function이 stable타입이다. 





LaunchEffect : 키 변화에 따른 동작을 수행하고 재실행 트리거는 key가 달라졌을 때 동작

rememberCoroutineScope : call site의 lifecycle에 따라 시작/취소되고 재실행 트리거는 없다.

rememberUpdatedState : 최신 동작을 저장, 래핑





# Reference

https://tourspace.tistory.com/

https://developer.android.com/jetpack/compose
