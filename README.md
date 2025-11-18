# AI-Powered Resume Builder

A full-stack application for creating professional resumes with AI-powered text enhancement. Built with Django REST Framework (backend) and Flutter (frontend - web & mobile).

## 🌟 Features

### Backend (Django REST Framework)
- **User Authentication**: JWT-based authentication with secure token management
- **Resume Templates**: 10 professional templates (Modern, Classic, Creative, Executive, Tech, Academic, Startup, Minimal Dark, ATS-Friendly, Portfolio)
- **Resume Management**: Full CRUD operations for user resumes
- **AI Enhancement**: OpenAI integration for:
  - Bullet point enhancement
  - Description improvement
  - Professional summary generation
  - Grammar and style correction
  - Keyword optimization
  - Full section rewrites
- **Export Functionality**: Generate PDF and DOCX files
- **Rate Limiting**: AI usage limits based on subscription tiers
- **Public Sharing**: Share resumes via unique URLs

### Frontend (Flutter)
- **Cross-Platform**: Web and mobile (iOS/Android) support
- **State Management**: Riverpod for reactive state management
- **Responsive Design**: Optimized for mobile, tablet, and desktop
- **Dark Mode**: Built-in theme switcher
- **Multi-Step Resume Builder**: Intuitive form with live preview
- **AI Enhancement Panel**: Side-by-side comparison of original vs enhanced text
- **Template Gallery**: Browse and filter templates by category
- **Dashboard**: Manage multiple resumes with quick actions
- **Offline Support**: Local caching with Hive
- **Export Options**: PDF, DOCX, email, and QR code sharing

## 📁 Project Structure

```
resume_master/
├── backend/                    # Django REST Framework backend
│   ├── api/                    # Main API application
│   │   ├── models/             # Database models
│   │   ├── serializers/        # DRF serializers
│   │   ├── views/              # API views
│   │   ├── services/           # Business logic (AI, PDF, DOCX)
│   │   ├── utils/              # Utilities and helpers
│   │   └── management/         # Custom management commands
│   ├── resume_builder/         # Django project settings
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Docker configuration
│   └── manage.py               # Django management script
│
├── frontend/                   # Flutter application
│   ├── lib/
│   │   ├── config/             # App configuration (routes, theme, API)
│   │   ├── models/             # Data models
│   │   ├── providers/          # Riverpod state providers
│   │   ├── screens/            # UI screens
│   │   ├── widgets/            # Reusable widgets
│   │   ├── services/           # API and storage services
│   │   └── utils/              # Utilities
│   ├── pubspec.yaml            # Flutter dependencies
│   └── assets/                 # Images, icons, templates
│
├── docker-compose.yml          # Docker Compose configuration
├── DEPLOYMENT.md               # Deployment guide
└── README.md                   # This file
```

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY=your-openai-api-key
   ```

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Backend API: http://localhost:8000
   - Backend Admin: http://localhost:8000/admin
   - Database: PostgreSQL on port 5432

### Manual Setup

#### Backend Setup

1. **Navigate to backend and create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run migrations and seed data**:
   ```bash
   python manage.py migrate
   python manage.py seed_templates
   python manage.py createsuperuser  # Optional
   ```

5. **Start server**:
   ```bash
   python manage.py runserver
   ```

#### Frontend Setup

1. **Navigate to frontend**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   flutter pub get
   ```

3. **Generate code**:
   ```bash
   flutter pub run build_runner build --delete-conflicting-outputs
   ```

4. **Update API endpoint** in `lib/config/api_config.dart`

5. **Run the app**:
   ```bash
   flutter run -d chrome  # For web
   flutter run            # For mobile
   ```

## 📚 API Documentation

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET/PUT /api/auth/profile/` - User profile
- `POST /api/auth/token/refresh/` - Refresh token

### Templates
- `GET /api/templates/` - List templates
- `GET /api/templates/{id}/` - Template details

### Resumes
- `GET /api/resumes/` - List user resumes
- `POST /api/resumes/` - Create resume
- `GET/PUT/DELETE /api/resumes/{id}/` - Resume operations
- `GET /api/resumes/{id}/download/` - Download resume

### AI Enhancement
- `POST /api/ai/enhance-text/` - Enhance text
- `POST /api/ai/suggest-improvements/` - Get suggestions

## 🎨 Resume Templates

1. **Modern Minimal** - Clean, single-column design
2. **Professional Classic** - Traditional two-column layout
3. **Creative Bold** - Colorful, design-focused (Premium)
4. **Executive** - Formal template for senior roles (Premium)
5. **Tech Developer** - Code-themed for developers
6. **Academic** - Research-focused template
7. **Startup** - Modern startup-style design
8. **Minimal Dark** - Elegant dark theme (Premium)
9. **ATS-Friendly** - Optimized for applicant tracking systems
10. **Portfolio** - Showcases projects and portfolios

## 🤖 AI Enhancement Features

- **Bullet Point Enhancement**: Transform basic points into impactful achievements
- **Description Improvement**: Enhance job/project descriptions
- **Summary Generation**: Create professional summaries
- **Grammar & Style**: Fix grammar and improve writing
- **Keyword Optimization**: Add relevant keywords for ATS
- **Full Rewrite**: Complete section rewrite

### Usage Limits
- Free: 5 enhancements/day
- Premium: 50 enhancements/day
- Enterprise: Unlimited

## 🔒 Security

- JWT authentication with token refresh
- Password hashing with Django validators
- CORS configuration
- HTTPS enforcement in production
- SQL injection protection via ORM
- XSS and CSRF protection
- Rate limiting on AI endpoints

## 📱 Responsive Design

- **Mobile** (<600dp): Single column, bottom sheets
- **Tablet** (600-960dp): Two-column layouts
- **Desktop** (>960dp): Multi-column, sidebar navigation

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:
- Heroku
- AWS EC2
- DigitalOcean
- Vercel (Frontend)
- Firebase (Frontend)
- App Stores (iOS/Android)

## 🧪 Testing

**Backend**:
```bash
cd backend
python manage.py test
```

**Frontend**:
```bash
cd frontend
flutter test
```

## 📝 Tech Stack

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL
- OpenAI API
- WeasyPrint (PDF generation)
- python-docx (DOCX generation)
- JWT Authentication

### Frontend
- Flutter 3.0+
- Riverpod (State Management)
- Dio (HTTP Client)
- Hive (Local Storage)
- Go Router (Navigation)
- Google Fonts

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenAI for AI capabilities
- Django & Django REST Framework
- Flutter & Dart teams
- All open-source contributors

## 📧 Support

For support:
- Open an issue on GitHub
- Email: support@example.com

---

**Built with ❤️ for job seekers worldwide**
