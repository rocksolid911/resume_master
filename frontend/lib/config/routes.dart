import 'package:flutter/material.dart';
import '../screens/auth/login_screen.dart';
import '../screens/auth/register_screen.dart';
import '../screens/dashboard/dashboard_screen.dart';
import '../screens/templates/template_selection_screen.dart';
import '../screens/resume/resume_builder_screen.dart';
import '../screens/resume/resume_preview_screen.dart';
import '../screens/settings/settings_screen.dart';

/// Application route names
class Routes {
  static const String splash = '/';
  static const String login = '/login';
  static const String register = '/register';
  static const String dashboard = '/dashboard';
  static const String templates = '/templates';
  static const String resumeBuilder = '/resume/builder';
  static const String resumeEdit = '/resume/edit';
  static const String resumePreview = '/resume/preview';
  static const String settings = '/settings';
}

/// Application routes configuration
class AppRoutes {
  /// Generate route based on settings
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case Routes.login:
        return MaterialPageRoute(
          builder: (_) => const LoginScreen(),
          settings: settings,
        );

      case Routes.register:
        return MaterialPageRoute(
          builder: (_) => const RegisterScreen(),
          settings: settings,
        );

      case Routes.dashboard:
        return MaterialPageRoute(
          builder: (_) => const DashboardScreen(),
          settings: settings,
        );

      case Routes.templates:
        return MaterialPageRoute(
          builder: (_) => const TemplateSelectionScreen(),
          settings: settings,
        );

      case Routes.resumeBuilder:
        final args = settings.arguments as Map<String, dynamic>?;
        return MaterialPageRoute(
          builder: (_) => ResumeBuilderScreen(
            templateId: args?['templateId'],
          ),
          settings: settings,
        );

      case Routes.resumeEdit:
        final args = settings.arguments as Map<String, dynamic>?;
        return MaterialPageRoute(
          builder: (_) => ResumeBuilderScreen(
            resumeId: args?['resumeId'],
          ),
          settings: settings,
        );

      case Routes.resumePreview:
        final args = settings.arguments as Map<String, dynamic>?;
        final resumeId = args?['resumeId'] as String?;
        if (resumeId == null) {
          return _errorRoute('Resume ID is required');
        }
        return MaterialPageRoute(
          builder: (_) => ResumePreviewScreen(resumeId: resumeId),
          settings: settings,
        );

      case Routes.settings:
        return MaterialPageRoute(
          builder: (_) => const SettingsScreen(),
          settings: settings,
        );

      default:
        return _errorRoute('Route not found: ${settings.name}');
    }
  }

  /// Error route for undefined routes
  static Route<dynamic> _errorRoute(String message) {
    return MaterialPageRoute(
      builder: (_) => Scaffold(
        appBar: AppBar(title: const Text('Error')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 80, color: Colors.red),
              const SizedBox(height: 16),
              Text(
                message,
                style: const TextStyle(fontSize: 18),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// Initial route based on authentication state
  static String getInitialRoute(bool isAuthenticated) {
    return isAuthenticated ? Routes.dashboard : Routes.login;
  }
}

/// Route arguments helper class
class RouteArguments {
  /// Arguments for resume builder
  static Map<String, dynamic> resumeBuilder({String? templateId}) {
    return {'templateId': templateId};
  }

  /// Arguments for resume edit
  static Map<String, dynamic> resumeEdit({required String resumeId}) {
    return {'resumeId': resumeId};
  }

  /// Arguments for resume preview
  static Map<String, dynamic> resumePreview({required String resumeId}) {
    return {'resumeId': resumeId};
  }
}
