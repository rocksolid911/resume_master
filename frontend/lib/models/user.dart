import 'package:json_annotation/json_annotation.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  final int id;
  final String email;
  @JsonKey(name: 'first_name')
  final String firstName;
  @JsonKey(name: 'last_name')
  final String lastName;
  @JsonKey(name: 'full_name')
  final String? fullName;
  @JsonKey(name: 'phone_number')
  final String? phoneNumber;
  final String? location;
  @JsonKey(name: 'professional_summary')
  final String? professionalSummary;
  @JsonKey(name: 'linkedin_url')
  final String? linkedinUrl;
  @JsonKey(name: 'github_url')
  final String? githubUrl;
  @JsonKey(name: 'portfolio_url')
  final String? portfolioUrl;
  @JsonKey(name: 'subscription_tier')
  final String subscriptionTier;
  @JsonKey(name: 'ai_enhancements_used_today')
  final int aiEnhancementsUsedToday;
  @JsonKey(name: 'can_use_ai')
  final bool? canUseAi;
  @JsonKey(name: 'ai_usage_remaining')
  final int? aiUsageRemaining;

  User({
    required this.id,
    required this.email,
    required this.firstName,
    required this.lastName,
    this.fullName,
    this.phoneNumber,
    this.location,
    this.professionalSummary,
    this.linkedinUrl,
    this.githubUrl,
    this.portfolioUrl,
    this.subscriptionTier = 'free',
    this.aiEnhancementsUsedToday = 0,
    this.canUseAi,
    this.aiUsageRemaining,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);

  User copyWith({
    int? id,
    String? email,
    String? firstName,
    String? lastName,
    String? fullName,
    String? phoneNumber,
    String? location,
    String? professionalSummary,
    String? linkedinUrl,
    String? githubUrl,
    String? portfolioUrl,
    String? subscriptionTier,
    int? aiEnhancementsUsedToday,
    bool? canUseAi,
    int? aiUsageRemaining,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      fullName: fullName ?? this.fullName,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      location: location ?? this.location,
      professionalSummary: professionalSummary ?? this.professionalSummary,
      linkedinUrl: linkedinUrl ?? this.linkedinUrl,
      githubUrl: githubUrl ?? this.githubUrl,
      portfolioUrl: portfolioUrl ?? this.portfolioUrl,
      subscriptionTier: subscriptionTier ?? this.subscriptionTier,
      aiEnhancementsUsedToday: aiEnhancementsUsedToday ?? this.aiEnhancementsUsedToday,
      canUseAi: canUseAi ?? this.canUseAi,
      aiUsageRemaining: aiUsageRemaining ?? this.aiUsageRemaining,
    );
  }
}

@JsonSerializable()
class AuthTokens {
  final String access;
  final String refresh;

  AuthTokens({
    required this.access,
    required this.refresh,
  });

  factory AuthTokens.fromJson(Map<String, dynamic> json) => _$AuthTokensFromJson(json);
  Map<String, dynamic> toJson() => _$AuthTokensToJson(this);
}

@JsonSerializable()
class AuthState {
  final User? user;
  final AuthTokens? tokens;
  final bool isAuthenticated;

  AuthState({
    this.user,
    this.tokens,
    this.isAuthenticated = false,
  });

  factory AuthState.fromJson(Map<String, dynamic> json) => _$AuthStateFromJson(json);
  Map<String, dynamic> toJson() => _$AuthStateToJson(this);

  AuthState copyWith({
    User? user,
    AuthTokens? tokens,
    bool? isAuthenticated,
  }) {
    return AuthState(
      user: user ?? this.user,
      tokens: tokens ?? this.tokens,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
    );
  }

  static AuthState initial() {
    return AuthState(isAuthenticated: false);
  }
}
