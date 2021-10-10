# Android MediStore 읽기/쓰기

- Andorid 10에서 `Scoped Storage`가 적용되어 Media파일은 MediaStore API를 이용하여 읽기/쓰기를 해야합니다.

## 읽기

### 권한

- MediaStore의 파일을 읽기 위해서는 다음 권한을 필요로 합니다.

```xml
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

### 쿼리

- 실제 MediaStore의 파일에 접근하기 위해서는 쿼리를 만들어야 합니다.
- 쿼리는 크게 5개의 값들을 가지고 있고 사용자가 이를 설정해서 원하는 결과(cursor)를 얻을 수 있습니다.

```java
public final @Nullable Cursor query(@RequiresPermission.Read @NonNull Uri uri,
            @Nullable String[] projection, @Nullable String selection,
            @Nullable String[] selectionArgs, @Nullable String sortOrder)
```

- uri : 찾고자하는 uri를 명시, content:// scheme를 의미
- projection : 각 Media에 있는 MediaColumns값을 넣어 해당 column들을 받게 됨
  - MediaStore.Image, MediaStore.Video, .... 에 정의된 id, name 등을 받아옴
- selection : DB의 where문과 동일한 조건식, 필터링 역할을 수행함
- selctionArgs : 조건식의 인자값을 지정함
- sortOrder : 정렬조건

```kotlin
// id, display_name, date_taken column을 지정
val projection = arrayOf(
    MediaStore.Images.Media._ID,
    MediaStore.Images.Media.DISPLAY_NAME,
    MediaStore.Images.Media.DATE_TAKEN
)

// date_taken 은 long 값으로 시간값이 저장되어 있다.
val selection = "${MediaStore.Images.Media.DATE_TAKEN} >= ?"
val selectionArgs = arrayOf(
    dateToTimestamp(day = 1, month = 1, year = 1970).toString()
)

// 오름차순 : "${MediaStore.Images.Media.DATE_TAKEN} ASC"
val sortOrder = "${MediaStore.Images.Media.DATE_TAKEN} DESC"

val cursor = contentResolver.query(
    MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
    projection,
    selection,
    selectionArgs,
    sortOrder
)

private fun dateToTimestamp(year: Int, month: Int, day: Int): Long {
    return SimpleDateFormat("yyyy.MM.dd", Locale.getDefault()).parse("$year.$month.$day")?.time ?: 0
}
```

### 커서

- 쿼리로 부터 얻은 커서로 받아온 데이터의 컬럼을 확인하고 처리한다.
- column에는 projectino에 작성된 값이 넘어옵니다.
- `getColumnIndexOrThrow`를 이용하여 column index를 받아온다.

```kotlin
val idColumn = cursor.getColumnIndexOrThrow(MediaStore.Images.Media._ID)
val dateTakenColumn =
    cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATE_TAKEN)
val displayNameColumn =
    cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DISPLAY_NAME)

while (cursor.moveToNext()) {
    val id = cursor.getLong(idColumn)
    val dateTaken = Date(cursor.getLong(dateTakenColumn))
    val displayName = cursor.getString(displayNameColumn)
    val contentUri = Uri.withAppendedPath(
        MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
        id.toString()
    )
}
```
- 다음과 같은 결과를 받을 수 있다.

```tex
id: 2830, display_name: 20150329_190719.jpg, date_taken: Thu Jan 01 09:00:00 GMT+09:00 1970, content_uri: content://media/external/images/media/2830
```

- 결과의 uri를 통해 view에 보여줄 수 있다.

## 쓰기
