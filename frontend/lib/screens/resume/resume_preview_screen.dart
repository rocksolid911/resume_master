import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ResumePreviewScreen extends ConsumerWidget {
  final String resumeId;

  const ResumePreviewScreen({
    super.key,
    required this.resumeId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Resume Preview'),
        actions: [
          IconButton(
            icon: const Icon(Icons.download),
            onPressed: () {
              // Download PDF
            },
          ),
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {
              // Share resume
            },
          ),
        ],
      ),
      body: Center(
        child: Container(
          constraints: const BoxConstraints(maxWidth: 800),
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(40),
              child: Column(
                children: [
                  Text(
                    'Resume Preview',
                    style: Theme.of(context).textTheme.displayMedium,
                  ),
                  const SizedBox(height: 24),
                  const Expanded(
                    child: Center(
                      child: Text('Resume content will be rendered here'),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
