# Reset vs Revert

## reset
> 공개된 저장소에 push된 이력은 절대 reset하지 않는다
```bash
$ git reset {해시코드}
```
* 기본(--mixed) : 이후 변경 사항을 wd에 유지시켜줌

* --hard : 이후 변경사항을 모두 삭제됨

* --soft : 지금 작업하고 있는 내용 및 변경사항을 we에 유지시켜줌



## revert

> 해당 커밋으로 되돌렸다라는 이력(revert)을 남긴다

```bash
$ git revert {해시코드}
```

* vim -> 커밋 메시지 작성