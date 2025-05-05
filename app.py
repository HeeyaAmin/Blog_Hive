# app.py
# Authors: Heeya Mineshkumar Amin and Shail Jayesh Patel
import requests
import uuid
from pathlib import Path

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
# Written by Heeya Mineshkumar Amin
# Helper function to generate images
# ----------------------------------------
def generate_and_save_image(prompt_text):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url).content

        # Generate safe filename
        file_name = f"{uuid.uuid4().hex}.png"
        image_path = Path("static/images") / file_name

        # Save image to static folder
        with open(image_path, "wb") as f:
            f.write(img_data)

        return f"static/images/{file_name}"  # relative path for HTML
    except Exception as e:
        print("Image generation error:", e)
        return "static/images/default.png"

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

        # Generate image
        image_prompt = f"{blog_data['title']} - {blog_data['description'][:100]}"
        image_url = generate_and_save_image(image_prompt)

        # Save blog generation to DB
        cursor.execute(
            "INSERT INTO blog_generation_log (user_id, generated_title, generated_description, selected_data) VALUES (%s, %s, %s, %s)",
            (session['user_id'], blog_data.get('title'), blog_data.get('description'), json.dumps(keyword_adjectives))
        )
        db.commit()

        return jsonify(matched_blogs=[{
            "title": blog_data.get('title', 'Untitled Blog'),
            "description": blog_data.get('description', 'No description available.'),
            "image_url": image_url
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

# Wriiten by Shail Jayesh Patel
@app.route('/favorite_blog', methods=['POST'])
def favorite_blog():
    if 'user_id' not in session:
        return jsonify({'status': 'unauthorized'})

    data = request.json
    title = data.get('title')
    description = data.get('description')
    image_url = data.get('image_url', 'static/images/default.png')

    try:
        cursor.execute(
            "SELECT * FROM user_favorites WHERE user_id=%s AND blog_title=%s",
            (session['user_id'], title)
        )
        if cursor.fetchone():
            return jsonify({'status': 'already_favorited'})

        cursor.execute(
            "INSERT INTO user_favorites (user_id, blog_title, blog_description, image_url) VALUES (%s, %s, %s, %s)",
            (session['user_id'], title, description, image_url)
        )
        db.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


# Written by Heeya Mineshkumar Amin
@app.route('/favorites')
def favorites():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute(
        "SELECT blog_title AS title, blog_description AS description, image_url "
        "FROM user_favorites WHERE user_id = %s",
        (session['user_id'],)
    )
    favorites = cursor.fetchall()
    return render_template('favorites.html', favorites=favorites)


# Written by Shail Jayesh Patel
@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    cursor.execute(
        "DELETE FROM user_favorites WHERE user_id = %s AND blog_title = %s",
        (session['user_id'], title)
    )
    db.commit()
    return redirect(url_for('favorites'))


# ----------------------------------------
# 🚀 Main Entry Point
# ----------------------------------------

# Written by Heeya Mineshkumar Amin
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
