# 🐝 BlogHive

**BlogHive** is a web application where users can select their interests and instantly generate blog templates — complete with titles, descriptions, and images — all powered by a fully normalized **MySQL database** and a **Flask backend**.

---

## 📋 Features

- User Registration & Login
- Interest (Keyword) Selection
- Blog Template Matching based on Interests
- View Matched Blogs Dynamically
- Clean Frontend with Bootstrap 5
- Backend Queries use JOINs and Conditions
- Database Normalized (1NF, 2NF, 3NF)
- Secure Session Management
- Easy to Extend with Favorites (optional)

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Database:** MySQL
- **Environment Management:** Python-dotenv

---

## 📁 Project Structure

BlogHive/ │ ├── app.py # Main Flask server ├── templates/ # HTML Pages │ ├── login.html │ ├── signup.html │ ├── index.html ├── static/ # Static files │ ├── script.js │ ├── styles.css │ └── images/ │ ├── travel2025.png │ ├── fitnessboost.png │ └── (more images) ├── .env # Environment Variables (secret keys, database config) ├── requirements.txt # Python dependencies └── README.md # Project documentation

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/BlogHive.git
cd BlogHive
2. Set up a Virtual Environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the project root:

dotenv
Copy
Edit
FLASK_SECRET_KEY=your-very-secret-random-string
DB_HOST=localhost
DB_PORT=8889
DB_USER=root
DB_PASSWORD=root
DB_NAME=bloghive
5. Set Up the Database
Use the provided bloghive_schema.sql file

Execute it in MySQL Workbench

It will create all tables (user, keywords, blog, blog_keywords, user_favorites) and insert sample data.

6. Run the Application
bash
Copy
Edit
python app.py
Visit:

arduino
Copy
Edit
http://localhost:5000/
✅ BlogHive will be live!

📚 Database Design (Normalization)
Normalization:

1NF: Each table has atomic values (no repeating groups).

2NF: All non-key attributes fully depend on primary key.

3NF: No transitive dependencies.

Relations:

blog ⬌ keywords via blog_keywords (many-to-many)

user ⬌ user_favorites ⬌ blog

JOINs and Conditional Queries Used:

Blog fetching by selected keywords uses JOINs and WHERE IN conditions.



Login Page	Keyword Selection	Blog Display
✨ Future Improvements 
Add user profile pages

Allow users to favorite blogs

Save customized blogs

Deploy live on Render / Vercel

🧑‍💻 Author
Heeya Amin
Data Science and Software Developer

🛡️ License
This project is licensed under the MIT License.