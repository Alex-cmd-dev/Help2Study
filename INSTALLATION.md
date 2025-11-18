# Quick Installation Guide

The fastest way to get set up using package managers.

---

## What You Need

1. **Python 3.8+**
2. **Node.js 16+** (npm comes with it automatically)
3. **Git**

---

## macOS - Use Homebrew

### 1. Install Homebrew (if you don't have it)

Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Everything

```bash
# Install Python, Node.js, and Git all at once
brew install python3 node git
```

That's it! Homebrew installs Python, Node.js (with npm), and Git in one command.

### 3. Verify

```bash
python3 --version
node --version
npm --version
git --version
```

---

## Windows - Use Winget

Winget comes pre-installed on Windows 10/11!

### 1. Open PowerShell or Command Prompt

Search for "PowerShell" in the Start menu and run as Administrator.

### 2. Install Everything

```powershell
# Install Python
winget install Python.Python.3.12

# Install Node.js (includes npm)
winget install OpenJS.NodeJS.LTS

# Install Git
winget install Git.Git
```

### 3. Restart your terminal and verify

Close PowerShell and open a new one, then:

```powershell
python --version
node --version
npm --version
git --version
```

**Note:** If `python` doesn't work, try `python3` or `py`.

---

## Download and Setup the Project

### macOS:

```bash
# Go to your Documents folder
cd ~/Documents

# Download the project
git clone https://github.com/Alex-cmd-dev/Help2Study.git

# Go into the project
cd Help2Study

# Run automated setup
./setup.sh
```

### Windows:

```powershell
# Go to your Documents folder
cd Documents

# Download the project
git clone https://github.com/Alex-cmd-dev/Help2Study.git

# Go into the project
cd Help2Study

# Run automated setup
./setup.bat
```

**Important for Windows users:** If the setup script stops after showing the npm version, you need to enable PowerShell script execution. Open PowerShell **as Administrator** and run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then run `setup.bat` again. This is a one-time setup that allows npm to work properly.

---

## Get Your Gemini API Key

1. Go to https://aistudio.google.com
2. Sign in with your Google account
3. Click on "Get API Key" in the dashboard
4. Click "Create API Key"
5. Create a new project (or select an existing project if you have one)
6. Select the project you want to use for this application
7. Click "Generate API Key"
8. Copy the generated API key
9. When the setup script asks, paste it in the `.env` file as: `GEMINI_API_KEY=your_key_here`

---

## Start the App

```bash
make dev
```

**Windows without Make:**
```powershell
# Terminal 1:
cd backend
python manage.py runserver

# Terminal 2:
cd frontend
npm run dev
```

**macOS without Make:**
```bash
# Terminal 1:
cd backend
python3 manage.py runserver

# Terminal 2 (Cmd+T for new tab):
cd frontend
npm run dev
```

Open http://localhost:5173 in your browser!

---

## Troubleshooting

### Winget not found (Windows)

Update Windows to the latest version. Winget comes with Windows 10 (version 1809+) and Windows 11.

### Homebrew installation fails (macOS)

Make sure Command Line Tools are installed:
```bash
xcode-select --install
```

### "Command not found" after installation

Close and reopen your terminal, then try again.

---

## Why Package Managers?

- **Fast:** One command installs everything
- **Easy:** No clicking through installers
- **Updates:** Easy to update (`brew upgrade` or `winget upgrade`)
- **Clean:** Easy to uninstall (`brew uninstall` or `winget uninstall`)

That's it! See the main [README.md](README.md) for more details about the project.
