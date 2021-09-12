# Glide

## Listener

- 리스너를 이용하여 이미지 로드에 대한 실패와 성공시 사전 처리를 수행할 수 있도록 한다.
- 일반적으로 웹에서 이미지를 받아올 경우 유용하게 사용될 수 있다.

```kotlin
Glide.with(context)
        .asDrawable()
        .listener(object : RequestListener<Drawable> {
            override fun onLoadFailed(e: GlideException?, model: Any?, target: Target<Drawable>?, isFirstResource: Boolean): Boolean {
                // 로드 실패시
                return false
            }
            override fun onResourceReady(resource: Drawable?, model: Any?, target: Target<Drawable>?, dataSource: DataSource?, isFirstResource: Boolean): Boolean {
                // 로드가 성공적으로 완료되기 직전에 onResourceReady가 호출된다.
                return false
            }

        })
        .into(binding.imageView)
```

