# Fitness Slot Booking Automation

An automated booking system for TU Delft X fitness slots with both a web-based React interface and a native Python GUI.

## Features

- Two user interface options:
  - Modern React web application
  - Native Python Tkinter GUI
- Calendar for date selection
- Customizable time slot selection with priority ordering
- Automatic retry mechanism with adjustable interval
- Visual feedback on booking status
- Secure credential management through environment variables

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- TU Delft account credentials
- Node.js and npm (for React web app only)
- Conda environment (recommended for managing dependencies)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd fitness-booking
```

2. Create and activate a conda environment (recommended):
```bash
conda create -n xscript python=3.8
conda activate xscript
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your TU Delft credentials:
```
TU_USERNAME=your_username
TU_PASSWORD=your_password
```

5. For the React web app, install JavaScript dependencies:
```bash
cd x-script-web
npm install
```

## Usage

### Quick Start with Run Scripts

We provide convenient run scripts that automatically activate the conda environment and start the application:

#### For Windows:
```
.\run.bat
```

#### For Unix-based systems (Linux/macOS):
```
./run.sh
```

By default, these scripts activate the "xscript" conda environment. If you used a different name for your environment, you can specify it as a parameter:

```
.\run.bat your-env-name
```
or
```
./run.sh your-env-name
```

### Option 1: Python Tkinter GUI

1. Run the application:
```bash
python main.py
```

2. Using the GUI:
   - Select a date using the calendar
   - Check the time slots you want to book
   - Arrange the priority order using the ↑↓ arrows
   - Set your preferred retry interval (default: 300 seconds)
   - Click "Book Selected Slots" to start the booking process
   - Use "Stop Retrying" to cancel the automatic retry process

### Option 2: React Web Application

1. Start the Next.js development server:
```bash
cd x-script-web
npm run dev
```
   Or use the run scripts to activate the conda environment and start the application:
```bash
# Windows
.\run.bat

# Unix-based systems
./run.sh
```

2. Open your browser and navigate to `http://localhost:3000`

3. Using the web interface:
   - Select a date using the calendar
   - Check the time slots you want to book
   - Drag and drop to arrange priority order
   - Set your preferred retry interval
   - Click "Book Selected Slots" to start the booking process
   - Use "Stop Retrying" to cancel the automatic retry process

## How It Works

- The booking system will try slots in the order you prioritized them
- If a slot is unavailable, it will automatically try the next preferred time
- The retry interval can be adjusted through either UI
- The React app communicates with the Python script via API endpoints
- The browser automation runs headless (invisible) to reduce resource usage

## Security

- Credentials are stored locally in the `.env` file
- The `.env` file is excluded from version control
- Never share your credentials or the `.env` file

## Troubleshooting

If you encounter issues:
1. Ensure Chrome browser is installed and up to date
2. Verify your internet connection
3. Check that your TU Delft credentials are correct in the `.env` file
4. Make sure all dependencies are properly installed
5. For the React app, ensure the API endpoints are correctly configured

## Dependencies

### Python
- python-dotenv: Environment variable management
- selenium: Web automation
- webdriver-manager: Chrome driver management
- numpy: Numerical operations
- tkcalendar: Calendar widget for GUI

### JavaScript (React App)
- Next.js: React framework
- React: UI library
- React Calendar: Date picker component
- React Beautiful DnD: Drag and drop functionality
- Tailwind CSS: Styling
