import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/resume_template.dart';
import '../services/api_service.dart';

// Template list provider
final templateListProvider = FutureProvider<List<ResumeTemplate>>((ref) async {
  final apiService = ref.read(apiServiceProvider);
  return apiService.getTemplates();
});

// Filtered template list provider
final filteredTemplateProvider = FutureProvider.family<List<ResumeTemplate>, TemplateFilter>(
  (ref, filter) async {
    final apiService = ref.read(apiServiceProvider);
    return apiService.getTemplates(
      category: filter.category,
      premium: filter.premium,
      search: filter.search,
    );
  },
);

// Single template provider
final templateProvider = FutureProvider.family<ResumeTemplate, int>((ref, id) async {
  final apiService = ref.read(apiServiceProvider);
  return apiService.getTemplate(id);
});

class TemplateFilter {
  final String? category;
  final bool? premium;
  final String? search;

  TemplateFilter({
    this.category,
    this.premium,
    this.search,
  });
}
