import 'package:json_annotation/json_annotation.dart';

part 'resume_template.g.dart';

@JsonSerializable()
class ResumeTemplate {
  final int id;
  @JsonKey(name: 'template_id')
  final String templateId;
  final String name;
  final String description;
  final String category;
  @JsonKey(name: 'html_structure')
  final String? htmlStructure;
  @JsonKey(name: 'css_styling')
  final String? cssStyleing;
  @JsonKey(name: 'preview_image')
  final String? previewImage;
  final String? thumbnail;
  @JsonKey(name: 'is_premium')
  final bool isPremium;
  @JsonKey(name: 'supports_photo')
  final bool supportsPhoto;
  @JsonKey(name: 'supports_colors')
  final bool supportsColors;
  @JsonKey(name: 'usage_count')
  final int usageCount;
  final double rating;

  ResumeTemplate({
    required this.id,
    required this.templateId,
    required this.name,
    required this.description,
    required this.category,
    this.htmlStructure,
    this.cssStyleing,
    this.previewImage,
    this.thumbnail,
    this.isPremium = false,
    this.supportsPhoto = true,
    this.supportsColors = true,
    this.usageCount = 0,
    this.rating = 0.0,
  });

  factory ResumeTemplate.fromJson(Map<String, dynamic> json) =>
      _$ResumeTemplateFromJson(json);
  Map<String, dynamic> toJson() => _$ResumeTemplateToJson(this);

  String get categoryLabel {
    switch (category) {
      case 'modern':
        return 'Modern';
      case 'classic':
        return 'Classic';
      case 'creative':
        return 'Creative';
      case 'executive':
        return 'Executive';
      case 'tech':
        return 'Tech';
      case 'academic':
        return 'Academic';
      case 'startup':
        return 'Startup';
      case 'minimal':
        return 'Minimal';
      case 'ats_friendly':
        return 'ATS Friendly';
      case 'portfolio':
        return 'Portfolio';
      default:
        return category;
    }
  }
}
