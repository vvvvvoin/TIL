# JWT (Json Web Token)

- jwt는 인증에 필요한 정보들을 암호화시킨 토근을 의미한다.
- 기존방식에는 세션과 쿠키가 존재한다.

### 세션과 쿠키

- 세션과 쿠키는 HTTP 프로토콜에서 나타나는 비연결성, 상태정보를 저장하지 않는 특징을 보완하기 위해 나온 개념이다.
- 사용자가 요청을 보내고 서버로부터 응답을 받으면 서로간에 연결이 끊기는 비연결성 때문에 상태정보가 저장되지 않는다.
- 이때문에 로그인정보가 필요하면 다시 로그인해서 요청을 보내야 한다.
- 이러한 문제를 해결하는 것이 세션과 쿠키이다.

### JWT 란?

- 세션과 쿠키는 서버 인증 방식이라고 하며서버의 세션이나 메모리, 디스크, DB등을 토해 관리된다.
- jwt는 인증받은 사용자들이 갖는 토큰이다.
- 서버에 요청을 하면 헤더에 토큰을 담아 보내도록 하여 유효성을 검사하게 된다.
- 토큰은 3가지로 구성된다.
  - Header : jwt를 검증하는데 필요한 정보를 가진 JSON객체는 base64 인코딩된 문자열이다.
    - typ(토큰타입), alg(알고리즘 방식을 지정, signature 및 코튼 검증에 사용됨)
  - Payload : 토큰으로 사용하는 데이터가 담기는 곳
  - Signature : header와 payload를 합친 후 비밀키와 함께 header의 해싱알고리즘으로 인코딩됨

### 동작원리

#### 기존방식 - 세션, 쿠키

<div>
    <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbARRUx%2FbtqGDQEf5p1%2FMBoTKadQziR8skS9DqSAxk%2Fimg.png" width=500 />
</div>

#### 토큰방식

<div>
    <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbBykLp%2FbtqGNDW0zyb%2FuhpMTVLp95PPMLKklbz1v0%2Fimg.png" width=500 />
</div>
### 어떻게 만들어지나?

- 위에서 말했듯이 header, payload, signature로 구성되어 있다.
- 그리고 header, payload에는 json형태로 데이터가 존재한다.

#### header, payload

- 각 json데이터를 base64 url로 인코딩하여 겉보기에 의미없는 값을 만든다.

#### signature

- header와 payload에서 생성된 값을 다시 base64 url 인코딩하여 signature값으로 갖는다.
- 그리고 각각에서 생성된 값을 `.`로 구분하면 합치면 JWT가 만들어 진다.
- 다음과 같은 데이터로 나타내어진다.

> ```
> eyJhbGciOiJFUzI1NiIsImtpZCI6IktleSBJRC9.eyJpYXQiOjE1ODYzNjQzMjcsImlzcyI6Imp
> pbmhvLnNoaW4ifQ.MEQCIBSOVBBsCeZ_8vHulOvspJVFU3GADhyCHyzMiBFVyS3qAiB7Tm_ME
> Xi2kLusOBpanIrcs2NVq24uuVDgH71M_fIQGg
> ```

- 이러한 값을 담아 서버에 전송하여 사용자를 구분할 수 있게 되고 암호하된 데이터를 전송할 수 있다.





> 참고 : [권한 인증방식 (tistory.com)](https://qjadud22.tistory.com/69), [JWT를 소개합니다. : NHN Cloud Meetup (toast.com)](https://meetup.toast.com/posts/239)

