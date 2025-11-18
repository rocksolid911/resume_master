#!/bin/bash
# Build APK for Production flavor

echo "📦 Building APK for PRODUCTION..."
flutter build apk --flavor prod -t lib/main_prod.dart --release
