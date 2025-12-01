## Personal Blog Website (Flask)

This is a **premium, modern personal blog** built with **Flask** and **SQLite**.  
You can create, view, edit, and delete blog posts through a clean, responsive web interface.

### 1. Requirements

- **Python 3.8+** installed  
- **pip** (Python package manager)
- No virtual environment is required (as requested).

### 2. Install Dependencies (one time)

Open **PowerShell** in this project folder:

```powershell
cd "D:\Devanshu_Pote\The_Developers_Arena_Internship\Task9_(Personnal_Blog_Website)"
pip install flask flask_sqlalchemy
```

This installs all required libraries globally for your Python installation.

### 3. Project Structure

- `app.py` – main Flask application (routes, database model, configuration)
- `templates/` – HTML templates
  - `base.html` – shared layout (navbar, footer, styles)
  - `index.html` – homepage with latest posts
  - `post_detail.html` – single post page
  - `create_edit_post.html` – create/edit form
  - `admin_posts.html` – manage all posts
  - `404.html` – custom not found page
- `static/css/style.css` – custom premium styling

### 4. How to Run the Blog

From the project folder in **PowerShell**:

```powershell
cd "D:\Devanshu_Pote\The_Developers_Arena_Internship\Task9_(Personnal_Blog_Website)"
python app.py
```

You should see output similar to:

```text
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Now open your browser and go to:

- `http://127.0.0.1:5000/` – Homepage (public blog)
- `http://127.0.0.1:5000/admin/posts` – Manage posts (admin dashboard)

The **SQLite database** file `blog.db` will be created automatically on first run.

### 5. Using the Web Interface

- **Create a new post**
  - Click **“+ New Post”** in the navbar or **“Start Writing”** on the homepage.
  - Fill in **Title** and **Content**.
  - Leave **“Publish this post”** checked to make it visible on the homepage.
  - Click **“Publish Post”**.

- **View posts**
  - Go to the **Home** page (`/`) to see the latest published posts.
  - Click any post title to view the full article.

- **Edit a post**
  - Go to **Manage Posts** (`/admin/posts`).
  - Click **Edit** next to the post.
  - Update the fields and click **Save Changes**.

- **Delete a post**
  - Go to **Manage Posts** (`/admin/posts`).
  - Click **Delete** next to the post and confirm.

### 6. Customization Ideas

- Change the site name and branding text in `templates/base.html`.
- Adjust colors, fonts, and layout in `static/css/style.css` for your own visual identity.
- Add author names, categories, or tags by extending the `Post` model in `app.py`.
- Add authentication (login/logout) to protect the admin routes if you need it.

### 7. Stopping the Server

In the PowerShell window where the app is running, press:

- `Ctrl + C`

This will stop the Flask development server.


