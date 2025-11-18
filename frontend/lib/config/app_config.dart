import 'package:flutter/foundation.dart';

/// Application configuration for different flavors
class AppConfig {
  final String appName;
  final String apiBaseUrl;
  final String flavor;
  final bool enableLogging;
  final bool enableAnalytics;

  AppConfig({
    required this.appName,
    required this.apiBaseUrl,
    required this.flavor,
    this.enableLogging = false,
    this.enableAnalytics = false,
  });

  /// Development configuration
  static AppConfig development() {
    return AppConfig(
      appName: 'Resume Builder DEV',
      apiBaseUrl: 'http://localhost:8000',
      flavor: 'dev',
      enableLogging: true,
      enableAnalytics: false,
    );
  }

  /// Staging configuration
  static AppConfig staging() {
    return AppConfig(
      appName: 'Resume Builder STAGING',
      apiBaseUrl: 'https://staging-api.yourdomain.com',
      flavor: 'staging',
      enableLogging: true,
      enableAnalytics: true,
    );
  }

  /// Production configuration
  static AppConfig production() {
    return AppConfig(
      appName: 'Resume Builder',
      apiBaseUrl: 'https://api.yourdomain.com',
      flavor: 'prod',
      enableLogging: false,
      enableAnalytics: true,
    );
  }

  /// Check if running in development mode
  bool get isDevelopment => flavor == 'dev';

  /// Check if running in staging mode
  bool get isStaging => flavor == 'staging';

  /// Check if running in production mode
  bool get isProduction => flavor == 'prod';

  @override
  String toString() {
    return 'AppConfig{appName: $appName, apiBaseUrl: $apiBaseUrl, flavor: $flavor}';
  }
}

/// Global app configuration instance
late AppConfig appConfig;

/// Initialize app configuration based on flavor
void initAppConfig(String flavor) {
  switch (flavor.toLowerCase()) {
    case 'dev':
    case 'development':
      appConfig = AppConfig.development();
      break;
    case 'staging':
    case 'stg':
      appConfig = AppConfig.staging();
      break;
    case 'prod':
    case 'production':
      appConfig = AppConfig.production();
      break;
    default:
      if (kDebugMode) {
        appConfig = AppConfig.development();
      } else {
        appConfig = AppConfig.production();
      }
  }

  if (appConfig.enableLogging) {
    debugPrint('🚀 App initialized with config: $appConfig');
  }
}
