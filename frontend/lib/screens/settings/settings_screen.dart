import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/auth_provider.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDarkMode = ref.watch(themeProvider);
    final authState = ref.watch(authStateProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: ListView(
        children: [
          ListTile(
            title: const Text('Appearance'),
            subtitle: const Text('Dark Mode'),
            trailing: Switch(
              value: isDarkMode,
              onChanged: (value) {
                ref.read(themeProvider.notifier).toggleTheme();
              },
            ),
          ),
          const Divider(),
          authState.whenData((state) {
            if (state.user != null) {
              return ListTile(
                title: const Text('Account'),
                subtitle: Text(state.user!.email),
              );
            }
            return const SizedBox();
          }).value ?? const SizedBox(),
          const Divider(),
          ListTile(
            title: const Text('About'),
            subtitle: const Text('AI Resume Builder v1.0.0'),
            onTap: () {
              // Show about dialog
            },
          ),
        ],
      ),
    );
  }
}
