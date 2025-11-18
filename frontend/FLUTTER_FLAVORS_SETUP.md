# Flutter Flavors Setup Guide

This guide explains how to set up and use Flutter flavors for the Resume Builder application. Flavors allow you to maintain different configurations for development, staging, and production environments.

## Table of Contents

1. [What are Flavors?](#what-are-flavors)
2. [Android Setup](#android-setup)
3. [iOS Setup](#ios-setup)
4. [Running the App with Flavors](#running-the-app-with-flavors)
5. [Building for Release](#building-for-release)
6. [VS Code Configuration](#vs-code-configuration)
7. [Troubleshooting](#troubleshooting)

## What are Flavors?

Flavors (also called build variants or configurations) allow you to create multiple versions of your app with different:
- API endpoints
- App names
- Bundle identifiers
- Icons
- Feature toggles
- Analytics configurations

Our app has three flavors:
- **dev**: Development environment (localhost:8000)
- **staging**: Staging environment
- **prod**: Production environment

## Android Setup

### 1. Update `android/app/build.gradle`

Add the following configuration to your `android/app/build.gradle` file:

```gradle
android {
    // ... existing config ...

    defaultConfig {
        applicationId "com.yourcompany.resumebuilder"
        minSdkVersion flutter.minSdkVersion
        targetSdkVersion flutter.targetSdkVersion
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
    }

    flavorDimensions "environment"

    productFlavors {
        dev {
            dimension "environment"
            applicationIdSuffix ".dev"
            versionNameSuffix "-dev"
            resValue "string", "app_name", "Resume Builder DEV"
        }

        staging {
            dimension "environment"
            applicationIdSuffix ".staging"
            versionNameSuffix "-staging"
            resValue "string", "app_name", "Resume Builder STAGING"
        }

        prod {
            dimension "environment"
            resValue "string", "app_name", "Resume Builder"
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.debug
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

### 2. Update AndroidManifest.xml

Replace the hard-coded app name with the flavor-specific name in `android/app/src/main/AndroidManifest.xml`:

```xml
<application
    android:label="@string/app_name"
    android:icon="@mipmap/ic_launcher">
    <!-- rest of configuration -->
</application>
```

### 3. Create Flavor-Specific Icons (Optional)

Create separate icon sets for each flavor:

```
android/app/src/dev/res/mipmap-*/ic_launcher.png
android/app/src/staging/res/mipmap-*/ic_launcher.png
android/app/src/prod/res/mipmap-*/ic_launcher.png
```

## iOS Setup

### 1. Open Xcode

```bash
cd ios
open Runner.xcworkspace
```

### 2. Create Build Configurations

1. Select the **Runner** project in Xcode
2. Go to **Info** tab
3. Under **Configurations**, click **+** to duplicate:
   - Duplicate `Debug` → `Debug-dev`
   - Duplicate `Debug` → `Debug-staging`
   - Duplicate `Debug` → `Debug-prod`
   - Duplicate `Release` → `Release-dev`
   - Duplicate `Release` → `Release-staging`
   - Duplicate `Release` → `Release-prod`

### 3. Create Schemes

For each flavor (dev, staging, prod):

1. Go to **Product** → **Scheme** → **Manage Schemes**
2. Click **+** to add a new scheme
3. Name it according to the flavor (e.g., "dev", "staging", "prod")
4. Edit the scheme:
   - **Run**: Use `Debug-[flavor]` configuration
   - **Archive**: Use `Release-[flavor]` configuration

### 4. Update Info.plist

Add these keys to `ios/Runner/Info.plist`:

```xml
<key>CFBundleDisplayName</key>
<string>$(APP_DISPLAY_NAME)</string>
<key>CFBundleIdentifier</key>
<string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
```

### 5. Configure Build Settings

For each configuration (dev, staging, prod):

1. Select **Runner** target
2. Go to **Build Settings**
3. Add User-Defined Settings:
   - `APP_DISPLAY_NAME`:
     - dev: "Resume Builder DEV"
     - staging: "Resume Builder STG"
     - prod: "Resume Builder"
   - `PRODUCT_BUNDLE_IDENTIFIER`:
     - dev: "com.yourcompany.resumebuilder.dev"
     - staging: "com.yourcompany.resumebuilder.staging"
     - prod: "com.yourcompany.resumebuilder"

## Running the App with Flavors

### Using Shell Scripts

We've provided convenient shell scripts:

```bash
# Development
./run_dev.sh

# Staging
./run_staging.sh

# Production
./run_prod.sh
```

### Using Flutter Command

```bash
# Development
flutter run --flavor dev -t lib/main_dev.dart

# Staging
flutter run --flavor staging -t lib/main_staging.dart

# Production
flutter run --flavor prod -t lib/main_prod.dart
```

### For Web (No Flavors Needed)

Web doesn't require flavor configuration. Just run:

```bash
# Development
flutter run -d chrome -t lib/main_dev.dart

# Production
flutter run -d chrome -t lib/main_prod.dart
```

## Building for Release

### Android APK

```bash
# Development APK
./build_apk_dev.sh
# Or: flutter build apk --flavor dev -t lib/main_dev.dart --release

# Production APK
./build_apk_prod.sh
# Or: flutter build apk --flavor prod -t lib/main_prod.dart --release
```

### Android App Bundle (for Play Store)

```bash
# Production
flutter build appbundle --flavor prod -t lib/main_prod.dart --release
```

### iOS

```bash
# Development
flutter build ios --flavor dev -t lib/main_dev.dart --release

# Production
flutter build ios --flavor prod -t lib/main_prod.dart --release
```

Then archive using Xcode:
1. Open `ios/Runner.xcworkspace`
2. Select the appropriate scheme (dev/staging/prod)
3. Product → Archive

## VS Code Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Dev",
      "request": "launch",
      "type": "dart",
      "program": "lib/main_dev.dart",
      "args": ["--flavor", "dev"]
    },
    {
      "name": "Staging",
      "request": "launch",
      "type": "dart",
      "program": "lib/main_staging.dart",
      "args": ["--flavor", "staging"]
    },
    {
      "name": "Production",
      "request": "launch",
      "type": "dart",
      "program": "lib/main_prod.dart",
      "args": ["--flavor", "prod"]
    }
  ]
}
```

## Understanding the Code Structure

### App Configuration (`lib/config/app_config.dart`)

```dart
class AppConfig {
  final String appName;
  final String apiBaseUrl;
  final String flavor;
  final bool enableLogging;
  final bool enableAnalytics;

  // Factory methods for each flavor
  static AppConfig development() => AppConfig(...);
  static AppConfig staging() => AppConfig(...);
  static AppConfig production() => AppConfig(...);
}
```

### Main Entry Points

- `lib/main_dev.dart` - Development entry point
- `lib/main_staging.dart` - Staging entry point
- `lib/main_prod.dart` - Production entry point

Each calls `mainCommon(flavor)` which initializes the app with the appropriate configuration.

### Usage in Code

```dart
import 'package:resume_builder_app/config/app_config.dart';

// Access current configuration
debugPrint('API URL: ${appConfig.apiBaseUrl}');
debugPrint('Flavor: ${appConfig.flavor}');

if (appConfig.isDevelopment) {
  // Development-specific code
}

if (appConfig.enableLogging) {
  // Log something
}
```

## Troubleshooting

### Issue: "No flavor configuration found"

**Solution**: Make sure you're using the `--flavor` flag and `-t` flag together:
```bash
flutter run --flavor dev -t lib/main_dev.dart
```

### Issue: Android build fails with "Duplicate class"

**Solution**: Clean and rebuild:
```bash
flutter clean
flutter pub get
flutter build apk --flavor dev -t lib/main_dev.dart
```

### Issue: iOS build fails with "Scheme not found"

**Solution**:
1. Delete `ios/Podfile.lock` and `ios/Pods/` directory
2. Run `cd ios && pod install`
3. Open Xcode and verify schemes are correctly configured

### Issue: App name doesn't change

**Android**: Verify `resValue "string", "app_name"` is set in `build.gradle`
**iOS**: Check `APP_DISPLAY_NAME` in Build Settings

### Issue: Wrong API endpoint being used

**Solution**: Verify the flavor is being initialized correctly:
```dart
void main() async {
  initAppConfig('dev'); // Make sure this matches your flavor
  // ...
}
```

## Best Practices

1. **Never commit sensitive data**: Use environment variables or secure vaults for production secrets
2. **Test all flavors**: Before release, test dev, staging, and prod builds
3. **Use appropriate icons**: Different icons help distinguish flavor builds
4. **Version naming**: Use semantic versioning with flavor suffixes (e.g., 1.0.0-dev)
5. **Automated builds**: Set up CI/CD for each flavor
6. **Feature flags**: Use flavor configuration for feature toggles

## Example CI/CD Configuration

### GitHub Actions

```yaml
name: Build APKs

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        flavor: [dev, staging, prod]

    steps:
      - uses: actions/checkout@v2
      - uses: subosito/flutter-action@v2

      - name: Install dependencies
        run: flutter pub get

      - name: Build APK
        run: flutter build apk --flavor ${{ matrix.flavor }} -t lib/main_${{ matrix.flavor }}.dart

      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: app-${{ matrix.flavor }}-release
          path: build/app/outputs/flutter-apk/
```

## Additional Resources

- [Flutter Official Documentation - Flavors](https://flutter.dev/docs/deployment/flavors)
- [Android Build Variants](https://developer.android.com/studio/build/build-variants)
- [iOS Schemes and Configurations](https://developer.apple.com/documentation/xcode/customizing-the-build-schemes-for-a-project)

---

**Need help?** Open an issue on GitHub or contact the development team.
