#!/bin/bash
# Build APK for Development flavor

echo "📦 Building APK for DEVELOPMENT..."
flutter build apk --flavor dev -t lib/main_dev.dart --release
