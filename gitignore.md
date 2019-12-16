# Gitignore

> Git을 통한 프로젝트 시작시 반드시 설정하자

# 활용법

`.gitignore`파일을 생성 후 git으로 관리하지 않을 파일의 목록을 작성한다.

```
*.xlsx 	#확장자가 xlsx인 모든 파일
test/ 	#test폴더
a.txt 	#특정파일
```

보통 `.gitignore`에 등록되는 파일은 IDE설정과 관련된 내용 혹은 프로그래밍 언어별 임시 파일, 윈도우 등 os 관련 파일을 등록한다.(프로젝트 소스코드와 무관)

잘 모르는 경우 해당 환경을 [gitignore.io](http://gitignore.io/)에서 검색하여 설정하자.

예) eclipse, java, window, ....

