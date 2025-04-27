from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import secrets
from dotenv import load_dotenv
import os
from openai import OpenAI
import json


# Load environment variables from .env file
load_dotenv()
# Load OpenAI API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=int(os.getenv('DB_PORT')),
    database=os.getenv('DB_NAME')
)


# ✅ Flask app initialization
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generates a secure random secret key


cursor = db.cursor(dictionary=True)

# ----------------------------
# 🛠 Helper Functions
# ----------------------------

def get_keywords():
    cursor.execute("SELECT * FROM keywords")
    return cursor.fetchall()

def get_blogs_by_keywords(selected_keywords):
    """Returns blogs matching any of the selected keywords."""
    format_strings = ','.join(['%s'] * len(selected_keywords))
    query = f"""
        SELECT DISTINCT b.blog_id, b.title, b.description, b.image_url
        FROM blog b
        JOIN blog_keywords bk ON b.blog_id = bk.blog_id
        JOIN keywords k ON bk.keyword_id = k.keyword_id
        WHERE k.keyword_name IN ({format_strings})
    """
    cursor.execute(query, selected_keywords)
    return cursor.fetchall()

# ----------------------------
# 🔐 User Authentication Routes
# ----------------------------

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ----------------------------
# 🎯 Main App Routes
# ----------------------------

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    keywords = get_keywords()
    return render_template('index.html', keywords=keywords)



@app.route('/generate_blogs', methods=['POST'])
def generate_blogs():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    selected_keywords = request.json.get('selected_keywords', [])
    if not selected_keywords:
        return jsonify({"error": "No keywords selected."})

    # Prepare prompt for OpenAI
    prompt_text = f"""
    Based on the following keywords: {', '.join(selected_keywords)},
    generate a JSON output with:
    - A creative blog title
    - A detailed, engaging blog description

    Example format:
    {{
        "title": "Sample Title",
        "description": "Sample description text..."
    }}
    """

    try:
        # Call OpenAI's Chat Completion API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.7,
            max_tokens=500
        )

        content = response.choices[0].message.content

        # Safely parse JSON from OpenAI response
        blog_data = json.loads(content)

        return jsonify(matched_blogs=[{
            "title": blog_data.get('title', 'Untitled Blog'),
            "description": blog_data.get('description', 'No description available.'),
            "image_url": "static/images/default.png"  # Default image
        }])

    except Exception as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"})


# Route to save a blog to favorites
@app.route('/save_favorite', methods=['POST'])
def save_favorite():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Not logged in"})

    data = request.json
    title = data.get('title')
    description = data.get('description')

    try:
        cursor.execute(
            "INSERT INTO user_favorites (user_id, blog_title, blog_description) VALUES (%s, %s, %s)",
            (session['user_id'], title, description)
        )
        db.commit()
        return jsonify({"status": "success", "message": "Blog saved to favorites!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# route to view favorite blogs
@app.route('/favorites')
def favorites():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    query = """
        SELECT blog_title, blog_description
        FROM user_favorites
        WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    favorites = cursor.fetchall()

    return render_template('favorites.html', favorites=favorites)




# ----------------------------
# 🚀 Main
# ----------------------------

if __name__ == '__main__':
    app.run(debug=True)
