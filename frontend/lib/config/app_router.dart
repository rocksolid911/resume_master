import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../screens/auth/login_screen.dart';
import '../screens/auth/register_screen.dart';
import '../screens/dashboard/dashboard_screen.dart';
import '../screens/templates/template_selection_screen.dart';
import '../screens/resume/resume_builder_screen.dart';
import '../screens/resume/resume_preview_screen.dart';
import '../screens/settings/settings_screen.dart';
import '../providers/auth_provider.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authStateProvider);

  return GoRouter(
    initialLocation: '/login',
    redirect: (context, state) {
      final isAuthenticated = authState.value?.isAuthenticated ?? false;
      final isAuthRoute = state.matchedLocation.startsWith('/login') ||
          state.matchedLocation.startsWith('/register');

      if (!isAuthenticated && !isAuthRoute) {
        return '/login';
      }

      if (isAuthenticated && isAuthRoute) {
        return '/dashboard';
      }

      return null;
    },
    routes: [
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        name: 'register',
        builder: (context, state) => const RegisterScreen(),
      ),
      GoRoute(
        path: '/dashboard',
        name: 'dashboard',
        builder: (context, state) => const DashboardScreen(),
      ),
      GoRoute(
        path: '/templates',
        name: 'templates',
        builder: (context, state) => const TemplateSelectionScreen(),
      ),
      GoRoute(
        path: '/resume/new',
        name: 'new-resume',
        builder: (context, state) {
          final templateId = state.uri.queryParameters['template'];
          return ResumeBuilderScreen(templateId: templateId);
        },
      ),
      GoRoute(
        path: '/resume/:id',
        name: 'edit-resume',
        builder: (context, state) {
          final resumeId = state.pathParameters['id']!;
          return ResumeBuilderScreen(resumeId: resumeId);
        },
      ),
      GoRoute(
        path: '/resume/:id/preview',
        name: 'preview-resume',
        builder: (context, state) {
          final resumeId = state.pathParameters['id']!;
          return ResumePreviewScreen(resumeId: resumeId);
        },
      ),
      GoRoute(
        path: '/settings',
        name: 'settings',
        builder: (context, state) => const SettingsScreen(),
      ),
    ],
  );
});
