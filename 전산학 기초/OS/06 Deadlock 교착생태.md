# Deadlock 교착생태

## 데드락의 개념

- blocked/asleep state
  - 프로세스가 특정 이벤트와 필요한 자원을 기다리는 상태
- 데드락 상태
  - 프로세스가 발생 가능성이 없는 이벤트를 기다리는 경우
  - 시스템 내에 데르락에 빠진 프로세스가 있는 경우
- 데드락 vs startvation
  - 데드락은 빠저나갈 수 없는 상태이고 스타베이션은 언젠가는 빠저나감
  - 데드락은 어슬림상태에서 못 빠저나감
  - starvation은 레디상태에서 상주함(자원을 할당받으면 나갈 수 있음)

## 자원의 분류

- 일반적으로 HW, SW 자원이 있음

### 선점 가능 여부에 따른 분류

- preemptible resource
  - 선점 당한 후 돌아와도 문제가 발생하지 않는 자원
  - processor, memory
- non preempptible resources
  - 선점 당하면 이후 진행에 문제가 발생하는 자원
  - disk drive

### 할당 단위에 따른 분류

- total allocation resources
  - 자원 전체를 프로세스에게 할당
  - 프로세서
- partitioned allocation resources
  - 하나의 자원을 여러 조각으로 나누어 여러 프로세스들에게 할ㄷ
  - memory

### 동시 사용가능 여부에 따른 분류

- Exclusive allocation resources
  - 한 순간에 한 프로세스만 사용 가능한 자원
  - 프로세서, 메모리
- shared allocation resource
  - 여러 프로세스가 동시에 사용 가능한 자원
  - 프로그램, shared data 등

### 재사용 가능 여부에 따른 분류

- SR (serially reusable resources)
  - 시스템 내에 항상 존재하는 자원
  - 사용이 끝나면 다른 프로세스가 사용가능
  - 프로세서, 메모리, 프로그램
- CR (consumable resources)
  - 한 프로세스가 사용 후에 사라지는 자원
  - signal, message 등

## 데드락과 자원의 종류

- 데드락을 발생시킬 수 있는 자원의 형태
  - non preemptible resource (할당받은 자원을 뺏지 못하는 경우)
  - exclusive allocation resource (혼자 자원을 사용하는 경우)
  - serially reusable resources
    - CR의 경우 너무 복잡함

## 데드락 발생의 예

- 두개의 프로세스가 서로의 요청하는 자원을 사용하는 경우

## 데드락의 모델

- graph model
- state trasition model

## 데르락 발생 필요조건

- 자원의 특성
  - Exclusive use of resources
  - non-preemptible resources
- 프로세스의 특성
  - hold and wait
    - 자원을 하나 hold하고 다른 자원 요청
  - circular wait

## 데드락 해결방법

### 교착상태 예방

- 필요조건 4가지 중 하나를 제거
  - 모든 자원을 공유
    - 현실적으로 불가능
  - 모든 자원에 대한 선점 허용
    - 현실적으로 불가능
  - 필요 자원 한번에 모두 할당
    - 자원 낭비 발생 - 필요하지 않은 순간에도 가지고 있음
    - 무한 대기 현상 발생 가능
  - circular wait 조건 제거
    - 자원들에게 순서를 부여
    - 프로세스는 순서의 증가 방향으로만 자원 요청 가능
    - 자원 낭비 발생

### 교착상태 회피

- 시스템의 상태를 계속감시하여 데드락 생태가 될 가능성이 있는 경우 요청 보류
- 시스템을 항상 safe state로 유지

- safe state
  - 모든 프로세스가 정상적 종료 가능한 상태
- unsafe state
  - 데드락 상태가 될 가능성이 있음

- 가정
  - 프로세스의 수가 고정
  - 자원의 종류와 수가 고정
  - 프로세스가 요구하는 자원 및 최대 수량을 알고 있음
  - 프로세스는 자원을 사용 후 반드시 반납한다.
- 데드락의 발새을 막을 수 있음
- 시스템을 항상 감시행하는 오버헤드
- 자원 활용성이 낮음

#### Dijkstra's  banker's alorithm,

- 한 종류의 자원이 여러개로 가정한다.

#### habermann's alorithm

### 교착생태 탐지 및 복구

- 데드락 방지를 위한 사전작업을 하지 않음
- 주기적으로 데드락 발생확인
- Resource allocation graph를 사용하여 데드락을 찾음

#### graph reduction

- 언블럭드 프로세스 - 필요한 자원을 모두 할당 받을 수 있는 프로세스

- 사용방법
  - 필요한 자원을 모두 할당 받을 수 있는 언블럭드 프로세스의 엣지를 제거
  - 더이상 언블럭드 프로세스가 없을 때까지 반복
- 엣지가 모두 제거되면 데드락 없음, 일부 엣지가 남으면 데드락 존재

- 오버헤드큼
- 데드락이 발생하면 복구하는 과정이 필요함

 ### 데드락 리커버리

- 데드락을 검출 한 후 해결하는 과정

#### 프로세스 터미네이션

- 데드락 프로세스 중 일부 종료
- 우선순위에 따라 프로세스를 선택하여 종료

#### resource preemption

- 데드락 상태 해결을 위해 선점할 자원 선택
- 해당 자원을 가지고 있는 프로세스를 종료시킴
  - 데드락 상태가 아닌 프로세스가 종료될 수 있음

#### checkpoint restart method

- 프로세스의 수행 중특점 지점마다 컨텍스트를 저장
- rollback을 위해 사용
  - 프로세스 강제 종료 후 가장 최근의 checkpoint에서 재시작

