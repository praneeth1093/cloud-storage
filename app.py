
from flask import Flask, request, redirect, url_for, session, render_template
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import boto3
import os
import io

load_dotenv()

from config import Config

# -----------------------------
# Flask Configuration
# -----------------------------

app = Flask(__name__)

app.config.from_object(Config)

mysql = MySQL(app)

s3 = boto3.client(
    "s3",
    region_name="ap-south-1"
)

BUCKET_NAME = "praneeth-cloud-storage"

# -----------------------------
# Flask Configuration
# -----------------------------
app = Flask(__name__)

app.config.from_object(Config)

mysql = MySQL(app)

s3 = boto3.client(
    "s3",
<<<<<<< HEAD
    region_name=os.getenv("AWS_REGION")
=======
    region_name="ap-south-1"
>>>>>>> e560bec519b811958e36c1636dd8ec2b0eaf2deb
)

BUCKET_NAME = "praneeth-cloud-storage"

# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():
    return render_template("home.html")

# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if user:
            cursor.close()
            return "Email already registered!"

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, hashed_password)
        )

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()

        if user and check_password_hash(user[3], password):

            session["user_id"] = user[0]
            session["name"] = user[1]

            return redirect(url_for("dashboard"))

        return "Invalid Email or Password"

    return render_template("login.html")

# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT id,
               original_filename,
               uploaded_at
        FROM files
        WHERE uploaded_by=%s
        ORDER BY uploaded_at DESC
    """, (session["user_id"],))

    files = cursor.fetchall()

    cursor.close()

    return render_template(
        "dashboard.html",
        name=session["name"],
        files=files
    )

# -----------------------------
# Upload File
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():

    if "user_id" not in session:
        return redirect(url_for("login"))

    uploaded_file = request.files["file"]
    print("FILES RECEIVED:", request.files)

    if not uploaded_file or uploaded_file.filename== "":
        return "No file selected."

    try:

        uploaded_file.seek(0, os.SEEK_END)
        file_size = uploaded_file.tell()
        uploaded_file.seek(0)

        # Upload to S3
        s3.upload_fileobj(
            uploaded_file,
            BUCKET_NAME,
            uploaded_file.filename
        )

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO files
            (filename,
             original_filename,
             s3_key,
             file_size,
             file_type,
             uploaded_by)
            VALUES(%s,%s,%s,%s,%s,%s)
        """,
        (
            uploaded_file.filename,
            uploaded_file.filename,
            uploaded_file.filename,
            file_size,
            uploaded_file.content_type,
            session["user_id"]
        ))

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("dashboard"))

    except Exception as e:
        import traceback
        traceback.print_exc()
        return str(e), 500    
        return str(e)

# -----------------------------
# Download File
# -----------------------------
@app.route("/download/<int:file_id>")
def download(file_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT original_filename,
               s3_key
        FROM files
        WHERE id=%s
        AND uploaded_by=%s
    """, (file_id, session["user_id"]))

    file = cursor.fetchone()

    cursor.close()

    if not file:
        return "File not found."

    try:

        stream = io.BytesIO()

        s3.download_fileobj(
            BUCKET_NAME,
            file[1],
            stream
        )

        stream.seek(0)

        return send_file(
            stream,
            as_attachment=True,
            download_name=file[0]
        )

    except Exception as e:
        return str(e)
@app.route("/delete/<int:file_id>")
def delete(file_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT s3_key
        FROM files
        WHERE id=%s AND uploaded_by=%s
    """, (file_id, session["user_id"]))

    file = cursor.fetchone()

    if not file:
        cursor.close()
        return "File not found."

    try:

        # Delete from S3
        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=file[0]
        )

        # Delete from MySQL
        cursor.execute(
            "DELETE FROM files WHERE id=%s",
            (file_id,)
        )

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("dashboard"))

    except Exception as e:
        cursor.close()
        return str(e)
# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

# -----------------------------
# Test S3
# -----------------------------
@app.route("/test-s3")
def test_s3():

    try:
        buckets = s3.list_buckets()
        return str(buckets["Buckets"])

    except Exception as e:
        return str(e)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



