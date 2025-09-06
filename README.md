# 💰 Currency Collector

A production-grade currency collection management system built with FastAPI and vanilla JavaScript. Track your currency notes, manage valuations, and export data with a clean, responsive web interface.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎯 **Core Functionality**
- **CRUD Operations**: Add, edit, delete, and view currency notes
- **Advanced Search**: Search across all fields including numeric values
- **Data Import/Export**: CSV import/export with atomic operations
- **Real-time Filtering**: Filter by country, pick, grade, and more
- **Responsive Design**: Works on desktop, tablet, and mobile

### 🔐 **Security**
- **Session-based Authentication**: Secure web login
- **API Token Authentication**: Bearer token for programmatic access
- **Rate Limiting**: Built-in protection against abuse
- **CORS Support**: Configurable cross-origin resource sharing
- **Secure Cookies**: HttpOnly, SameSite, and HTTPS flags

### 📊 **Data Management**
- **CSV Database**: Simple, portable data storage
- **Atomic Operations**: Safe concurrent access
- **Data Validation**: Pydantic models ensure data integrity
- **Backup Support**: Easy data export and import

### 🔗 **External Integrations**
- **PMG Verification**: Direct links to PMG certificate lookup
- **eBay Search**: Quick search for similar items
- **Heritage Auctions**: Direct links to auction listings
- **n8n API**: Programmatic access for automation

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/currency-collector.git
   cd currency-collector
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp backend/env.example backend/.env
   # Edit backend/.env with your settings
   ```

4. **Run the application**
   ```bash
   python backend/main.py
   ```

5. **Access the application**
   - Open your browser to `http://localhost:8000`
   - Login with the password from your `.env` file

## 📁 Project Structure

```
currency-collector/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── sample_notes.csv     # Sample data
│   └── env.example          # Environment variables template
├── static/
│   └── index.html           # Frontend application
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── QUICK_START.md           # Quick start guide
└── PYTHONANYWHERE_DEPLOYMENT.md  # Deployment guide
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Web login password
APP_PASSWORD=your_secure_password

# API bearer token
API_TOKEN=your_secure_api_token

# CSV file path
CSV_PATH=./sample_notes.csv

# Session secret (use a long random string)
SESSION_SECRET=your_session_secret

# CORS origin
ALLOW_ORIGIN=*
```

### Security Best Practices

- Use strong, unique passwords
- Generate secure API tokens
- Use long random session secrets
- Enable HTTPS in production
- Rotate tokens regularly

## 🌐 Deployment

### PythonAnywhere

This application is optimized for PythonAnywhere deployment. See `PYTHONANYWHERE_DEPLOYMENT.md` for detailed instructions.

### Other Platforms

The application can be deployed to any platform that supports Python and FastAPI:
- Heroku
- DigitalOcean
- AWS
- Google Cloud Platform
- VPS/Dedicated servers

## 📖 API Documentation

### Authentication

- **Web UI**: Session-based authentication with cookies
- **API**: Bearer token authentication

### Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/health` | Health check | No |
| POST | `/api/login` | Web login | No |
| GET | `/api/logout` | Web logout | No |
| GET | `/api/notes` | Get all notes | Session |
| POST | `/api/notes` | Create note | Session |
| PUT | `/api/notes/{id}` | Update note | Session |
| DELETE | `/api/notes/{id}` | Delete note | Session |
| POST | `/api/import` | Import CSV | Session |
| GET | `/api/notes.csv` | Export CSV | Session |
| PATCH | `/api/notes/{id}/estimate` | Update estimate | Bearer Token |

### Example API Usage

```bash
# Get all notes (requires session)
curl -X GET "http://localhost:8000/api/notes" \
  -H "Cookie: session=your_session_cookie"

# Update estimate (requires bearer token)
curl -X PATCH "http://localhost:8000/api/notes/123/estimate" \
  -H "Authorization: Bearer your_api_token" \
  -H "Content-Type: application/json" \
  -d '{"est_value": 150.00}'
```

## 🎨 Frontend Features

### User Interface
- **Dark Theme**: Modern, easy-on-the-eyes design
- **Responsive Layout**: Works on all screen sizes
- **Real-time Search**: Instant filtering as you type
- **Sortable Columns**: Click headers to sort data
- **Modal Forms**: Clean add/edit interfaces
- **Toast Notifications**: User-friendly feedback

### Data Management
- **Bulk Import**: Upload CSV files to add multiple notes
- **Data Export**: Download your data as CSV
- **Quick Actions**: Edit, delete, and view details
- **External Links**: Direct access to PMG, eBay, Heritage

## 🔒 Security Features

- **Session Management**: Secure cookie-based sessions
- **Rate Limiting**: Prevents abuse and DoS attacks
- **Input Validation**: Pydantic models ensure data integrity
- **CORS Protection**: Configurable cross-origin policies
- **Secure Headers**: HttpOnly, SameSite, and HTTPS flags

## 🧪 Testing

The application includes comprehensive testing:

```bash
# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=backend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend uses vanilla JavaScript and CSS
- Icons from [Heroicons](https://heroicons.com/)
- Inspired by real currency collectors' needs

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/currency-collector/issues) page
2. Review the documentation
3. Create a new issue with detailed information

---

**Made with ❤️ for currency collectors worldwide**