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

- 미디어 데이터를 저장할 때는 MediaStore를 이용하기를 권장한다.

- Android P 이하와 Q에서 MediaStore에 쓰기에 대해 알아본다.

### 권한

- MediaStore는 데이터를 쓰기는 읽기와 다르게 별도의 권한을 요구하지 않는다.

### contentValue

- 기본 사이즈를 갖는 빈 값, ContentValue를 생성하고 해당 값에 Media file에 대한 정보를 입력한다.

```kotlin
val values = ContentValues().apply {
    put(MediaStore.Images.Media.DISPLAY_NAME, file_name)
    put(MediaStore.Images.Media.MIME_TYPE, file_mime_type)
    put(MediaStore.Images.Media.IS_PENDING, 1)
}

val collection = MediaStore.Images.Media.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY)
val uri: Uri = contentResolver.insert(collection, values)
```

- 읽기와 마찬가지로 MediStore 에 정의된 media타입에 맞는 값들을 지정해준다.

- 이제 item: Uri에 파일을 쓰기할 수 있게 되었다.

#### 저장 경로

- 해당 파일을 insert하면 다음 `/sdcard/Pictures` 경로에 저장되게 된다.
- 만약 다른 경로에 저장하고 싶다면 contentValues에 값을 추가하면 된다.

```kotlin
// pictures/myImage
val path = Environment.DIRECTORY_PICTURES + File.separator + "myImage"

val values = ContentValues().apply {
  // anohther option
  // write next code
  put(MediaStore.Images.Media.RELATIVE_PATH, path)
}
```

#### IS_PENDING?

- 앱이 미디어 파일에 쓰기 작업을 하는 것과 같이 시간이 많이 소요될 수 있는 작업을 실행한다면 작업을 처리하는 동안 파일에 독점적으로 액세스하는 것이 유용합니다.
- 미디어 파일을 쓰기 작업하는데 다소 시간이 소유된다면 해당 파일을 처리하는 앱에서만 접근하여 사용하는 것이 유용하다.
- 그래서 contentValue에 `IS_PENDING` 값을 1로 설정하여 해당 앱에서만 처리할 권한을 얻는다.

### Write

- uri로 fileDescriptor를 얻고 이를 이용하여 파일을 쓰기해준다.
- 웹에서 받은 `Okhhp3.ResponseBody` 타입의 이미지인 경우 다음과 같이 파일을 저장할 수 있다.

> android q에서는 write권한이 없기 때문에 절대경로 알 수 없다.

```kotlin
val body = api.getResposeBody()

contentResolver.openFileDescriptor(uri, "w", null)?.also { pdf ->
    val fos = FileOutputStream(pdf.fileDescriptor)
    fos.write(body.bytes)
    fos.close()
    pdf.close()
}
```

### Update

- 쓰기 후 이제 해당 파일의 `IS_PENDING` 값을 0으로 설정하여 다른 앱에서 접근할 수 있도록 한다.

```kotlin
values.put(MediaStore.Images.Media.IS_PENDING, 0)
contentResolver.update(uri, values, null, null)
```



.......
