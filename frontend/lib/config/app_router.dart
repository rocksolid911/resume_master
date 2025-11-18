import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/auth_provider.dart';
import 'routes.dart';

/// Provider for initial route based on authentication state
final initialRouteProvider = Provider<String>((ref) {
  final authState = ref.watch(authStateProvider);
  final isAuthenticated = authState.value?.isAuthenticated ?? false;
  return AppRoutes.getInitialRoute(isAuthenticated);
});

/// Route generator provider
final routeGeneratorProvider = Provider<RouteFactory>((ref) {
  return AppRoutes.generateRoute;
});
