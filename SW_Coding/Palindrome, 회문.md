# Palindrome, 회문

- **회문**(回文) 또는 **팰린드롬**(palindrome)은 거꾸로 읽어도 제대로 읽는 것과 같은 [문장](https://ko.wikipedia.org/wiki/문장)이나 [낱말](https://ko.wikipedia.org/wiki/낱말), 숫자, 문자열(sequence of characters) 등이다. ([wiki](https://ko.wikipedia.org/wiki/%ED%9A%8C%EB%AC%B8))

### 1213 팰린드롬 만들기

- 주어진 입력문자를 이용하여 회문을 만들 수 있다면 사전순으로 앞선 것을 출력하는 문제이다.
- 불가능할 경우 `"I'm Sorry Hansoo"`문자열을 출력한다.

#### 풀이

- 우선 입력문자가 회문으로 만들 수 있는지를 먼저 확인한다.
- 회문을 만들 수 있는 조건은 2가지이다
  - 문자의 갯수가 모두 짝수개이다 ex) ABBA
  - 한 문자를 홀수 나머지는 짝수개 이어야 한다. ex) AAACAAA

- 입력에 제한이 대문자로만 주어지므로 26개의 배열방을 선언해주고 입력으로 들어오는 문자를 1번만 돌아 배열에 넣어 홀수개인지 짝수 개인지 구분한다.

```JAVA
String str = br.readLine();
int countOdd = 0;
for(char c : str.toCharArray()) {
	int x = getCharNumber(c);
	if(x != -1) {
		cnt[x]++;
		if(cnt[x] % 2 == 1) {
			countOdd++;
		}else {
			countOdd--;
		}
	}
}
if(countOdd > 1) {
	System.out.println("I'm Sorry Hansoo");
	return;
}
```

```JAVA
private static int getCharNumber(char c) {
	int A = Character.getNumericValue('A');
	int Z = Character.getNumericValue('Z');
	int value = Character.getNumericValue(c);
	if(A <= value && value <= Z) {
		return value - A;
	}
	return -1;
}
```

- `getCharNumber`함수로 인덱스 0 부터 25까지 값을 매핑할 수 있다.
- 그리고 `cnt[x]`의 값을 2로 나눈 나머지 값이 1일 경우 홀수 이므로 `countOdd`를 증가시켜준다
- 짝수일 경우 값일 하나 줄임으로서 홀수개가 1개 이상인지를 확인하여 예외를 처리해준다.

- 주어진 입력으로 회문을 만들 수 있는 조건이 갖추어지면 사전순으로 가장 앞선 회문을 만들어야한다.
- 이미 사전순으로 배열로 몇개의 문자가 있는지 정의되있고 배열을 이용하여 사전순으로 회문을 만든다.

```java
//answer은 입력 문자열의 크기와 같은 배열
//cnt는 A-Z까지 문자가 몇개 존재하는 담은 배열
private static void makeStr(char[] answer, int[] cnt) {
	int index = 0;
    //사전순으로 회문을 만들어야 하므로 cnt배열 앞에서 부터 값을 찾는다.
	for(int i = 0; i < cnt.length; i++) {
        //문자가 1개 이상인 경우 짝수개 이다
		if(cnt[i] > 1) {
            //정답배열 앞에 추가
			answer[index] = (char)(i + 'A');
            //정답배열 뒤에 추가
			answer[answer.length - index - 1] = (char)(i + 'A');
            //짝수개 이므로 -2
			cnt[i] -= 2;
            //다음 위치 변경
			index++;
            //cnt[i]값이 더 존재하는지 확인하기 위해 i--
			i--;
        //홀수이면 반드시 해당 문자가 가운데 존재해야 회문이 됨
		}else if(cnt[i] == 1){
			answer[answer.length / 2] = (char)(i + 'A');
		}
	}
}
```

### 10942 팰린드롬?

- 입력으로 주어진 문자열에서 시작, 끝 인덱스로 지정했을때 인덱스 내에 존재하는 문자열이 회문인지 확인하는 문제이다.

#### 풀이

- 입력으로 들어오는 인덱스의 경우가 많을 경우 일일히 찾아 매번 확인하는 것보다 미리 모든 문자열을 확인해 회문인지를 저장해두면 시간절약이 된다.
- 문자열에서 다음 두가지 조건을 만족하면 회문이 된다.
  - 앞뒤 문자가 같아야 한다. ex) 1, 2, 3, 4, 5
  - 앞뒤 문자를 제외한 나머지 문자가 회문이어야 한다. 212, 22122
- 앞뒤 문자를 제외할 수 없는 크기가 1인 문자부터 입력문자열의 크기까지 크기를 키워 회문인지 저장하면 모든 구간의 문자열이 회문인지 확인할 수 있다.

```java
//길이가 1인 문자는 반드시 회문이다.
for(int i = 1; i <= size; i++) {
	dp[i][i] = true;
}

// 길이가2인 구간은 앞,뒤가 같으면 팰린드롬이다.
// ex) 11, 22, 33
for(int i = 1; i < size; i++) {
	if(arr[i] == arr[i + 1]) {
		dp[i][i+1] = true;
	}
}

// i는 j부터 i만큼 떨어진 인덱스
// j는 시작 인덱스
// 조건1 : j부터 시작하는 문자열에서 j+i하여 문자열의 끝과 같은지 비교
// 조건2 : 시작인덱스로 부터 다음칸과 끝 인덱스에 전의 문자가 회문이었는지 비교
for(int i = 2; i < size; i++) {
	for(int j = 1; j <= size - i ; j++) {
        // 조건1				// 조건 2
		if(arr[j] == arr[j + i] && dp[j+1][i + j -1] == true) {
			dp[j][j + i] = true;
		}
	}
}
```

### 1254 팰린드롬 만들기

- 주어진 입력문자열을 회문으로 만들어야 하는 문제이다
- 단 주어진 입력문자열에 존재하는 문자만을 가지고 추가하야 가장 짧은 회문을 만들어야한다.

#### 풀이

- 회문의 조건은 두 가지가 있다

  - 앞뒤문자가 같아야 한다.
  - 앞뒤문자열을 제외한 문자열이 회문이어야 한다.
- 입력으로 주어진 문자열을 회문조건에 맞추어 풀어야 한다.
- 앞뒤문자열이 같아야 한다는 조건은 입력으로 주어진 문자열에 문자가 추가될 경우를 이용해야 한다.
- 입력이 `abab`일 경우

  - 해당 문자가 회문인지 먼저 확인
- 아닐 경우 회문 첫번째 조건에 따라 인덱스0문자를 추가한다.
  
  - `ababa` 두가지 조건을 만족한다.
  - 만약 조건에 맞지 아닐 경우 인덱스0부터 1까지 문자를 reverse하여 추가한다.
    - `ababba` 조건에 맞지 않음
  - 계속해서 끝 인덱스를 입력 문자열 크기만큼 추가해 나간다.
    - `abababa`, `ababbaba` 까지 나올 수 있음
- 하지만 첫번째 조건만을 확인한 것이므로 두번재 조건으로 미리 reverse해서 추가할 문자열을 제외한 나머지 문자열이 회문인지를 확인해야한다.
- 이는 `10942 팰린드롬?`에서 사용한 방법과 같게 미리 회문인지를 구할 수 있다.

- 그리고 시작인덱스부터 마지막인덱스까지 해당 문자열이 가장 큰 값을 다음과 같이 찾는다.

```java
int temp = -1;
for(int i = 1; i <= size; i++) {
    //시작 인덱스 i부터  마지막 인덱스까지 회문이진 확인
	if(dp[i][size] == true) {
        //회문일 경우 REVERSE해서 추가로 붙일 문자를 제외한 나머지 문자의 크기를 담는다
		temp = Math.max(temp, size - i + 1);
	}
}
//최악인 전체문자를 rever해서 붙인 경우에서
//reverse해서 추가로 붙일 문자열의 크기를 제외한 크기와 빼준다
System.out.println(size + size - temp);
```

- 입력으로 주어진 문자가 처음부터 회문이면 `temp`는 기존문자열 크기가 된다.
- 그리고 `기존문자열 크기 + (기존문자열크기 - (rever를 할 문자를 제외한 회문))`가 정답이 된다.