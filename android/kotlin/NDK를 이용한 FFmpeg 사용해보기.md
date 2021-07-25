# NDK를 이용한 FFmpeg사용해보기

- JVM위에서 돌아가는 android에서는 C로 작성된 FFmpeg를 실행하는데 어려움이 있다. 
- 이를 안드로이드 ndk를 이용하여  FFmpeg를 사용할 수 있다.

> **FFmpeg**은 디지털 음성 스트림과 영상 스트림에 대해서 다양한 종류의 형태로 기록하고 변환하는 컴퓨터 프로그램이다.

## 설치

- 여러 관련 글들이 존재하는데 너무 오래되고 FFmpeg 소스파일을 컴파일하는데 사용되는 빌드 스크립트가 대부분 다르고 해서 최신버전을 기준으로 작성한다.
- 설치환경
  - Mac 10.15.7
  - Androd Studiio 4.1.2
  - NDK 21.1
  - FFmpeg 4.3.1

- 21.7.25일 기준 안드로이드 스튜디오는 4.2, FFmpeg는 4.4, NDK는 23까지 존재하는데 이부분들을 최신버전으로 해도 사용될 수 있다.

### 프로젝트 생성

- 프로젝트 생성을 하는데 Native Project로 생성한다.

<div><img src="https://user-images.githubusercontent.com/58923717/126887466-13024d18-cd1d-4bf0-b998-fcbd7a4cf069.png"  /></div>

- 그러면 프로젝트 구조에서 cpp이라는 폴더가 새롭게 나타나고 MainActivity에는 `external fun stringFromJNI(): String` 함수가 새롭게 추가된것을 볼 수 있다.
### NDK 설치

- Android SDK -  SDK Tools에서 다음을 받는다
  - NDK (Side by side)
  - CMake

<div>
  <img src="https://user-images.githubusercontent.com/58923717/126888043-f440f387-3609-4d38-887c-43a32ac909eb.png" />
</div>

### FFmpeg 소드코드

- 이제 빌드 스크립트를 사용하여 FFmpeg 소스코드를 안드로이드에 맞게 얻어야한다.
- https://ffmpeg.org/download.html 에서 소스코드를 받는다.

> 한 번에 소스코드를 받고 처리해줄 수 있는 내용이 아래 작성되어 있다. 굳이 안받아도 된다.

- 이후 압축을 푼 후에 내부에 `configure` 파일을 수정한다.

```
before
SLIBNAME_WITH_MAJOR='$(SLIBNAME).$(LIBMAJOR)'
LIB_INSTALL_EXTRA_CMD='$$(RANLIB) "$(LIBDIR)/$(LIBNAME)"'
SLIB_INSTALL_NAME='$(SLIBNAME_WITH_VERSION)'
SLIB_INSTALL_LINKS='$(SLIBNAME_WITH_MAJOR) $(SLIBNAME)'

after
SLIBNAME_WITH_MAJOR='$(SLIBPREF)$(FULLNAME)-$(LIBMAJOR)$(SLIBSUF)'
LIB_INSTALL_EXTRA_CMD='$$(RANLIB) "$(LIBDIR)/$(LIBNAME)"'
SLIB_INSTALL_NAME='$(SLIBNAME_WITH_MAJOR)'
SLIB_INSTALL_LINKS='$(SLIBNAME)'
```

- 그리고 최상위 폴더에 다음 스크립트를 작성하도록 한다.

```shell
#!/bin/bash

NDK=/Users/[YOUR_USER_NAME]/Library/Android/sdk/ndk/[YOURE_VERSION]
SYSROOT=$NDK/toolchains/llvm/prebuilt/darwin-x86_64/sysroot
TOOLCHAIN=$NDK/toolchains/llvm/prebuilt/darwin-x86_64

function build_one
{
./configure \
 --prefix=$PREFIX \
 --enable-shared \
 --disable-static \
 --disable-doc \
 --disable-ffmpeg \
 --disable-ffplay \
 --disable-ffprobe \
 --disable-ffserver \
 --disable-avdevice \
 --disable-doc \
 --disable-symver \
 --cross-prefix=$TOOLCHAIN/bin/arm-linux-androideabi- \
 --target-os=android \
 --arch=arm \
 --enable-cross-compile \
 --sysroot=$SYSROOT \
 --extra-cflags="-Os -fpic $ADDI_CFLAGS" \
 --extra-ldflags="$ADDI_LDFLAGS" \
 $ADDITIONAL_CONFIGURE_FLAG

make clean
make
make install
}

CPU=arm
PREFIX=$(pwd)/android/$CPU
ADDI_CFLAGS="-marm"
build_one
```

- 일반적으로 안드로이드 ffmpeg 빌드 스크립트를 찾으면 위와 같은 형태인데 약간 NDK폴더 구조가 다른경우가 존재하는데 이를 수정해줘야한다.

> 옛날 글을 보면 ndk폴더 경로에 ndk-bundle이라고 들어가 있는데 이는 레거시이다.

- 위 스크립트를 사용하는 것도 좋겠지만 https://github.com/Javernaut/ffmpeg-android-maker 이 git을 확인해서 한번에 ffmpeg 소스코드를 받고 configure수정해주고 cpu타입별 소스코드를 받을 수 있도록 한다.
- 사용방법은 터미널로 해당 폴더 까지 들어 간 후 다음 값을 지정한다.

```
export ANDROID_SDK_HOME=/Users/[YOUR_USER_NAME]/Library/Android/sdk
export ANDROID_NDK_HOME=/Users/[YOUR_USER_NAME]/Library/Android/sdk/ndk/[YOURE_VERSION]
```

- 추가적으로 타켓 API나 ffmpeg버전을 바꾸고 싶다면 script폴더에 있는 `parse-arguments.sh`에서 API와 ffmpeg 버전을 수정해주면 된다.

### 빌드 후

- 스크립트가 빌드가 끝났다면 폴더에 output에 타입별 4가지 폴더가 생성되어있을 것이다.
- 이를 안드로이드 프로젝트에 다음과 같이 위치시킨다.

<div><img src="https://user-images.githubusercontent.com/58923717/126887810-9c811126-86c4-4def-86ac-8f284cdacd42.png"  /></div>

> 기존과 다른 파일들은 일단 무시한다.

- 그 후 해당 파일들이 실제을 인식시켜줄 수 있도록 CMakeLists를 수정해줘야 한다.

```tex
# Declares and names the project.

project("YOUR_PROEJCT_NAME")

set(ffmpeg_dir ${CMAKE_SOURCE_DIR}/)
set(ffmpeg_libs ${ffmpeg_dir}/lib/${ANDROID_ABI})

include_directories(${ffmpeg_dir}/include/${ANDROID_ABI})

set(
        # List variable name
        ffmpeg_libs_names
        # Values in the list
        avutil avformat avcodec swscale avdevice avfilter swresample)

foreach (ffmpeg_lib_name ${ffmpeg_libs_names})
    add_library(
            ${ffmpeg_lib_name}
            SHARED
            IMPORTED)
    set_target_properties(
            ${ffmpeg_lib_name}
            PROPERTIES
            IMPORTED_LOCATION
            ${ffmpeg_libs}/lib${ffmpeg_lib_name}.so)
endforeach ()


add_library( # Sets the name of the library.
             native-lib

             # Sets the library as a shared library.
             SHARED

             # Provides a relative path to your source file(s).
             native-lib.cpp )


find_library( # Sets the name of the path variable.
              log-lib

              # Specifies the name of the NDK library that
              # you want CMake to locate.
              log )


target_link_libraries( # Specifies the target library.
                       native-lib
        							 ${ffmpeg_libs_names}
                       # Links the target library to the log library
                       # included in the NDK.
                       ${log-lib} )
```

### 샘플 C

```c
#include <jni.h>
#include "libavformat/avformat.h"

#include <android/log.h>
#define LOG_TAG "FFmpegForAndroid"
#define LOGI(...) __android_log_print(4, LOG_TAG, __VA_ARGS__);
#define LOGE(...) __android_log_print(6, LOG_TAG, __VA_ARGS__);


jint JNICALL
Java_YOUR_PROJECT_PACKAGE_METHOD(JNIEnv *env, jobject thiz, jstring filepath) {
  
    const char* nativeFilepath = (*env)->GetStringUTFChars((env),
                                                          (filepath), NULL) ;

    AVFormatContext* avFormatContext = NULL;

    // muxer, demuxer, decoder, encoder 초기화
    av_register_all();

    // nativeFilepath로 avFormatContext 가져오기

    if(avformat_open_input(&avFormatContext, nativeFilepath, NULL, NULL) < 0)
    {
        LOGE("Can't open input file '%s'", nativeFilepath);
        (*env)->ReleaseStringUTFChars(env, filepath, nativeFilepath);
        return -1;
    }

    // 유효한 스트림 정보 찾기
    if(avformat_find_stream_info(avFormatContext, NULL) < 0)
    {
        LOGE("Failed to retrieve input stream information");
        (*env)->ReleaseStringUTFChars(env, filepath, nativeFilepath);
        return -2;
    }

    // avFormatContext->nb_streams : 비디오 파일의 전체 스트림 수
    for(unsigned int index = 0; index < avFormatContext->nb_streams; index++)
    {
        AVCodecParameters* avCodecParameters = avFormatContext->streams[index]->codecpar;
        if(avCodecParameters->codec_type == AVMEDIA_TYPE_VIDEO)
        {
            LOGI("------- Video info -------");
            LOGI("codec_id : %d", avCodecParameters->codec_id);
            LOGI("bitrate : %lld", avCodecParameters->bit_rate);
            LOGI("width : %d / height : %d", avCodecParameters->width, avCodecParameters->height);
        }
        else if(avCodecParameters->codec_type == AVMEDIA_TYPE_AUDIO)
        {
            LOGI("------- Audio info -------");
            LOGI("codec_id : %d", avCodecParameters->codec_id);
            LOGI("bitrate : %lld", avCodecParameters->bit_rate);
            LOGI("sample_rate : %d", avCodecParameters->sample_rate);
            LOGI("number of channels : %d", avCodecParameters->channels);
        }
    }

    // release
    if(avFormatContext != NULL)
    {
        avformat_close_input(&avFormatContext);
    }

    // release
    (*env)->ReleaseStringUTFChars(env, filepath, nativeFilepath);

    return 0;
}


//출처: https://prompt-dev2.tistory.com/79?category=100139 [프람트 MoS 사업부]
```

### MainActivity

```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val videoIntent = Intent(Intent.ACTION_PICK).apply {
            type = "video/*"
        }
        val button = findViewById<Button>(R.id.buttonOpen)
        button.setOnClickListener {
            startActivityForResult(videoIntent, 100)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (resultCode == RESULT_OK && requestCode == 100) {
            val uri = data?.data

            getRealPathFromURI(uri)?.let {
                testCode(it)
            }
        }
    }


    fun getRealPathFromURI(contentUri: Uri?): String? {
        val proj = arrayOf(MediaStore.Images.Media.DATA)
        val cursor: Cursor? = contentResolver.query(contentUri!!, proj, null, null, null)
        cursor?.moveToNext()
        val path: String? = cursor?.getString(cursor.getColumnIndex(MediaStore.MediaColumns.DATA))
        val uri = Uri.fromFile(File(path!!))
        cursor?.close()
        return path
    }

    external fun stringFromJNI(): String
    external fun testCode(filepath: String): Int

    companion object {
        init {
            System.loadLibrary("native-lib")
        }
    }
}
```
### Manifest
```xml
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```
- 위와 같이 소스코드를 작성하면 지정된 파일에 대한 간단한 정보를 ffmpeg소스코드를 이용하여 출력하게 된다.
- 그리고 핸드폰 애플리케이션에서 해당 프로젝트에서 파일 권한을 허용시켜주도록한다. (혹은 권한 관련 코드를 작성한다)



























































