class ApiConfig {
  // Base URL - Change this to your backend URL
  static const String baseUrl = 'http://localhost:8000';

  // API Endpoints
  static const String apiPrefix = '/api';

  // Auth endpoints
  static const String loginEndpoint = '$apiPrefix/auth/login/';
  static const String registerEndpoint = '$apiPrefix/auth/register/';
  static const String profileEndpoint = '$apiPrefix/auth/profile/';
  static const String refreshTokenEndpoint = '$apiPrefix/auth/token/refresh/';

  // Template endpoints
  static const String templatesEndpoint = '$apiPrefix/templates/';

  // Resume endpoints
  static const String resumesEndpoint = '$apiPrefix/resumes/';

  // AI endpoints
  static const String aiEnhanceEndpoint = '$apiPrefix/ai/enhance-text/';
  static const String aiSuggestEndpoint = '$apiPrefix/ai/suggest-improvements/';

  // Timeout durations
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  static const Duration sendTimeout = Duration(seconds: 30);
}
