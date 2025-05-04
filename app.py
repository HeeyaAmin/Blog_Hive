# app.py
# Authors: Heeya Mineshkumar Amin and Shail Jayesh Patel

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import secrets
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# ----------------------------------------
# Written by Heeya Mineshkumar Amin
# Load environment variables and initialize Flask app
# ----------------------------------------
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))

# ----------------------------------------
# Written by Heeya Mineshkumar Amin
# Database connection
# ----------------------------------------
db = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', 'root'),
    port=int(os.getenv('DB_PORT', 8889)),
    database=os.getenv('DB_NAME', 'bloghive')
)
cursor = db.cursor(dictionary=True)

# ----------------------------------------
# Written by Heeya Mineshkumar Amin
# OpenAI client setup
# ----------------------------------------
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# ----------------------------------------
# Written by Heeya Mineshkumar Amin
# Helper function to fetch keywords
# ----------------------------------------
def get_keywords():
    cursor.execute("SELECT * FROM keywords")
    return cursor.fetchall()

# ----------------------------------------
# Written by Shail Jayesh Patel
# Helper function to fetch random adjectives
# ----------------------------------------
def fetch_random_adjectives(selected_keywords):
    """Fetch a random row and pick adjectives for selected keywords."""
    query = "SELECT * FROM adjectives ORDER BY RAND() LIMIT 1"
    cursor.execute(query)
    random_row = cursor.fetchone()

    selected_adjectives = []
    for keyword in selected_keywords:
        if keyword in random_row and random_row[keyword]:
            selected_adjectives.append(random_row[keyword])

    return selected_adjectives

# ----------------------------------------
# 🔐 User Authentication Routes
# ----------------------------------------

# Written by Heeya Mineshkumar Amin
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        try:
            cursor.execute(
                "INSERT INTO user (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, password)
            )
            db.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('signup.html')

# Written by Heeya Mineshkumar Amin
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM user WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['user_id']
            session['user_name'] = user['first_name']
            return redirect(url_for('index'))
        else:
            return "Invalid email or password!"

    return render_template('login.html')

# Written by Heeya Mineshkumar Amin
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ----------------------------------------
# 🎯 Main Application Routes
# ----------------------------------------

# Written by Heeya Mineshkumar Amin
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    keywords = get_keywords()
    return render_template('index.html', keywords=keywords)

# Written by Shail Jayesh Patel
@app.route('/generate_blogs', methods=['POST'])
def generate_blogs():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    data = request.json
    keyword_adjectives = data.get('keyword_adjectives', {})

    if not keyword_adjectives:
        return jsonify({"error": "No adjectives selected."})

    # Flatten all selected adjectives into one list
    selected_adjectives = []
    for adjective_list in keyword_adjectives.values():
        selected_adjectives.extend(adjective_list)

    prompt_text = f"""
    Based on the following concepts: {', '.join(selected_adjectives)},
    generate a JSON output with:
    - A creative blog title
    - A detailed, engaging blog description

    Format:
    {{
        "title": "Generated Title",
        "description": "Generated Description..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.7,
            max_tokens=500
        )

        content = response.choices[0].message.content
        blog_data = json.loads(content)

        # Save blog generation to DB
        cursor.execute(
            "INSERT INTO blog_generation_log (user_id, generated_title, generated_description, selected_data) VALUES (%s, %s, %s, %s)",
            (session['user_id'], blog_data.get('title'), blog_data.get('description'), json.dumps(keyword_adjectives))
        )
        db.commit()

        return jsonify(matched_blogs=[{
            "title": blog_data.get('title', 'Untitled Blog'),
            "description": blog_data.get('description', 'No description available.'),
            "image_url": "static/images/default.png"
        }])

    except Exception as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"})


# Written by Heeya Mineshkumar Amin
@app.route('/get_adjectives/<keyword>')
def get_adjectives(keyword):
    query = f"SELECT DISTINCT `{keyword}` AS adjective FROM adjectives WHERE `{keyword}` IS NOT NULL"
    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify([row['adjective'] for row in results if row['adjective']])


# ----------------------------------------
# 🚀 Main Entry Point
# ----------------------------------------

# Written by Heeya Mineshkumar Amin
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
