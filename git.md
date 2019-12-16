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

* add 전 상태

``` bash
$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        git.md
        image/
        markdown.md

nothing added to commit but untracked files present (use "git add" to track)
```

* add 후 상태

``` bash
$ git add .
$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   git.md
        new file:   image/1c9d3bc79f6b5ab777b6aca64f1a8661.png
        new file:   markdown.md
```



## Commit

> Commit은 코드의 이력을 남기는 과정이다.

``` bash
$ git commit -m {커밋 메세지}
[master (root-commit) bd35297] 마크다운 및 git기초 정리
 3 files changed, 128 insertions(+)
 create mode 100644 git.md
 create mode 100644 image/1c9d3bc79f6b5ab777b6aca64f1a8661.png
 create mode 100644 markdown.md
```

* 커밋 메세지는 항상 해당 이력에 대한 정보를 담을 수 있도록 작성하는 것이 좋다.
* 일관적인 커밋 메세지를 작성하는 습관을 들이자.
* 이력 확인을 위서는 아래의 멍령어를 활용한다.

``` bash
$ git log
commit bd35297450bc7351b08bff107993558fde1b85ff (HEAD -> master)
Author: vvvvvoin <aszx7009@gmail.com>
Date:   Mon Dec 16 14:28:15 2019 +0900

    마크다운 및 git기초 정리
```

**항상 status 명령어를 통해 git의 상태를 확인하자**

**commit 이후에는 log명령어를 통해 이력들을 확인하자**

