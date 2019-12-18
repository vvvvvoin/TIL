# Git status & undoing

## commit

파일 존재

```bash
$ git commit
On branch master

Initial commit

Untracked files:
        a.txt
# commit 할 것이 없음 -> staging area가 비어있음
# tracked 파일이 존재함 -> git commit 이력에 담기지 않은 파일은 있음
nothing added to commit but untracked files present
```

파일 없음

```bash
$ git commit
On branch master

Initial commit
# 어떠한 변경 사항도 없음.
nothing to commit
```

## status

파일생성 후 add 전

```bash
$ git status
On branch master

No commits yet
## commit 이력에 담긴 적 없는 파일
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        a.txt

nothing added to commit but untracked files present (use "git add" to track)
```

파일생성 후 add 후

```bash
$ git status
On branch master

No commits yet
## commit될 변경사항들
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   a.txt
```

## commit

> 부제 : vim 활용 기초

```bash
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch master
#
# Initial commit
# Changes to be committed:
#       new file:   a.txt
```

* 편집(입력)모드 :  `i`
  * 문서 편집 가능
* 명령모드  : `esc`
  * `dd` : 해달 줄 삭제
  * `:wq` : 저장 및 종료
    * `q` : 종료
    * `w` : 쓰기
  * `:q!` : 강제종료
    * `q` : 종료
    * `!` : 강제

```bash
$ git commit -m 'commit message'
```

* commit message 해당 작업이력을 나타낼 수 있도록 작성한다
* 일관적인 포맷으로 작성하도록 한다

## log

> 커밋은 해시값에 의해서 구분된다
>
> SHA-1 HASH 알고리즘을 사용하여 표현한다

```bash
$ git log
commit b2ef0deb8cbc5f621d3a2da20e3541ca542a8526
Author: vvvvvoin <aszx7009@gmail.com>
Date:   Wed Dec 18 09:45:13 2019 +0900

    a.txt 내용 추가
```

```bash
$ git log --oneline
$ git log -1
$ git log --oneline --graph
$ git log -1 --oneline
```

## commit undoing

1. commit message를 변경하고 싶을 때

```bash
$ git commit --amend
```

직전 commit message 수정하는 경우 해시 값이 변경되므로, 다른 이력으로 관리된다.

**따라서, 공개된 저장소에 이미 push된 경우 절대 수정해서는 안된다.**

2.  특정 파일 추가하기
   * c.txt 파일을 같이 커밋을 하려고 했는데, add 를 하지 않고 커밋해버렸다.

```bash
$ git add c.txt
$ git commit --amend
```

## staging area

### 1. 커밋 이력이 있는 파일 수정하는 경우

```bash
$ git status
On branch master
# 변경 사항인데, staging area가 아닌
Changes not staged for commit:
# git add로 staging area로 보낼 수 있다.
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   a.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

```bash
$ git add a.txt
$ git status
On branch master
Changes to be committed:
# unstage 하기 위해서
  (use "git restore --staged <file>..." to unstage)
        modified:   a.txt
```

### add 취소하기

```bash
$ git restore --staged <File>
```

* 구버전의 git 에서는 아래의 멍령어를 사용해야한다

  > ```bash
  > $ git reset HEAD <file>
  > ```

## WD 변화 삭제하기

> git 에서는 모든 commit 시점으로 되돌릴수는 있다.
>
> 다만, wd삭제하는 것은 되돌릴 수가 없다.

```bash
$ git resotre <file>
```

* 구버전 git 에서는 아래의 명령어를 사용해야 한다.

  > ```bash
  > $ git checkout -- <file>
  > ```

  

