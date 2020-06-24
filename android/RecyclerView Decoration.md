### RecyclerView Decoration

#### 기본 구분선 추가

- Activity, Fragment에서 추가

```java
RecyclerView recyclerView = view.findViewById(R.id.recyclerView);
LinearLayoutManager linearLayoutManager = new LinearLayoutManager(context, LinearLayoutManager.VERTICAL, false);

DividerItemDecoration dividerItemDecoration = new DividerItemDecoration(context, linearLayoutManager.getOrientation());

recyclerView.setLayoutManager(linearLayoutManager);
recyclerView.addItemDecoration(dividerItemDecoration);
```
#### Item간 여백 주기
- RecyclerView.ItemDecoration 상속받는 class 생성
- RecyclerDecoration.java
```java
public class RecyclerDecoration extends RecyclerView.ItemDecoration {

    private final int itemHeight;

    public RecyclerDecoration(int itemHeight) {
        this.itemHeight = itemHeight;
    }

    @Override
    public void getItemOffsets(@NonNull Rect outRect, @NonNull View view, @NonNull RecyclerView parent, @NonNull RecyclerView.State state) {
        super.getItemOffsets(outRect, view, parent, state);
        if(parent.getChildAdapterPosition(view) != parent.getAdapter().getItemCount() -1){
            outRect.bottom = itemHeight;
        }
    }
}
```

- Activity, Fragment에서 recyclerView에 addItemDecoration()
```java
RecyclerView recyclerView = view.findViewById(R.id.recyclerView);
LinearLayoutManager linearLayoutManager = new LinearLayoutManager(context, LinearLayoutManager.VERTICAL, false);

DividerItemDecoration dividerItemDecoration = new DividerItemDecoration(context, linearLayoutManager.getOrientation());
//새롭게 추가됨
RecyclerDecoration recyclerDecoration = new RecyclerDecoration(20);

recyclerView.setLayoutManager(linearLayoutManager);
recyclerView.addItemDecoration(dividerItemDecoration);
//새롭게 추가됨
recyclerView.addItemDecoration(recyclerDecoration);
```



- 구분선 없고 여백없음

<img src="image/리스트 구분없음여백없음.jpg" alt="구분선 없고 여백없음" style="zoom: 33%;" />


- 구분선 있고, 여백없음

<img src="image/리스트 구분있음여백없음.jpg" alt="구분선 있고, 여백없음" style="zoom: 33%;" />


- 구분선 있고 여백있음

<img src="image/리스트 구분있음여백있음.jpg" alt="구분선 있고 여백있음" style="zoom: 33%;" />






















