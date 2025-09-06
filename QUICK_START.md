# Currency Collector - Quick Start Guide

## 🚀 INSTALLATION & RUNNING

### Option 1: Automated Setup (Recommended)

**PowerShell (Recommended):**
```powershell
.\install_and_run.ps1
```

**Command Prompt:**
```cmd
install_and_run.bat
```

### Option 2: Manual Setup

1. **Install Python 3.11+**
   - Download from: https://www.python.org/downloads/
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Restart your terminal after installation

2. **Run the application:**
   ```cmd
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

## 🌐 ACCESS THE APPLICATION

Once running, open your browser and go to:
- **Main App**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Login Password**: `admin123`

## 📋 FEATURES

### ✅ What You Can Do
- **View Notes**: See all your currency notes in a beautiful table
- **Add Notes**: Click "Add Note" to create new entries
- **Edit Notes**: Click "Edit" on any note to modify it
- **Delete Notes**: Click "Delete" to remove notes (with confirmation)
- **Search & Filter**: Use the search box and dropdown filters
- **Import CSV**: Upload CSV files to bulk import notes
- **Export CSV**: Download your data as CSV
- **External Links**: Quick links to PMG, eBay, Heritage Auctions
- **Portfolio Stats**: See total value, ROI, and other KPIs

### 🔧 API Features (for n8n integration)
- **Get All Notes**: `GET /api/notes` with Bearer token
- **Update Estimates**: `PATCH /api/notes/{id}/estimate` with Bearer token
- **Export Data**: `GET /api/notes.csv` with Bearer token

## 📊 SAMPLE DATA

The app comes with 12 sample currency notes including:
- United States Morgan Silver Dollars (1921-1929)
- Canadian Silver Dollars (1935-1937)
- Various grades (63-69) and EPQ designations
- Purchase prices and estimated values
- PMG certification numbers for some notes

## 🔑 LOGIN & SECURITY

- **Web Login**: Password-based with session cookies
- **API Access**: Bearer token authentication
- **Default Password**: `admin123`
- **API Token**: `your-secret-api-token`

## 📁 DATA STORAGE

- **Format**: CSV file (`backend/notes.csv`)
- **Backup**: The CSV file is your data backup
- **Atomic Operations**: Safe read/write to prevent data corruption

## 🛠️ TROUBLESHOOTING

### Python Not Found
```
ERROR: Python is not installed or not in PATH
```
**Solution**: 
1. Install Python from https://www.python.org/downloads/
2. Make sure to check "Add Python to PATH"
3. Restart your terminal

### Dependencies Not Found
```
ERROR: Missing required dependency
```
**Solution**: Run `pip install -r backend/requirements.txt`

### Port Already in Use
```
ERROR: Address already in use
```
**Solution**: 
1. Stop any existing server (Ctrl+C)
2. Or change the port in `backend/main.py`

### Can't Access the Website
**Solution**: 
1. Make sure the server is running
2. Use http://localhost:8000 (not file://)
3. Check if Windows Firewall is blocking the connection

## 📱 BROWSER SUPPORT

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🔄 UPDATING DATA

### Adding Notes
1. Click "Add Note" button
2. Fill in required fields (Country, Pick, Grade, Purchase Price)
3. Add optional details (EPQ, PMG Cert, etc.)
4. Click "Save Note"

### Editing Notes
1. Click "Edit" button on any note
2. Modify the fields you want to change
3. Click "Save Note"

### Importing CSV
1. Click "Import CSV" button
2. Select your CSV file
3. The app will automatically import and update existing notes

### Exporting Data
1. Click "Export CSV" button
2. The file will download automatically

## 🎯 NEXT STEPS

1. **Explore the sample data** to understand the format
2. **Add your own notes** using the "Add Note" button
3. **Customize the data** by editing existing notes
4. **Use the search and filters** to find specific notes
5. **Export your data** for backup or analysis
6. **Integrate with n8n** using the API endpoints

## 📞 SUPPORT

If you encounter any issues:

1. **Check the console** for error messages
2. **Verify Python installation**: `python --version`
3. **Check dependencies**: `pip list`
4. **Restart the application** if needed
5. **Check the API docs** at http://localhost:8000/docs

## 🎉 SUCCESS INDICATORS

You'll know everything is working when:
- ✅ Server starts without errors
- ✅ Web page loads at http://localhost:8000
- ✅ You can login with password "admin123"
- ✅ You see the sample notes in the table
- ✅ You can add, edit, and delete notes
- ✅ Search and filters work
- ✅ Import/export functions work

---

**Ready to start? Run `.\install_and_run.ps1` and open http://localhost:8000!**
