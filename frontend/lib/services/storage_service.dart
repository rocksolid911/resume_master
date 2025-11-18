import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class StorageService {
  static late SharedPreferences _prefs;

  static Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  // Auth tokens
  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';
  static const String _userKey = 'user_data';
  static const String _themeKey = 'dark_theme';

  static Future<void> saveAccessToken(String token) async {
    await _prefs.setString(_accessTokenKey, token);
  }

  static String? getAccessToken() {
    return _prefs.getString(_accessTokenKey);
  }

  static Future<void> saveRefreshToken(String token) async {
    await _prefs.setString(_refreshTokenKey, token);
  }

  static String? getRefreshToken() {
    return _prefs.getString(_refreshTokenKey);
  }

  static Future<void> saveUserData(Map<String, dynamic> userData) async {
    await _prefs.setString(_userKey, json.encode(userData));
  }

  static Map<String, dynamic>? getUserData() {
    final userString = _prefs.getString(_userKey);
    if (userString != null) {
      return json.decode(userString) as Map<String, dynamic>;
    }
    return null;
  }

  static Future<void> clearAuthData() async {
    await _prefs.remove(_accessTokenKey);
    await _prefs.remove(_refreshTokenKey);
    await _prefs.remove(_userKey);
  }

  static Future<void> setDarkTheme(bool isDark) async {
    await _prefs.setBool(_themeKey, isDark);
  }

  static bool getDarkTheme() {
    return _prefs.getBool(_themeKey) ?? false;
  }

  static Future<void> clearAll() async {
    await _prefs.clear();
  }
}
