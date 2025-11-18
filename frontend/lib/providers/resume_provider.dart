import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/resume.dart';
import '../services/api_service.dart';

// Resume list provider
final resumeListProvider = FutureProvider<List<Resume>>((ref) async {
  final apiService = ref.read(apiServiceProvider);
  return apiService.getResumes();
});

// Single resume provider
final resumeProvider = FutureProvider.family<Resume, int>((ref, id) async {
  final apiService = ref.read(apiServiceProvider);
  return apiService.getResume(id);
});

// Resume editor state provider
final resumeEditorProvider = StateNotifierProvider<ResumeEditorNotifier, AsyncValue<Resume?>>((ref) {
  return ResumeEditorNotifier(ref.read(apiServiceProvider));
});

class ResumeEditorNotifier extends StateNotifier<AsyncValue<Resume?>> {
  final ApiService _apiService;

  ResumeEditorNotifier(this._apiService) : super(const AsyncValue.data(null));

  Future<void> loadResume(int id) async {
    state = const AsyncValue.loading();
    try {
      final resume = await _apiService.getResume(id);
      state = AsyncValue.data(resume);
    } catch (e, stackTrace) {
      state = AsyncValue.error(e, stackTrace);
    }
  }

  Future<void> createResume(Map<String, dynamic> data) async {
    state = const AsyncValue.loading();
    try {
      final resume = await _apiService.createResume(data);
      state = AsyncValue.data(resume);
    } catch (e, stackTrace) {
      state = AsyncValue.error(e, stackTrace);
    }
  }

  Future<void> updateResume(int id, Map<String, dynamic> data) async {
    try {
      final resume = await _apiService.updateResume(id, data);
      state = AsyncValue.data(resume);
    } catch (e, stackTrace) {
      state = AsyncValue.error(e, stackTrace);
    }
  }

  Future<void> deleteResume(int id) async {
    try {
      await _apiService.deleteResume(id);
      state = const AsyncValue.data(null);
    } catch (e, stackTrace) {
      state = AsyncValue.error(e, stackTrace);
    }
  }
}
