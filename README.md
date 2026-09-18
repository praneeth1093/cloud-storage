# ☁️ Cloud File Storage Web Application

A cloud-based file storage web application built using **Python Flask, MySQL, and AWS S3**. The application allows users to register, log in, upload files, view their uploaded files, download files, and delete files.

## 🚀 Project Overview

The main goal of this project is to build a simple cloud storage system where the **actual files are stored in Amazon S3**, while **user information and file metadata are stored in MySQL**.

This project helped me understand how a web application can integrate with cloud storage services and manage data between an application, database, and cloud infrastructure.

## 🛠️ Technologies Used

* **Python** – Backend programming
* **Flask** – Web application framework
* **MySQL** – Database for users and file metadata
* **AWS S3** – Cloud storage for uploaded files
* **Boto3** – Python SDK used to communicate with AWS S3
* **HTML/CSS** – Frontend
* **Git & GitHub** – Version control
* **Environment Variables** – Configuration and sensitive credentials

## ✨ Features

* 👤 User Registration
* 🔐 User Login & Logout
* 🔑 Password Hashing
* 📤 File Upload
* ☁️ Cloud Storage using AWS S3
* 📋 View Uploaded Files
* 📥 Download Files
* 🗑️ Delete Files
* 👥 Basic User File Ownership Checks

## 🏗️ Architecture

```text
                 ┌──────────────────┐
                 │      User        │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   Flask Web App  │
                 │     (Python)     │
                 └───────┬────┬─────┘
                         │    │
              ┌──────────┘    └──────────┐
              ▼                          ▼
      ┌───────────────┐          ┌───────────────┐
      │    MySQL      │          │    AWS S3     │
      │               │          │               │
      │ Users         │          │ Actual Files  │
      │ File Metadata │          │               │
      └───────────────┘          └───────────────┘
```

## 🔄 How the Application Works

### 1. User Registration

The user provides their name, email, and password.

The password is hashed before being stored in MySQL.

### 2. User Login

The application verifies the user's email and password and creates a session for the logged-in user.

### 3. File Upload

When a user uploads a file:

User
  ↓
Flask Application
  ↓
AWS S3 → Stores the actual file
  ↓
MySQL → Stores file metadata


### 4. File Download

When a user downloads a file:

User
  ↓
Flask Application
  ↓
MySQL → Finds file information
  ↓
AWS S3 → Retrieves actual file
  ↓
User

### 5. File Delete

When a user deletes a file, the application removes the file from AWS S3 and removes its metadata from MySQL.

## 🗄️ Database

MySQL is used to store:

* User information
* File name
* Original file name
* File size
* File type
* S3 key
* User who uploaded the file
* Upload time

## ☁️ Why AWS S3?

AWS S3 is used to store the actual uploaded files instead of storing them directly on the application server.

This separates:

**MySQL → Information about the files**

**AWS S3 → Actual files**

This approach also allows the application to use cloud object storage for user-uploaded files.

## 🔐 Security

The project includes basic security features such as:

* Password hashing using Werkzeug
* Session-based authentication
* User ownership checks for files
* Database credentials stored using environment variables
* Flask secret key stored using environment variables

## 📁 Project Structure


cloud-storage/
│
├── .github/
│   └── workflows/
│
├── static/
│
├── templates/
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
└── sample.txt
```

## ⚙️ Installation & Setup

### 1. Clone the repository

git clone https://github.com/praneeth1093/cloud-storage.git
cd cloud-storage
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and configure your database, Flask secret key, and AWS region.

```text
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=your_database
SECRET_KEY=your_secret_key
AWS_REGION=your_aws_region
```

### 5. Configure AWS S3

Create an S3 bucket in your AWS account and configure AWS credentials using your AWS environment/configuration.

### 6. Run the application

```bash
python app.py
```

The application will run on:

```text
http://localhost:5000
```

## 🎯 Challenges Faced

During the development of this project, I worked on:

1. Integrating Flask with AWS S3 using Boto3.
2. Handling file uploads and downloads between the application and S3.
3. Managing file metadata separately from the actual files.
4. Connecting Flask with MySQL.
5. Implementing user authentication and password hashing.
6. Ensuring users can access their own uploaded files.

## 📚 What I Learned

Through this project, I gained practical experience in:

* Python Flask development
* AWS S3 cloud storage
* Boto3
* MySQL database integration
* User authentication
* File upload/download handling
* Cloud application architecture
* Git and GitHub

## 🔮 Future Improvements

Possible improvements for the project include:

* File size and file type validation
* Better error handling
* AWS IAM-based access control
* S3 encryption configuration
* Presigned URLs for file downloads
* Dockerizing the application
* CI/CD deployment using GitHub Actions
* Deploying the application to AWS

## 👨‍💻 Author

**Praneeth Vakamullu**

GitHub:
https://github.com/praneeth1093

