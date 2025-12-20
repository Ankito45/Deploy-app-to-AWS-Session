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

**If you get permission denied error:**
```bash
chmod 400 your-key.pem
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

**Note:** Your terminal prompt should change to show `(venv)` at the beginning.

**If venv module not found:**
```bash
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Python Packages

```bash
pip install -r requirements.txt
```

**If pip install fails:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Try installing packages individually
pip install Flask==3.0.0
pip install Werkzeug==3.0.1
pip install matplotlib==3.8.2
pip install pandas==2.1.4
```

**If matplotlib installation fails:**
```bash
# Install additional dependencies
sudo apt install python3-tk libopenblas-dev -y
pip install matplotlib==3.8.2
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

### Error: "Templates folder not found" or "TemplateNotFound"

**Solution:**
```bash
# Check if templates directory exists
ls -la templates/

# If missing, create it
mkdir -p templates

# Make sure index.html exists in templates folder
ls templates/index.html

# If missing, you need to create or pull it from GitHub
git pull origin master
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

### Error: Cannot connect to application from browser

**Step 1: Check if app is running**
```bash
# Test locally on EC2
curl http://localhost:5000

# If this works, the app is running fine
```

**Step 2: Check Security Group**
```bash
# Verify port 5000 is open in AWS Security Group
# Go to AWS Console → EC2 → Security Groups
# Make sure inbound rule for port 5000 exists
```

**Step 3: Check if firewall is blocking**
```bash
# Check UFW status
sudo ufw status

# If active and blocking, allow port 5000
sudo ufw allow 5000
```

**Step 4: Verify EC2 public IP**
```bash
# Get your public IP
curl http://checkip.amazonaws.com

# Use this IP in browser: http://PUBLIC_IP:5000
```

### Error: "git: command not found"

**Solution:**
```bash
sudo apt update
sudo apt install git -y
```

### Error: Virtual environment activation not working

**Solution:**
```bash
# If using bash
source venv/bin/activate

# If using a different shell
. venv/bin/activate

# Verify activation - should show (venv) in prompt
which python
# Should show: /home/ubuntu/Deploy-app-to-AWS-Session/venv/bin/python
```

### Error: "pip: command not found" after activating venv

**Solution:**
```bash
# Deactivate and recreate venv
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Error: Application stops when SSH session closes

**Solution (Using Screen):**
```bash
# Install screen
sudo apt install screen -y

# Start a screen session
screen -S flaskapp

# Run your app
source venv/bin/activate
python3 app.py

# Detach from screen: Press Ctrl+A, then D
# App continues running in background

# To reattach later
screen -r flaskapp

# To list all screen sessions
screen -ls
```

### Error: Memory or resource issues

**Solution:**
```bash
# Check available memory
free -h

# Check disk space
df -h

# If low on memory, consider upgrading EC2 instance type
# or use Gunicorn with fewer workers
```

### General Debugging Commands

```bash
# Check Python version
python3 --version

# Check pip version
pip --version

# List installed packages
pip list

# Check if process is running
ps aux | grep python

# Check system logs
sudo journalctl -xe

# Check available ports
sudo netstat -tulpn | grep LISTEN
```

### Production Deployment

**Using Gunicorn with Systemd:**

Install Gunicorn:
```bash
pip install gunicorn
```

Create service file:
```bash
sudo nano /etc/systemd/system/flaskapp.service
```

Add the following configuration:
```ini
[Unit]
Description=Flask Student Management App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Deploy-app-to-AWS-Session
Environment="PATH=/home/ubuntu/Deploy-app-to-AWS-Session/venv/bin"
ExecStart=/home/ubuntu/Deploy-app-to-AWS-Session/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
sudo systemctl status flaskapp
```

### Optional: Nginx Setup

Install Nginx:
```bash
sudo apt install nginx -y
```

Create Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/flaskapp
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-ec2-public-ip;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

## Useful Commands

```bash
# Check service status
sudo systemctl status flaskapp

# View logs
sudo journalctl -u flaskapp -f

# Restart service
sudo systemctl restart flaskapp

# Update application
git pull
sudo systemctl restart flaskapp
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

## Troubleshooting

**Matplotlib errors:**
```bash
sudo apt install python3-tk libopenblas-dev -y
```

**Port already in use:**
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
