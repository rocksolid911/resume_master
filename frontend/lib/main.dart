import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'config/app_config.dart';
import 'config/app_router.dart';
import 'config/app_theme.dart';
import 'config/routes.dart';
import 'providers/auth_provider.dart';
import 'services/storage_service.dart';
import 'services/navigation_service.dart';

/// Main entry point for different flavors
void mainCommon(String flavor) async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize app configuration based on flavor
  initAppConfig(flavor);

  // Initialize Hive for local storage
  await Hive.initFlutter();

  // Initialize storage service
  await StorageService.init();

  runApp(
    const ProviderScope(
      child: ResumeBuilderApp(),
    ),
  );
}

class ResumeBuilderApp extends ConsumerWidget {
  const ResumeBuilderApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final initialRoute = ref.watch(initialRouteProvider);
    final isDarkMode = ref.watch(themeProvider);
    final routeGenerator = ref.watch(routeGeneratorProvider);

    return MaterialApp(
      title: appConfig.appName,
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: isDarkMode ? ThemeMode.dark : ThemeMode.light,
      initialRoute: initialRoute,
      onGenerateRoute: routeGenerator,
      navigatorKey: navigationService.navigatorKey,
      // Configure page transitions
      builder: (context, child) {
        return child ?? const SizedBox();
      },
    );
  }
}

/// Development flavor entry point
void main() => mainCommon('dev');
