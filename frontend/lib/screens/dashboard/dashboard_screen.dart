import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../providers/auth_provider.dart';
import '../../providers/resume_provider.dart';
import '../../config/app_theme.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authStateProvider);
    final resumesAsync = ref.watch(resumeListProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('My Resumes'),
        actions: [
          // Theme toggle
          IconButton(
            icon: Icon(
              ref.watch(themeProvider) ? Icons.light_mode : Icons.dark_mode,
            ),
            onPressed: () {
              ref.read(themeProvider.notifier).toggleTheme();
            },
          ),
          // Profile menu
          PopupMenuButton(
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'profile',
                child: Text('Profile'),
              ),
              const PopupMenuItem(
                value: 'settings',
                child: Text('Settings'),
              ),
              const PopupMenuItem(
                value: 'logout',
                child: Text('Logout'),
              ),
            ],
            onSelected: (value) {
              switch (value) {
                case 'profile':
                  // Navigate to profile
                  break;
                case 'settings':
                  context.go('/settings');
                  break;
                case 'logout':
                  ref.read(authStateProvider.notifier).logout();
                  break;
              }
            },
          ),
        ],
      ),
      body: resumesAsync.when(
        data: (resumes) {
          if (resumes.isEmpty) {
            return _buildEmptyState(context);
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: resumes.length,
            itemBuilder: (context, index) {
              final resume = resumes[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  leading: Icon(
                    Icons.description,
                    color: Theme.of(context).primaryColor,
                  ),
                  title: Text(resume.title),
                  subtitle: Text(
                    'Updated: ${_formatDate(resume.updatedAt)}',
                  ),
                  trailing: PopupMenuButton(
                    itemBuilder: (context) => [
                      const PopupMenuItem(
                        value: 'edit',
                        child: Text('Edit'),
                      ),
                      const PopupMenuItem(
                        value: 'preview',
                        child: Text('Preview'),
                      ),
                      const PopupMenuItem(
                        value: 'download',
                        child: Text('Download'),
                      ),
                      const PopupMenuItem(
                        value: 'delete',
                        child: Text('Delete'),
                      ),
                    ],
                    onSelected: (value) {
                      switch (value) {
                        case 'edit':
                          context.go('/resume/${resume.id}');
                          break;
                        case 'preview':
                          context.go('/resume/${resume.id}/preview');
                          break;
                        case 'download':
                          // Implement download
                          break;
                        case 'delete':
                          // Implement delete
                          break;
                      }
                    },
                  ),
                  onTap: () => context.go('/resume/${resume.id}'),
                ),
              );
            },
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(
          child: Text('Error: ${error.toString()}'),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          context.go('/templates');
        },
        icon: const Icon(Icons.add),
        label: const Text('New Resume'),
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.description_outlined,
            size: 100,
            color: Colors.grey[400],
          ),
          const SizedBox(height: 16),
          Text(
            'No resumes yet',
            style: Theme.of(context).textTheme.displaySmall,
          ),
          const SizedBox(height: 8),
          Text(
            'Create your first professional resume',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            onPressed: () {
              context.go('/templates');
            },
            icon: const Icon(Icons.add),
            label: const Text('Create Resume'),
          ),
        ],
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year}';
  }
}
