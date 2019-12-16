# GIT 기초

## 0. 준비사항

* [git bash](https://gitforwindows.org/)에서 다운받기
  * git을 활용하기 위한 'CLI(Command Line Interface)'를 제공한다.
  * source tree, github, desktop 등을 통해 GUI환경에서도 활용 가능하다.



# 1. 로컬 저장소 활용하기

### 1. 저장소 초기화

```bash
$ git init
Initialized empty Git repository in C:/Users/student/Desktop/TIL/.git/
```

* 저장소(repository)를 초기화 하게되면, `.git`폴더가 해당 디렉토리에 생성된다.
* bash 창에서는 (mater) 라고 표기된다.
  * 현재 브랜치가 master 라는 것을 의미함.

## 2. Add - staging area

> git으로 관리되는 파일들은 Working directroy(작업환경), Staging Area, Commit 단계를 거쳐 이력에 저장된디.

``` bash
$ git add a.txt # 파일명
$ git add images #  폴더명
$ git add . # 현재 디렉토리의 모든 파일 및 폴더
```



