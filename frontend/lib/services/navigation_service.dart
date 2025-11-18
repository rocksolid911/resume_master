import 'package:flutter/material.dart';

/// Service for handling navigation throughout the app
/// This is a singleton class that provides a common interface for navigation
class NavigationService {
  // Singleton instance
  static final NavigationService _instance = NavigationService._internal();
  factory NavigationService() => _instance;
  NavigationService._internal();

  // Global navigator key
  final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

  /// Get the current navigator state
  NavigatorState? get _navigator => navigatorKey.currentState;

  /// Get the current context
  BuildContext? get context => navigatorKey.currentContext;

  /// Navigate to a new screen
  Future<T?>? navigateTo<T>(String routeName, {Object? arguments}) {
    return _navigator?.pushNamed<T>(routeName, arguments: arguments);
  }

  /// Navigate to a new screen and remove all previous routes
  Future<T?>? navigateToAndRemoveUntil<T>(
    String routeName, {
    Object? arguments,
    bool Function(Route<dynamic>)? predicate,
  }) {
    return _navigator?.pushNamedAndRemoveUntil<T>(
      routeName,
      predicate ?? (route) => false,
      arguments: arguments,
    );
  }

  /// Replace current route with a new route
  Future<T?>? navigateToReplacement<T, TO>(
    String routeName, {
    TO? result,
    Object? arguments,
  }) {
    return _navigator?.pushReplacementNamed<T, TO>(
      routeName,
      result: result,
      arguments: arguments,
    );
  }

  /// Pop the current route
  void goBack<T>([T? result]) {
    if (_navigator?.canPop() ?? false) {
      _navigator?.pop<T>(result);
    }
  }

  /// Pop until a specific route
  void popUntil(String routeName) {
    _navigator?.popUntil((route) => route.settings.name == routeName);
  }

  /// Pop until the first route
  void popToFirst() {
    _navigator?.popUntil((route) => route.isFirst);
  }

  /// Check if can go back
  bool get canGoBack => _navigator?.canPop() ?? false;

  /// Show dialog
  Future<T?> showDialogBox<T>({
    required Widget child,
    bool barrierDismissible = true,
  }) async {
    return showDialog<T>(
      context: context!,
      barrierDismissible: barrierDismissible,
      builder: (context) => child,
    );
  }

  /// Show bottom sheet
  Future<T?> showBottomSheet<T>({
    required Widget child,
    bool isDismissible = true,
    bool enableDrag = true,
  }) async {
    return showModalBottomSheet<T>(
      context: context!,
      isDismissible: isDismissible,
      enableDrag: enableDrag,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => child,
    );
  }

  /// Show snackbar
  void showSnackBar({
    required String message,
    Duration duration = const Duration(seconds: 3),
    SnackBarAction? action,
    Color? backgroundColor,
  }) {
    final messenger = ScaffoldMessenger.of(context!);
    messenger.clearSnackBars();
    messenger.showSnackBar(
      SnackBar(
        content: Text(message),
        duration: duration,
        action: action,
        backgroundColor: backgroundColor,
      ),
    );
  }

  /// Show error snackbar
  void showError(String message) {
    showSnackBar(
      message: message,
      backgroundColor: Colors.red,
      duration: const Duration(seconds: 5),
    );
  }

  /// Show success snackbar
  void showSuccess(String message) {
    showSnackBar(
      message: message,
      backgroundColor: Colors.green,
    );
  }

  /// Show info snackbar
  void showInfo(String message) {
    showSnackBar(
      message: message,
      backgroundColor: Colors.blue,
    );
  }
}

/// Global navigation service instance
final navigationService = NavigationService();
