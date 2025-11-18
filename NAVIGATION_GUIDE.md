# Navigation Guide - Using NavigationService

This guide explains how to use the custom `NavigationService` class for navigation throughout the Resume Builder app.

## Quick Start

### Import Navigation Service

```dart
import 'package:resume_builder_app/services/navigation_service.dart';
```

### Basic Navigation

```dart
// Navigate to a route
navigationService.navigateTo(Routes.dashboard);

// Navigate with arguments
navigationService.navigateTo(
  Routes.resumeBuilder,
  arguments: RouteArguments.resumeBuilder(templateId: '123'),
);

// Go back
navigationService.goBack();

// Replace current route
navigationService.navigateToReplacement(Routes.login);

// Navigate and clear stack
navigationService.navigateToAndRemoveUntil(Routes.dashboard);
```

## Navigation Methods

### 1. `navigateTo()` - Push new route

Pushes a new route onto the navigation stack.

```dart
navigationService.navigateTo(Routes.templates);

// With arguments
navigationService.navigateTo(
  Routes.resumeEdit,
  arguments: {'resumeId': '123'},
);
```

### 2. `navigateToReplacement()` - Replace current route

Replaces the current route with a new one.

```dart
navigationService.navigateToReplacement(Routes.dashboard);
```

### 3. `navigateToAndRemoveUntil()` - Clear navigation stack

Removes all routes until a condition is met, then pushes new route.

```dart
// Remove all routes and navigate to dashboard
navigationService.navigateToAndRemoveUntil(Routes.dashboard);

// Remove routes until a specific route
navigationService.navigateToAndRemoveUntil(
  Routes.dashboard,
  predicate: (route) => route.settings.name == Routes.login,
);
```

### 4. `goBack()` - Pop current route

```dart
navigationService.goBack();

// With result
navigationService.goBack({'success': true});
```

### 5. `popUntil()` - Pop until specific route

```dart
navigationService.popUntil(Routes.dashboard);
```

### 6. `popToFirst()` - Pop to first route

```dart
navigationService.popToFirst();
```

## Dialogs and Bottom Sheets

### Show Dialog

```dart
await navigationService.showDialogBox(
  child: AlertDialog(
    title: Text('Confirm'),
    content: Text('Are you sure?'),
    actions: [
      TextButton(
        onPressed: () => navigationService.goBack(false),
        child: Text('Cancel'),
      ),
      ElevatedButton(
        onPressed: () => navigationService.goBack(true),
        child: Text('Confirm'),
      ),
    ],
  ),
);
```

### Show Bottom Sheet

```dart
await navigationService.showBottomSheet(
  child: Container(
    padding: EdgeInsets.all(20),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text('Choose an option'),
        ListTile(
          title: Text('Option 1'),
          onTap: () => navigationService.goBack('option1'),
        ),
        ListTile(
          title: Text('Option 2'),
          onTap: () => navigationService.goBack('option2'),
        ),
      ],
    ),
  ),
);
```

## Snackbars

### Show Snackbar

```dart
navigationService.showSnackBar(message: 'Profile updated successfully');
```

### Show Error

```dart
navigationService.showError('Failed to save resume');
```

### Show Success

```dart
navigationService.showSuccess('Resume created successfully');
```

### Show Info

```dart
navigationService.showInfo('Please fill all required fields');
```

## Route Arguments Helper

Use `RouteArguments` class for type-safe arguments:

```dart
// Resume builder with template
navigationService.navigateTo(
  Routes.resumeBuilder,
  arguments: RouteArguments.resumeBuilder(templateId: '123'),
);

// Resume edit
navigationService.navigateTo(
  Routes.resumeEdit,
  arguments: RouteArguments.resumeEdit(resumeId: '456'),
);

// Resume preview
navigationService.navigateTo(
  Routes.resumePreview,
  arguments: RouteArguments.resumePreview(resumeId: '789'),
);
```

## Example: Login Flow

```dart
class LoginScreen extends StatelessWidget {
  Future<void> _handleLogin() async {
    try {
      // Perform login
      await authService.login(email, password);

      // Navigate to dashboard and clear login stack
      navigationService.navigateToAndRemoveUntil(Routes.dashboard);

      // Show success message
      navigationService.showSuccess('Welcome back!');
    } catch (e) {
      // Show error
      navigationService.showError('Login failed: ${e.toString()}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: /* login form */,
    );
  }
}
```

## Example: Resume Creation Flow

```dart
class TemplateSelectionScreen extends StatelessWidget {
  void _onTemplateSelected(String templateId) {
    // Navigate to resume builder with selected template
    navigationService.navigateTo(
      Routes.resumeBuilder,
      arguments: RouteArguments.resumeBuilder(templateId: templateId),
    );
  }

  @override
  Widget build(BuildContext context) {
    return /* template grid */;
  }
}

class ResumeBuilderScreen extends StatelessWidget {
  Future<void> _saveAndPreview() async {
    try {
      // Save resume
      final resume = await resumeService.save(resumeData);

      // Navigate to preview
      navigationService.navigateTo(
        Routes.resumePreview,
        arguments: RouteArguments.resumePreview(resumeId: resume.id),
      );

      navigationService.showSuccess('Resume saved!');
    } catch (e) {
      navigationService.showError('Failed to save: ${e.toString()}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return /* builder form */;
  }
}
```

## Example: Confirmation Dialog

```dart
Future<bool> _showDeleteConfirmation() async {
  final result = await navigationService.showDialogBox<bool>(
    child: AlertDialog(
      title: Text('Delete Resume'),
      content: Text('Are you sure you want to delete this resume? This action cannot be undone.'),
      actions: [
        TextButton(
          onPressed: () => navigationService.goBack(false),
          child: Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: () => navigationService.goBack(true),
          style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
          child: Text('Delete'),
        ),
      ],
    ),
  );

  return result ?? false;
}

Future<void> _deleteResume(String resumeId) async {
  final confirmed = await _showDeleteConfirmation();

  if (confirmed) {
    try {
      await resumeService.delete(resumeId);
      navigationService.goBack(); // Go back to dashboard
      navigationService.showSuccess('Resume deleted');
    } catch (e) {
      navigationService.showError('Delete failed: ${e.toString()}');
    }
  }
}
```

## Example: Settings Screen

```dart
class SettingsScreen extends StatelessWidget {
  void _showLogoutConfirmation() async {
    final confirmed = await navigationService.showDialogBox<bool>(
      child: AlertDialog(
        title: Text('Logout'),
        content: Text('Are you sure you want to logout?'),
        actions: [
          TextButton(
            onPressed: () => navigationService.goBack(false),
            child: Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => navigationService.goBack(true),
            child: Text('Logout'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      await authService.logout();
      navigationService.navigateToAndRemoveUntil(Routes.login);
    }
  }

  @override
  Widget build(BuildContext context) {
    return /* settings UI */;
  }
}
```

## Checking Navigation State

```dart
// Check if can go back
if (navigationService.canGoBack) {
  navigationService.goBack();
} else {
  // Show exit confirmation or go to home
}
```

## Available Routes

```dart
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
```

## Best Practices

1. **Always use NavigationService**: Don't use `Navigator.of(context)` directly
2. **Use Route constants**: Always use `Routes.routeName` instead of string literals
3. **Type-safe arguments**: Use `RouteArguments` helper methods
4. **Handle errors**: Wrap navigation in try-catch blocks
5. **Provide feedback**: Use snackbars to inform users of actions
6. **Clear unnecessary routes**: Use `navigateToAndRemoveUntil` after login/logout

## Migration from go_router

If you're migrating from go_router, here's the equivalent:

| go_router | NavigationService |
|-----------|-------------------|
| `context.go('/route')` | `navigationService.navigateTo(Routes.route)` |
| `context.push('/route')` | `navigationService.navigateTo(Routes.route)` |
| `context.pop()` | `navigationService.goBack()` |
| `context.goNamed('route')` | `navigationService.navigateTo(Routes.route)` |
| `context.replace('/route')` | `navigationService.navigateToReplacement(Routes.route)` |

## Troubleshooting

### Issue: Navigation doesn't work

**Solution**: Make sure `navigatorKey` is set in MaterialApp:

```dart
MaterialApp(
  navigatorKey: navigationService.navigatorKey,
  // ...
)
```

### Issue: Context is null

**Solution**: Navigation service might be called before MaterialApp is built. Ensure MaterialApp is initialized.

### Issue: Routes not found

**Solution**: Check that the route is defined in `AppRoutes.generateRoute()` in `lib/config/routes.dart`.

---

For more information, check the source code in:
- `lib/services/navigation_service.dart`
- `lib/config/routes.dart`
- `lib/config/app_router.dart`
