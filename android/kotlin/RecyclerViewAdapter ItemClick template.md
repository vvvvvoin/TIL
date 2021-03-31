# RecyclerViewAdapter ItemClick

- ItemHolder와 onBindViewHolder에서 클릭이벤트를 activity/fragment에서 처리할 수 있도록 한다.

```kotlin
class NationAdapter : RecyclerView.Adapter<NationAdapter.ItemHolder>() {

    var list = ArrayList<Data>()
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int){ ... }

    override fun onBindViewHolder(holder: ItemHolder, position: Int) {
        itemListener?.let { itemListener ->
            holder.layout.setOnClickListener {
                itemListener.onClickListener(it, list[position])
            }
        }
    }

    override fun getItemCount(): Int { ... }

    inner class ItemHolder() : RecyclerView.ViewHolder(binding.root) { ... }

    var itemListener : ItemListener? = null
    interface ItemListener{
        fun onClickListener(view : View, data : Data)
    }

    fun onItemClick(listener: (view : View, data : Data) -> Unit) {
        itemListener = object : ItemListener{
            override fun onClickListener(view: View, data: Data) {
                listener(view, data)
            }
        }
    }

}
```

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    
    nationAdapter.onItemClick { view, data ->                                  
        //click event
    }
    
}
```

