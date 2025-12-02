# Premium Enhanced Blog Application

A **premium, feature-rich blog application** built with **Flask** and **SQLite**. This is an advanced-level blog platform with comprehensive features including user authentication, categories, tags, comments, search, analytics, RSS feeds, and REST API endpoints.

## 🚀 Features

### Core Features
- ✅ **User Authentication** - Register, login, logout with session management
- ✅ **Admin Dashboard** - Comprehensive admin panel with statistics
- ✅ **Post Management** - Create, edit, delete, publish/draft posts
- ✅ **Markdown Support** - Rich text editing with Markdown syntax
- ✅ **Categories & Tags** - Organize posts with categories and tags
- ✅ **Comments System** - User comments with approval workflow
- ✅ **Search Functionality** - Full-text search across posts
- ✅ **Post Analytics** - View counts and reading time estimation
- ✅ **Featured Posts** - Highlight important posts
- ✅ **RSS Feed** - Subscribe to blog updates
- ✅ **REST API** - JSON endpoints for posts
- ✅ **Dark Mode** - Toggle between light and dark themes
- ✅ **Responsive Design** - Mobile-friendly interface
- ✅ **Social Sharing** - Share posts on social media

### Advanced Features
- **Post Views Tracking** - Track unique views per post
- **Reading Time** - Automatic calculation based on word count
- **Related Posts** - Show related content based on categories
- **Comment Moderation** - Approve/reject comments
- **Admin Statistics** - Dashboard with key metrics
- **Post Excerpts** - Custom or auto-generated summaries
- **Category/Tag Filtering** - Browse posts by category or tag
- **Pagination** - Efficient post listing
- **SEO Friendly** - Clean URLs with slugs

## 📋 Requirements

- **Python 3.8+** installed
- **pip** (Python package manager)

## 🔧 Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies:**

```powershell
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Werkzeug 3.0.1
- Markdown 3.5.1
- Pygments 2.17.2

## 🏃 Running the Application

1. **Start the server:**

```powershell
python app.py
```

2. **Access the application:**

- Homepage: `http://127.0.0.1:5000/`
- Admin Dashboard: `http://127.0.0.1:5000/admin` (login required)
- RSS Feed: `http://127.0.0.1:5000/feed`
- API Endpoint: `http://127.0.0.1:5000/api/posts`

3. **Default Admin Credentials:**

On first run, a default admin user is created:
- **Username:** `admin`
- **Password:** `admin123`

**⚠️ IMPORTANT:** Change the default password immediately in production!

## 📁 Project Structure

```
Task10_(Enchanced_Blog_Website)/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── instance/
│   └── blog.db                # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   └── style.css          # Premium styling with dark mode
│   └── uploads/               # Image uploads directory
└── templates/
    ├── base.html              # Base template with navbar/footer
    ├── index.html             # Homepage with search & filters
    ├── post_detail.html       # Single post view with comments
    ├── login.html             # User login page
    ├── register.html          # User registration page
    ├── create_edit_post.html  # Post creation/editing form
    ├── admin_dashboard.html   # Admin statistics dashboard
    ├── admin_posts.html       # Post management interface
    ├── admin_categories.html  # Category management
    ├── admin_comments.html    # Comment moderation
    ├── category.html          # Posts by category
    ├── tag.html               # Posts by tag
    ├── 404.html               # 404 error page
    └── 500.html               # 500 error page
```

## 🎯 Usage Guide

### For Visitors

1. **Browse Posts**
   - Visit the homepage to see latest posts
   - Use the search bar to find specific content
   - Filter by categories or tags using the sidebar
   - Click on any post to read the full article

2. **Register & Comment**
   - Click "Register" to create an account
   - Login to post comments on articles
   - Comments require admin approval (except admin comments)

3. **Subscribe**
   - Click "RSS Feed" to subscribe to blog updates

### For Authors/Admins

1. **Login**
   - Use admin credentials to access the dashboard
   - Navigate to Admin section in the navbar

2. **Create Posts**
   - Click "+ New Post" or go to Admin → Create Post
   - Fill in title, content (Markdown supported), excerpt
   - Select category and add tags (comma-separated)
   - Choose to publish or save as draft
   - Mark as featured to highlight on homepage

3. **Manage Content**
   - **Posts:** View, edit, delete posts from Admin → Manage Posts
   - **Categories:** Create and manage categories
   - **Comments:** Approve or delete comments
   - **Dashboard:** View statistics and analytics

4. **Markdown Syntax**
   - Use Markdown for rich formatting
   - Headers: `# H1`, `## H2`, `### H3`
   - Bold: `**bold**`, Italic: `*italic*`
   - Links: `[text](url)`
   - Code: `` `inline code` ``
   - Code blocks: Use triple backticks
   - Lists: `- item` or `1. item`
   - See [Markdown Guide](https://www.markdownguide.org/basic-syntax/)

## 🔐 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Admin-only routes protection
- CSRF protection (via Flask forms)
- Input validation and sanitization

## 📊 Database Models

The application uses SQLite with the following models:

- **User** - User accounts with authentication
- **Post** - Blog posts with metadata
- **Category** - Post categories
- **Tag** - Post tags (many-to-many)
- **Comment** - User comments on posts
- **PostView** - Analytics for post views

## 🌐 API Endpoints

### REST API

- `GET /api/posts` - List all published posts (paginated)
- `GET /api/posts/<id>` - Get single post details

### RSS Feed

- `GET /feed` - RSS feed of latest posts

## 🎨 Customization

### Changing Site Branding

Edit `templates/base.html`:
- Update navbar brand text
- Modify footer content

### Styling

Edit `static/css/style.css`:
- Adjust colors and themes
- Modify dark mode colors
- Customize animations

### Configuration

Edit `app.py`:
- Change `SECRET_KEY` for production
- Modify database URI
- Adjust upload settings

## 🚀 Production Deployment

Before deploying to production:

1. **Change Secret Key:**
   ```python
   app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your-secret-key-here")
   ```

2. **Change Default Admin Password:**
   - Login and change password through the interface
   - Or modify the default password in `create_tables()`

3. **Use Production WSGI Server:**
   - Use Gunicorn or uWSGI instead of Flask dev server
   - Example: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`

4. **Environment Variables:**
   - Set `SECRET_KEY` as environment variable
   - Configure database URL if using external DB

5. **Security:**
   - Enable HTTPS
   - Set secure session cookies
   - Configure CORS if needed
   - Regular database backups

## 🐛 Troubleshooting

### Database Issues
- Delete `instance/blog.db` to reset database
- Run `python app.py` to recreate tables

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Port Already in Use
- Change port in `app.py`: `app.run(debug=True, port=5001)`
- Or kill the process using port 5000

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Feel free to fork, modify, and enhance this blog application!

## 📧 Support

For issues or questions, please check the code comments or create an issue in the repository.

---

**Built with ❤️ using Flask and modern web technologies**
