import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/user.dart';
import '../services/api_service.dart';
import '../services/storage_service.dart';

// Theme provider
final themeProvider = StateNotifierProvider<ThemeNotifier, bool>((ref) {
  return ThemeNotifier();
});

class ThemeNotifier extends StateNotifier<bool> {
  ThemeNotifier() : super(StorageService.getDarkTheme());

  void toggleTheme() {
    state = !state;
    StorageService.setDarkTheme(state);
  }
}

// Auth state provider
final authStateProvider = StateNotifierProvider<AuthNotifier, AsyncValue<AuthState>>((ref) {
  return AuthNotifier(ref.read(apiServiceProvider));
});

class AuthNotifier extends StateNotifier<AsyncValue<AuthState>> {
  final ApiService _apiService;

  AuthNotifier(this._apiService) : super(const AsyncValue.loading()) {
    _initializeAuth();
  }

  Future<void> _initializeAuth() async {
    try {
      final token = StorageService.getAccessToken();
      final userData = StorageService.getUserData();

      if (token != null && userData != null) {
        // Validate token by fetching profile
        try {
          final user = await _apiService.getProfile();
          state = AsyncValue.data(
            AuthState(
              user: user,
              tokens: AuthTokens(
                access: token,
                refresh: StorageService.getRefreshToken() ?? '',
              ),
              isAuthenticated: true,
            ),
          );
        } catch (e) {
          // Token is invalid
          await _clearAuth();
          state = AsyncValue.data(AuthState.initial());
        }
      } else {
        state = AsyncValue.data(AuthState.initial());
      }
    } catch (e) {
      state = AsyncValue.error(e, StackTrace.current);
    }
  }

  Future<void> login(String email, String password) async {
    state = const AsyncValue.loading();
    try {
      final data = await _apiService.login(email, password);

      final user = User.fromJson(data['user']);
      final tokens = AuthTokens.fromJson(data['tokens']);

      await StorageService.saveAccessToken(tokens.access);
      await StorageService.saveRefreshToken(tokens.refresh);
      await StorageService.saveUserData(user.toJson());

      state = AsyncValue.data(
        AuthState(
          user: user,
          tokens: tokens,
          isAuthenticated: true,
        ),
      );
    } catch (e, stackTrace) {
      state = AsyncValue.error(e, stackTrace);
    }
  }

  Future<void> register({
    required String email,
    required String password,
    required String firstName,
    required String lastName,
  }) async {
    state = const AsyncValue.loading();
    try {
      final data = await _apiService.register(
        email: email,
        password: password,
        firstName: firstName,
        lastName: lastName,
      );

      final user = User.fromJson(data['user']);
      final tokens = AuthTokens.fromJson(data['tokens']);

      await StorageService.saveAccessToken(tokens.access);
      await StorageService.saveRefreshToken(tokens.refresh);
      await StorageService.saveUserData(user.toJson());

      state = AsyncValue.data(
        AuthState(
          user: user,
          tokens: tokens,
          isAuthenticated: true,
        ),
      );
    } catch (e, stackTrace) {
      state = AsyncValue.error(e, stackTrace);
    }
  }

  Future<void> logout() async {
    await _clearAuth();
    state = AsyncValue.data(AuthState.initial());
  }

  Future<void> updateProfile(Map<String, dynamic> data) async {
    try {
      final user = await _apiService.updateProfile(data);
      await StorageService.saveUserData(user.toJson());

      state.whenData((authState) {
        state = AsyncValue.data(authState.copyWith(user: user));
      });
    } catch (e) {
      // Handle error
    }
  }

  Future<void> _clearAuth() async {
    await StorageService.clearAuthData();
  }
}
