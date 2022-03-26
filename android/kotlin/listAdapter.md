# ListAdapter

## 용도

- listAdapter는 recyclerView에서 변경되어야 하는 아이템을 갱신할 때 notifyXXX 메서드를 이용하는 경우를 diffUtil이라는 것을 이용하여 비동기로 처리하는 recylcerView.adapter의 래핑클래스이다.

## 사용방법

```kotlin
class MainAdapter : ListAdapter<Book, MainViewHolder>(mainAdapterDiffUtil) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MainViewHolder {
        return MainViewHolder.newInstance(parent, onMainItemClickListener)
    }

    override fun onBindViewHolder(holder: MainViewHolder, position: Int) {
        holder.bind(getItem(position))
    }
    
    companion object {
        val mainAdapterDiffUtil = object : DiffUtil.ItemCallback<ChannelBooksResponse.Book>() {
            override fun areItemsTheSame(oldItem: ChannelBooksResponse.Book, newItem: ChannelBooksResponse.Book): Boolean {
                return oldItem.isbn == newItem.isbn
            }

            override fun areContentsTheSame(oldItem: ChannelBooksResponse.Book, newItem: ChannelBooksResponse.Book): Boolean {
                return oldItem == newItem
            }
        }
    }
}

data class Book(
  val isbn: String,
  val title: String?,
  val author: List<String>?,
  val publisher: String?,
  val content: String?,
  val price: String?,
)

val adapter = MainAdapter()
adapter.submitList(YOUR_ITEM_LIST)
```

- 일반적으로 사용하던 recyclerView.adapter에 비해 간단하게 생긴것을 확인할 수 있다.
- 리스트를 세팅해주기 위해서는 따로 adapter내부에 만들어줄 수 있거나 곧 바로 `submitList`를 이용할 수 있다.
- 내부적으로 AsyncListDiffer가 멀티스레드로 사용자가 정의한 `areItemsTheSame`, `areContentsTheSame`를 통해 갱신할 아이템을 인식하게 된다.
  - areItemsTheSame - 비교되는 두 아이템이 같은 지를 체크한다. 각 아이템의 고유 id값일 수 있거나 아이템의 래퍼런스일 수 있다.
  - areContentsTheSame - 비교되는 두 아이템의 내부 값이 동일한지 체크한다. `==`, `equals`를 사용할 수 있는데, 이 때에는 equals를 오버라이딩해주거나 data class를 ㅇ 이용해야 한다.

## 주의사항

### 래퍼런스가 같은 리스트는 submitList해도 갱신하지 못한다.

- 하나의 래퍼런스를 submitList로 갱신 후에 해당 리스트의 값을 변경 후에 다시 submitList하게 된다면 newList와 mList는 같기 대문에 갱신되지 않고 return되게 된다.
- 만약 activity, presenter에서 하나의 래퍼런스를 참고하여 사용해야 된다면 `toList()`, `toMutableList()`로 해결할 수 있다.

```java
public void submitList(@Nullable final List<T> newList,@Nullable final Runnable commitCallback) {
  // incrementing generation means any currently-running diffs are discarded when they finish
  final int runGeneration = ++mMaxScheduledGeneration;

  if (newList == mList) {
    // nothing to do (Note - still had to inc generation, since may have ongoing work)
    if (commitCallback != null) {
      commitCallback.run();
    }
    return;
  }
  
  //....
}
```

### 외부에 대한 인터렉션으로 리스트를 갱신해야하는 경우 아이템이 동영상같은 비동기 처리로 동작하는 경우 잘못된 표시가 될 수 있다.

- 리스트 어댑터는 diff를 계산하고 변경해야할 경우가 된다면 자연스러운 애니메이션이 나타나는 것을 볼 수 있다.
- 하지만 이러한 애니메이션으로 문제가 되는 엣지케이스에 대해서 설명한다.
- viewPager혹은 recylcerView에 listAdapter를 사용하고 아이템으로 exoPlayer를 사용하는 경우에 부득이하게 아이템을 갱신할 때 전체 리스트를 submitList하지 않고 해당 아이템만 `notifyItemChanged`를 하게 될 경우 표시되는 부분이 어색하게 나타날 수 있다.
- 아래 영상을 예로 들면 exoPlayer를 갖는 커스텀뷰에 소리 on/off에 대한 결과를 바인딩시키기 위해 notifyItemchaged를 하면서 onBindViewHolder가 호출되고 바인드 되는 과정에서 애니메이션이 적용되면서 약간 깜박임이 보인다. 근데 이 애니메이션은 똑같은 viewHolder가 하나의 포지션에 위치해서 교체되기 때문에 동영상 동작이 잘 못될 수 있다. 해당 커스텀뷰는 같은 영상일 경우 새롭게 교체시키지 않도록 해두었지만 이상동작을 나타내고 있다.

https://user-images.githubusercontent.com/58923717/160229596-cf8abdee-6ba9-4ea1-b0b6-2c5ea8b8ea51.mp4

- 해결책은 간단하게 사용하는 recylcerView의 itemAnimator = null으로 설정하면 해결된다. listAdapter가 notifyXXX를 직접호출해서 사용하게 의도된 것은 아니지만 동영상같은 처리에서는 어색하게 표시될 수 있다.