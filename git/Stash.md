# Stash

> 변경사항을 임시로 저장하는 공간
>
> 마지막 커밋 시점으로 되돌려준다

```
1. feature branch 에서 a.txt 변경 후 커밋
2. master branch 에서 a.txt 수정 (add, commit 없이)
3. merge
```

```bash
$ git merge feature
error: Your local changes to the following files would be overwritten by merge:
        a.txt
Please commit your changes or stash them before you merge.
Aborting
Updating e4b1f5d..a9e1f2e
```
### 명령어

stash 저장

```bash
$ git stash
Saved working directory and index state WIP on master: e4b1f5d update a.txt
```

stash 목록

```bash
$ git stash list
stash@{0}: WIP on master: e4b1f5d update a.txt
```

stash 불러오기

```bash
$ git stash pop # 불러오기 + 목록에서 삭제
# $ git stash apply 불러오기
# $ git stash drop 목록에서 삭제
```

### 해결

```bash
$ git stash # 임시공간 저장
$ git merge feature # 병합 후에
$ git stash pop # 임시 공간에서 불러오기

#충돌 발생, 해결 후 작업 이어가기
```

```
<<<<<<< Updated upstream
수정수정
=======
마스터마스터
>>>>>>> Stashed changes
```

