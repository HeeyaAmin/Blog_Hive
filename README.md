
# 🐝 BlogHive — AI-Powered Blog Generator

**BlogHive** is a full-stack Flask-based web app that enables users to generate intelligent, tailored blog titles and descriptions by selecting interest-based keywords and adjectives. Built using Flask, MySQL, and OpenAI GPT models, it delivers a rich user experience with full backend customization, logging, and blog personalization.

---

## 🚀 Features

- User login/signup and session management
- Keyword selection interface with dynamic adjective dropdowns
- User can choose multiple adjectives per keyword
- AI-generated blog title + description using OpenAI GPT-3.5
- Save blogs to favorites
- Full logging of blog generation activity (who generated what, when, and using which adjectives)
- Mobile-responsive frontend (Bootstrap-based)

---

## 📦 Technologies Used

- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Backend**: Flask (Python), OpenAI API
- **Database**: MySQL (with full normalization and joins)
- **AI**: OpenAI GPT-3.5 Turbo (text generation)

---

## 🧠 Database Schema

### 🔸 Tables

| Table | Purpose |
|:--|:--|
| `user` | Stores user details (login, password) |
| `keywords` | Master list of interest categories |
| `adjectives` | A table with 20 columns (each for a keyword); each row is a different adjective set |
| `user_favorites` | Blogs saved by users |
| `blog_generation_log` | NEW: Tracks blogs generated along with selected keywords and adjectives |

---

### 🧬 `blog_generation_log` Schema

```sql
CREATE TABLE blog_generation_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  generated_title TEXT NOT NULL,
  generated_description TEXT NOT NULL,
  selected_data JSON NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);
✅ This logs:

user_id

generated_title and description

selected_data: JSON mapping like:

json
Copy
Edit
{
  "fitness": ["intense", "cardio"],
  "technology": ["automated"]
}
🗺 Entity Relationship Overview
scss
Copy
Edit
[user] ────< [user_favorites]

[user] ────< [blog_generation_log] 
                          ↳ (JSON: keyword → adjectives)

[keywords] 
      ↳ [adjectives] → stored as columns per keyword
🧪 How Blog Generation Works
User selects keywords

For each keyword, they choose one or more adjectives

These are used to create a prompt for OpenAI:

arduino
Copy
Edit
"Based on: adventure, spicy, futuristic..."
→ Title + Description
The blog and its metadata are saved in blog_generation_log for tracking

📂 Folder Structure
markdown
Copy
Edit
📁 static/
    └── styles.css, script.js

📁 templates/
    └── login.html, signup.html, index.html, favorites.html

📁 app.py
📁 .env
📁 requirements.txt
📁 README.md
⚙️ Setup Instructions
Clone the repo and set up a virtual environment

Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Configure .env file with:

ini
Copy
Edit
FLASK_SECRET_KEY=your_secret
OPENAI_API_KEY=your_api_key
DB_HOST=localhost
DB_PORT=8889
DB_USER=root
DB_PASSWORD=root
DB_NAME=bloghive
Create all tables (see SQL setup)

Run:

bash
Copy
Edit
flask run
✅ Normalization & Joins Used
All tables satisfy 3NF

user_favorites, blog_generation_log use foreign keys

Joins are used in:

Fetching adjectives (keywords → adjectives)

Filtering logs by user

Favorites by user

👩‍💻 Contributors
Heeya Mineshkumar Amin

Shail Jayesh Patel