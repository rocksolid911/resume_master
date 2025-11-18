import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ResumeBuilderScreen extends ConsumerStatefulWidget {
  final String? resumeId;
  final String? templateId;

  const ResumeBuilderScreen({
    super.key,
    this.resumeId,
    this.templateId,
  });

  @override
  ConsumerState<ResumeBuilderScreen> createState() => _ResumeBuilderScreenState();
}

class _ResumeBuilderScreenState extends ConsumerState<ResumeBuilderScreen> {
  int _currentStep = 0;

  final List<String> _steps = [
    'Personal Info',
    'Experience',
    'Education',
    'Skills',
    'Projects',
    'Review',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Build Your Resume'),
        actions: [
          IconButton(
            icon: const Icon(Icons.preview),
            onPressed: () {
              // Show preview
            },
          ),
          IconButton(
            icon: const Icon(Icons.save),
            onPressed: () {
              // Save draft
            },
          ),
        ],
      ),
      body: Row(
        children: [
          // Sidebar with steps
          NavigationRail(
            selectedIndex: _currentStep,
            onDestinationSelected: (index) {
              setState(() {
                _currentStep = index;
              });
            },
            labelType: NavigationRailLabelType.all,
            destinations: _steps
                .map((step) => NavigationRailDestination(
                      icon: const Icon(Icons.circle_outlined),
                      selectedIcon: const Icon(Icons.check_circle),
                      label: Text(step),
                    ))
                .toList(),
          ),
          const VerticalDivider(thickness: 1, width: 1),
          // Main content area
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: _buildStepContent(),
            ),
          ),
        ],
      ),
      bottomNavigationBar: BottomAppBar(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              if (_currentStep > 0)
                TextButton.icon(
                  onPressed: () {
                    setState(() {
                      _currentStep--;
                    });
                  },
                  icon: const Icon(Icons.arrow_back),
                  label: const Text('Previous'),
                ),
              const Spacer(),
              if (_currentStep < _steps.length - 1)
                ElevatedButton.icon(
                  onPressed: () {
                    setState(() {
                      _currentStep++;
                    });
                  },
                  icon: const Icon(Icons.arrow_forward),
                  label: const Text('Next'),
                )
              else
                ElevatedButton.icon(
                  onPressed: () {
                    // Submit resume
                  },
                  icon: const Icon(Icons.check),
                  label: const Text('Finish'),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStepContent() {
    switch (_currentStep) {
      case 0:
        return _buildPersonalInfoForm();
      case 1:
        return _buildExperienceForm();
      case 2:
        return _buildEducationForm();
      case 3:
        return _buildSkillsForm();
      case 4:
        return _buildProjectsForm();
      case 5:
        return _buildReviewStep();
      default:
        return const SizedBox();
    }
  }

  Widget _buildPersonalInfoForm() {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Personal Information',
            style: Theme.of(context).textTheme.displaySmall,
          ),
          const SizedBox(height: 24),
          const TextField(
            decoration: InputDecoration(labelText: 'First Name'),
          ),
          const SizedBox(height: 16),
          const TextField(
            decoration: InputDecoration(labelText: 'Last Name'),
          ),
          const SizedBox(height: 16),
          const TextField(
            decoration: InputDecoration(labelText: 'Email'),
          ),
          const SizedBox(height: 16),
          const TextField(
            decoration: InputDecoration(labelText: 'Phone'),
          ),
          const SizedBox(height: 16),
          const TextField(
            decoration: InputDecoration(labelText: 'Location'),
          ),
          const SizedBox(height: 16),
          const TextField(
            decoration: InputDecoration(
              labelText: 'Professional Summary',
              alignLabelWithHint: true,
            ),
            maxLines: 4,
          ),
        ],
      ),
    );
  }

  Widget _buildExperienceForm() {
    return const Center(
      child: Text('Work Experience Form - To be implemented'),
    );
  }

  Widget _buildEducationForm() {
    return const Center(
      child: Text('Education Form - To be implemented'),
    );
  }

  Widget _buildSkillsForm() {
    return const Center(
      child: Text('Skills Form - To be implemented'),
    );
  }

  Widget _buildProjectsForm() {
    return const Center(
      child: Text('Projects Form - To be implemented'),
    );
  }

  Widget _buildReviewStep() {
    return const Center(
      child: Text('Review & Preview - To be implemented'),
    );
  }
}
