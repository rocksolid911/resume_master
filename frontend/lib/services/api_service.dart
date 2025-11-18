import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config/api_config.dart';
import '../models/user.dart';
import '../models/resume.dart';
import '../models/resume_template.dart';
import 'storage_service.dart';
import 'package:logger/logger.dart';

final apiServiceProvider = Provider<ApiService>((ref) {
  return ApiService();
});

class ApiService {
  late final Dio _dio;
  final Logger _logger = Logger();

  ApiService() {
    _dio = Dio(BaseOptions(
      baseUrl: ApiConfig.baseUrl,
      connectTimeout: ApiConfig.connectTimeout,
      receiveTimeout: ApiConfig.receiveTimeout,
      sendTimeout: ApiConfig.sendTimeout,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));

    // Add interceptors
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          // Add auth token to requests
          final token = StorageService.getAccessToken();
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          _logger.d('Request: ${options.method} ${options.path}');
          return handler.next(options);
        },
        onResponse: (response, handler) {
          _logger.d('Response: ${response.statusCode} ${response.requestOptions.path}');
          return handler.next(response);
        },
        onError: (error, handler) async {
          _logger.e('Error: ${error.response?.statusCode} ${error.requestOptions.path}');

          // Handle token refresh on 401
          if (error.response?.statusCode == 401) {
            final refreshed = await _refreshToken();
            if (refreshed) {
              // Retry the request
              final options = error.requestOptions;
              options.headers['Authorization'] =
                  'Bearer ${StorageService.getAccessToken()}';
              try {
                final response = await _dio.request(
                  options.path,
                  options: Options(
                    method: options.method,
                    headers: options.headers,
                  ),
                  data: options.data,
                  queryParameters: options.queryParameters,
                );
                return handler.resolve(response);
              } catch (e) {
                return handler.next(error);
              }
            }
          }
          return handler.next(error);
        },
      ),
    );
  }

  Future<bool> _refreshToken() async {
    try {
      final refreshToken = StorageService.getRefreshToken();
      if (refreshToken == null) return false;

      final response = await _dio.post(
        ApiConfig.refreshTokenEndpoint,
        data: {'refresh': refreshToken},
      );

      if (response.statusCode == 200) {
        final newAccessToken = response.data['access'];
        await StorageService.saveAccessToken(newAccessToken);
        return true;
      }
      return false;
    } catch (e) {
      _logger.e('Token refresh failed: $e');
      return false;
    }
  }

  // Auth APIs
  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await _dio.post(
      ApiConfig.loginEndpoint,
      data: {
        'email': email,
        'password': password,
      },
    );
    return response.data['data'];
  }

  Future<Map<String, dynamic>> register({
    required String email,
    required String password,
    required String firstName,
    required String lastName,
  }) async {
    final response = await _dio.post(
      ApiConfig.registerEndpoint,
      data: {
        'email': email,
        'password': password,
        'password_confirm': password,
        'first_name': firstName,
        'last_name': lastName,
      },
    );
    return response.data['data'];
  }

  Future<User> getProfile() async {
    final response = await _dio.get(ApiConfig.profileEndpoint);
    return User.fromJson(response.data['data']);
  }

  Future<User> updateProfile(Map<String, dynamic> data) async {
    final response = await _dio.put(
      ApiConfig.profileEndpoint,
      data: data,
    );
    return User.fromJson(response.data['data']);
  }

  // Template APIs
  Future<List<ResumeTemplate>> getTemplates({
    String? category,
    bool? premium,
    String? search,
  }) async {
    final queryParams = <String, dynamic>{};
    if (category != null) queryParams['category'] = category;
    if (premium != null) queryParams['premium'] = premium;
    if (search != null) queryParams['search'] = search;

    final response = await _dio.get(
      ApiConfig.templatesEndpoint,
      queryParameters: queryParams,
    );

    final templates = (response.data['data']['templates'] as List)
        .map((json) => ResumeTemplate.fromJson(json))
        .toList();
    return templates;
  }

  Future<ResumeTemplate> getTemplate(int id) async {
    final response = await _dio.get('${ApiConfig.templatesEndpoint}$id/');
    return ResumeTemplate.fromJson(response.data['data']);
  }

  // Resume APIs
  Future<List<Resume>> getResumes() async {
    final response = await _dio.get(ApiConfig.resumesEndpoint);
    final resumes = (response.data['data']['resumes'] as List)
        .map((json) => Resume.fromJson(json))
        .toList();
    return resumes;
  }

  Future<Resume> getResume(int id) async {
    final response = await _dio.get('${ApiConfig.resumesEndpoint}$id/');
    return Resume.fromJson(response.data['data']);
  }

  Future<Resume> createResume(Map<String, dynamic> data) async {
    final response = await _dio.post(
      ApiConfig.resumesEndpoint,
      data: data,
    );
    return Resume.fromJson(response.data['data']);
  }

  Future<Resume> updateResume(int id, Map<String, dynamic> data) async {
    final response = await _dio.put(
      '${ApiConfig.resumesEndpoint}$id/',
      data: data,
    );
    return Resume.fromJson(response.data['data']);
  }

  Future<void> deleteResume(int id) async {
    await _dio.delete('${ApiConfig.resumesEndpoint}$id/');
  }

  Future<String> downloadResume(int id, {String format = 'pdf'}) async {
    final response = await _dio.get(
      '${ApiConfig.resumesEndpoint}$id/download/',
      queryParameters: {'format': format},
      options: Options(responseType: ResponseType.bytes),
    );
    // Return the file URL or save locally
    return ''; // Implement file saving logic
  }

  // AI APIs
  Future<Map<String, dynamic>> enhanceText({
    required String text,
    required String sectionType,
    String enhancementType = 'bullet_point',
    int? resumeId,
    Map<String, dynamic>? context,
  }) async {
    final response = await _dio.post(
      ApiConfig.aiEnhanceEndpoint,
      data: {
        'text': text,
        'section_type': sectionType,
        'enhancement_type': enhancementType,
        if (resumeId != null) 'resume_id': resumeId,
        if (context != null) 'context': context,
      },
    );
    return response.data['data'];
  }

  Future<Map<String, dynamic>> suggestImprovements(int resumeId) async {
    final response = await _dio.post(
      ApiConfig.aiSuggestEndpoint,
      data: {'resume_id': resumeId},
    );
    return response.data['data'];
  }
}
