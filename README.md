# Flask Student Management System - AWS EC2 Deployment Guide

A Flask-based student management application with data visualization capabilities using matplotlib and pandas.

## Prerequisites

- AWS EC2 instance running Ubuntu
- SSH access to your EC2 instance
- GitHub account with the project repository

## Deployment Steps

### Step 1: Connect to Your EC2 Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/Ankito45/Deploy-app-to-AWS-Session.git
cd Deploy-app-to-AWS-Session
```

**If git is not installed:**
```bash
sudo apt install git -y
git clone https://github.com/Ankito45/Deploy-app-to-AWS-Session.git
cd Deploy-app-to-AWS-Session
```

### Step 3: Update System and Install Dependencies

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install matplotlib system dependencies
sudo apt install python3-dev pkg-config libfreetype6-dev libpng-dev -y
```

**If you encounter "Unable to locate package" error:**
```bash
sudo apt update
sudo apt-cache search python3-pip
sudo apt install python3-pip -y
```

### Step 4: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 5: Install Python Packages

```bash
pip install -r requirements.txt
```

### Step 6: Configure AWS Security Group

1. Go to **AWS Console** → **EC2** → **Instances**
2. Select your instance
3. Click **Security** tab
4. Click on the **Security Group** link
5. Click **Edit inbound rules**
6. Click **Add rule**
7. Configure:
   - **Type:** Custom TCP
   - **Port Range:** 5000
   - **Source:** 0.0.0.0/0 (or your specific IP for security)
8. Click **Save rules**

**If you can't edit security group:**
- Check if you have proper IAM permissions
- Contact your AWS administrator

### Step 7: Run the Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the Flask app
python3 app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.31.x.x:5000
```

**Access your application:**
```
http://your-ec2-public-ip:5000
```

## Troubleshooting Guide

### Error: "Address already in use" or "Port 5000 is already in use"

**Solution:**
```bash
# Find the process using port 5000
sudo lsof -i :5000

# Kill the process (replace PID with actual process ID)
sudo kill -9 <PID>

# Or kill all Python processes on port 5000
sudo fkill -9 $(lsof -t -i:5000)

# Try running the app again
python3 app.py
```

### Error: "ModuleNotFoundError: No module named 'flask'" or similar

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt

# Verify installation
pip list | grep -i flask
```

### Error: Matplotlib or Pandas import errors

**Solution:**
```bash
# Install additional system dependencies
sudo apt install python3-tk libopenblas-dev libatlas-base-dev -y

# Reinstall matplotlib and pandas
pip uninstall matplotlib pandas -y
pip install matplotlib==3.8.2 pandas==2.1.4
```

### Error: "Permission denied" when running app

**Solution:**
```bash
# Make app.py executable
chmod +x app.py

# Or run with python3 explicitly
python3 app.py
```

## Features

- View all students with calculated grades
- Search students by roll number
- Filter students by grade
- View branch-wise statistics
- Display top performers
- Generate comprehensive reports
- Data visualization with matplotlib

## Tech Stack

- **Backend:** Flask 3.0.0
- **Data Processing:** Pandas 2.1.4
- **Visualization:** Matplotlib 3.8.2
- **Server:** Gunicorn (production)
- **Reverse Proxy:** Nginx (optional)
