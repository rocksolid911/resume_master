import 'package:json_annotation/json_annotation.dart';

part 'resume.g.dart';

@JsonSerializable()
class Resume {
  final int id;
  final String title;
  final int? template;
  @JsonKey(name: 'resume_data_json')
  final Map<String, dynamic> resumeDataJson;
  @JsonKey(name: 'custom_colors')
  final Map<String, dynamic>? customColors;
  @JsonKey(name: 'custom_fonts')
  final Map<String, dynamic>? customFonts;
  @JsonKey(name: 'is_active')
  final bool isActive;
  @JsonKey(name: 'is_public')
  final bool isPublic;
  @JsonKey(name: 'public_slug')
  final String? publicSlug;
  @JsonKey(name: 'pdf_file')
  final String? pdfFile;
  @JsonKey(name: 'docx_file')
  final String? docxFile;
  @JsonKey(name: 'view_count')
  final int viewCount;
  @JsonKey(name: 'download_count')
  final int downloadCount;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
  @JsonKey(name: 'updated_at')
  final DateTime updatedAt;

  Resume({
    required this.id,
    required this.title,
    this.template,
    required this.resumeDataJson,
    this.customColors,
    this.customFonts,
    this.isActive = true,
    this.isPublic = false,
    this.publicSlug,
    this.pdfFile,
    this.docxFile,
    this.viewCount = 0,
    this.downloadCount = 0,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Resume.fromJson(Map<String, dynamic> json) => _$ResumeFromJson(json);
  Map<String, dynamic> toJson() => _$ResumeToJson(this);

  Resume copyWith({
    int? id,
    String? title,
    int? template,
    Map<String, dynamic>? resumeDataJson,
    Map<String, dynamic>? customColors,
    Map<String, dynamic>? customFonts,
    bool? isActive,
    bool? isPublic,
    String? publicSlug,
    String? pdfFile,
    String? docxFile,
    int? viewCount,
    int? downloadCount,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Resume(
      id: id ?? this.id,
      title: title ?? this.title,
      template: template ?? this.template,
      resumeDataJson: resumeDataJson ?? this.resumeDataJson,
      customColors: customColors ?? this.customColors,
      customFonts: customFonts ?? this.customFonts,
      isActive: isActive ?? this.isActive,
      isPublic: isPublic ?? this.isPublic,
      publicSlug: publicSlug ?? this.publicSlug,
      pdfFile: pdfFile ?? this.pdfFile,
      docxFile: docxFile ?? this.docxFile,
      viewCount: viewCount ?? this.viewCount,
      downloadCount: downloadCount ?? this.downloadCount,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}

@JsonSerializable()
class ResumeData {
  @JsonKey(name: 'personal_info')
  final PersonalInfo personalInfo;
  @JsonKey(name: 'work_experience')
  final List<WorkExperience> workExperience;
  final List<Education> education;
  final List<Skill> skills;
  final List<Project> projects;
  final List<Certification>? certifications;
  final List<Language>? languages;

  ResumeData({
    required this.personalInfo,
    this.workExperience = const [],
    this.education = const [],
    this.skills = const [],
    this.projects = const [],
    this.certifications,
    this.languages,
  });

  factory ResumeData.fromJson(Map<String, dynamic> json) =>
      _$ResumeDataFromJson(json);
  Map<String, dynamic> toJson() => _$ResumeDataToJson(this);
}

@JsonSerializable()
class PersonalInfo {
  @JsonKey(name: 'first_name')
  final String firstName;
  @JsonKey(name: 'last_name')
  final String lastName;
  final String email;
  final String? phone;
  final String? location;
  @JsonKey(name: 'professional_summary')
  final String? professionalSummary;
  final String? linkedin;
  final String? github;
  final String? portfolio;

  PersonalInfo({
    required this.firstName,
    required this.lastName,
    required this.email,
    this.phone,
    this.location,
    this.professionalSummary,
    this.linkedin,
    this.github,
    this.portfolio,
  });

  factory PersonalInfo.fromJson(Map<String, dynamic> json) =>
      _$PersonalInfoFromJson(json);
  Map<String, dynamic> toJson() => _$PersonalInfoToJson(this);
}

@JsonSerializable()
class WorkExperience {
  final String position;
  final String company;
  @JsonKey(name: 'start_date')
  final String startDate;
  @JsonKey(name: 'end_date')
  final String? endDate;
  final String? location;
  final String? description;
  @JsonKey(name: 'bullet_points')
  final List<String>? bulletPoints;

  WorkExperience({
    required this.position,
    required this.company,
    required this.startDate,
    this.endDate,
    this.location,
    this.description,
    this.bulletPoints,
  });

  factory WorkExperience.fromJson(Map<String, dynamic> json) =>
      _$WorkExperienceFromJson(json);
  Map<String, dynamic> toJson() => _$WorkExperienceToJson(this);
}

@JsonSerializable()
class Education {
  final String degree;
  final String school;
  @JsonKey(name: 'graduation_date')
  final String? graduationDate;
  final String? gpa;
  final String? location;

  Education({
    required this.degree,
    required this.school,
    this.graduationDate,
    this.gpa,
    this.location,
  });

  factory Education.fromJson(Map<String, dynamic> json) =>
      _$EducationFromJson(json);
  Map<String, dynamic> toJson() => _$EducationToJson(this);
}

@JsonSerializable()
class Skill {
  final String name;
  final String? category;
  final String? proficiency;

  Skill({
    required this.name,
    this.category,
    this.proficiency,
  });

  factory Skill.fromJson(Map<String, dynamic> json) => _$SkillFromJson(json);
  Map<String, dynamic> toJson() => _$SkillToJson(this);
}

@JsonSerializable()
class Project {
  final String name;
  final String? description;
  final List<String>? technologies;
  final String? link;

  Project({
    required this.name,
    this.description,
    this.technologies,
    this.link,
  });

  factory Project.fromJson(Map<String, dynamic> json) =>
      _$ProjectFromJson(json);
  Map<String, dynamic> toJson() => _$ProjectToJson(this);
}

@JsonSerializable()
class Certification {
  final String name;
  final String? issuer;
  final String? date;

  Certification({
    required this.name,
    this.issuer,
    this.date,
  });

  factory Certification.fromJson(Map<String, dynamic> json) =>
      _$CertificationFromJson(json);
  Map<String, dynamic> toJson() => _$CertificationToJson(this);
}

@JsonSerializable()
class Language {
  final String name;
  final String? proficiency;

  Language({
    required this.name,
    this.proficiency,
  });

  factory Language.fromJson(Map<String, dynamic> json) =>
      _$LanguageFromJson(json);
  Map<String, dynamic> toJson() => _$LanguageToJson(this);
}
