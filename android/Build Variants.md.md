# Build Variants

- 개발하면서 개발 형태에 맞게 빌드 타입을 정하면 개발에 큰 도움이 될 수 있다.
- 디버그용, 테스트용, 배포용 등으로 타입(BuildType)으로 나눌 수도 있고 무료버전, 유료버전, 내수용, 수출용 등으로도 앱의 색(flavors)을 지정할 수 있다.
- 이러한 설정은 build.gradle에서 설정하는데 이 부분을 접근하는 것은 어색하고 어렵다.
- 이러한 설정을 어떻게하고 어떤 옵션이 있는지 알아본다.

## BuildType

- 빌드타입을 말 그대로 빌드의 타입을 나타낸다.
- 빌드타입을 나눈다는 것은 간단하게 디버그, 난독화, 패키지 서프픽스 등을 빌드 타입에 맞게 다룰 수 있게 된다.
- 일반적으로 처음 프로젝트를 생성하면 다음과 같은 build.gradle 이 작성되어 있다.

```groovy
android {
    compileSdkVersion 30
    buildToolsVersion "30.0.3"

    defaultConfig {
        applicationId "xxx.xxx"
        minSdkVersion 23
        targetSdkVersion 30
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
    }
}
```

- 그리고 `buildTypes`에 기본적으로 `release`가 있는 것을 볼 수 있고 이는 `Android Studio` 좌측 하단 탭에서 Build Variant에서도 확인할 수 있다.

<img width="344" alt="스크린샷 2021-11-27 오후 4 58 37" src="https://user-images.githubusercontent.com/58923717/143673355-59021b70-e625-4878-a316-0dd79df782e7.png">

- 기본값에는 `debug`도 포함되어 있고 설정을 추가하기 위해 build.gradled에 다음과 같이 추가한다.

```groovy
    buildTypes {
        // 배포용
        release {
            minifyEnabled true
            debuggable false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'

            buildConfigField 'boolean', 'DEBUG_MODE', "false"
        }

        // 내부 배포용
        inhouse {
            initWith release
          
            debuggable true

            applicationIdSuffix ".inhouse"
            signingConfig signingConfigs.debug
        }

        // 개발
        debug {
            applicationIdSuffix '.dubug'

            minifyEnabled false
            debuggable true

            buildConfigField 'boolean', 'DEBUG_MODE', "true"
        }
    }

```

- 옵션

  - minifyEnabled : 난독화 옵션 사용유무

    - 주의사항
      - 리플랙션을 쓰는 클래스, 라이브러리가 있는 경우 반드시 `proguard-rules.pro` 에 관련 내용 작성해야함.
      - 모델같은 경우도 API에서 받아온 값을 파싱시켜줄 수 없으므로 적절한 처리가 필요함

  - debuggable : 디버깅모드 활성 유무

  - buildConfigField : BuildConfigs.java에 원하는 상수 지정

    - 프로젝트를 빌드하게 될 경우 `BuildConfig.java`이 자동생성되고 이를 확인하면 다음과 같다.

    ```java
    package com.example.mybooks;
    
    public final class BuildConfig {
      public static final boolean DEBUG = Boolean.parseBoolean("true");
      public static final String APPLICATION_ID = "com.example.mybooks.dubug";
      public static final String BUILD_TYPE = "debug";
      public static final int VERSION_CODE = 1;
      public static final String VERSION_NAME = "1.0";
      // Field from build type: debug
      public static final boolean DEBUG_MODE = true;
    }
    ```

    - `DEBUG_MODE`상수가 `boolean`타입에 값이 `true`할당 된것을 확인할 수 있다.
    - buildConfigField 'TYPE' 'VALUE_NAME' 'VALUE'으로 작성하면 된다.

  - initWith : 상속받을 빌드 타입

    - 위에서는 release를 상속받았고 release에 설정된 옵션을 그대로 사용하겠다는 의미이다.
    - debuggable을 따로 false로 오버라이딩할 수 있다.

  - applicationIdSuffix : applicationId에 suffix를 붙임

    - suffix가 있을 경우 각 앱마다 다른 취급을 하기 때문에 하나의 단말에 다른 타입별로 앱을 설치할 수 있게 됨
    - 위쪽 BuilConfig.java `APPLICATION_ID`에서 suffix가 추가된 것을 확인 할 수 있다.

- 이외에도 여러 옵션이 존재하고 배워나가야함

## Flavors

- flavors에도 큰 분류(차원, dimension)가 필요하다.
- 분류는 무료/유료, 스토어별 등으로 개발자가 원하는 만큼 나눌 수 있게 된다.
- 큰 분류를 `flavorDimensions`에 값을 할당시켜준다.

```groovy
flavorDimensions "billing"
```

- 그리고 해당 dimension에 맞는 flavor를 추가한다.

```groovy
    flavorDimensions "billing"

    productFlavors {
        free {
            dimension "billing"
            applicationIdSuffix ".free"

            buildConfigField "String", "API_END_POINT", "\"example.com/free\""
        }
        pay {
            dimension "billing"
            applicationIdSuffix ".pay"

            buildConfigField "String", "API_END_POINT",  "\"example.com/pay\""
        }
    }
```

- 이때에 applicationSuffix는 flavor이 앞에 위치하게 된다.
- 그리고 Build Variants탭을 보면 빌드타입에 flavor별로 생성되게 된다.

<img width="303" alt="스크린샷 2021-11-27 오후 5 44 44" src="https://user-images.githubusercontent.com/58923717/143674703-eab9471a-79e1-415d-bbd0-ab39a824a30e.png">

- 주의해야할 점은 빌드타입 수 x FlavorDimensions 수 x 각 flavor 의 갯수만큼 생성되기 때문에 관리가 필요하다.
- **flavorDimensions**에 정의된 값은 **productFlavors**에서 적어도 하나 이상 할당(dimension) 받아야 빌드가 된다.