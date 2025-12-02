"""
Premium Enhanced Blog Application with Advanced Features
Built with Flask and SQLite
"""

import os
import re
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    session,
    jsonify,
    make_response,
    send_from_directory,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, or_
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-to-a-random-secret-key-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "webp"}

# Ensure upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)


# ==================== DATABASE MODELS ====================

class User(db.Model):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    posts = db.relationship("Post", backref="author", lazy="dynamic", cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="author", lazy="dynamic", cascade="all, delete-orphan")
    
    def set_password(self, password: str) -> None:
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Category(db.Model):
    """Category model for organizing posts"""
    __tablename__ = "categories"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship("Post", backref="category", lazy="dynamic")
    
    def __repr__(self) -> str:
        return f"<Category {self.name}>"


class Tag(db.Model):
    """Tag model for post tagging"""
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(60), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with Post
    posts = db.relationship("Post", secondary="post_tags", backref="tags", lazy="dynamic")
    
    def __repr__(self) -> str:
        return f"<Tag {self.name}>"


# Association table for Post-Tag many-to-many relationship
post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Post(db.Model):
    """Enhanced Post model"""
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)  # Short summary for previews
    featured_image = db.Column(db.String(255))  # Path to featured image
    is_published = db.Column(db.Boolean, default=False, index=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    views_count = db.Column(db.Integer, default=0, index=True)
    reading_time = db.Column(db.Integer)  # Estimated reading time in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)  # When post was published
    
    # Foreign keys
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    
    # Relationships
    comments = db.relationship("Comment", backref="post", lazy="dynamic", cascade="all, delete-orphan", order_by="desc(Comment.created_at)")
    post_views = db.relationship("PostView", backref="post", lazy="dynamic", cascade="all, delete-orphan")
    
    def calculate_reading_time(self) -> int:
        """Calculate estimated reading time (average 200 words per minute)"""
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))
    
    def increment_views(self) -> None:
        """Increment view count"""
        self.views_count += 1
        db.session.commit()
    
    def __repr__(self) -> str:
        return f"<Post {self.title!r}>"


class Comment(db.Model):
    """Comment model for post comments"""
    __tablename__ = "comments"
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"))  # For nested comments
    
    # Relationships
    replies = db.relationship("Comment", backref=db.backref("parent", remote_side=[id]), lazy="dynamic")
    
    def __repr__(self) -> str:
        return f"<Comment {self.id}>"


class PostView(db.Model):
    """Track post views for analytics"""
    __tablename__ = "post_views"
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Foreign key
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    
    def __repr__(self) -> str:
        return f"<PostView {self.id}>"


# ==================== UTILITY FUNCTIONS ====================

def slugify(text: str) -> str:
    """Create a URL-friendly slug from text"""
    slug = text.strip().lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug.strip("-")


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def markdown_to_html(content: str) -> str:
    """Convert Markdown content to HTML"""
    extensions = [
        CodeHiliteExtension(css_class="highlight"),
        FencedCodeExtension(),
        TableExtension(),
    ]
    return markdown(content, extensions=extensions)


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login", next=request.url))
        user = User.query.get(session["user_id"])
        if not user or not user.is_admin:
            flash("Admin access required.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROUTES ====================

@app.route("/")
@app.route("/page/<int:page>")
def index(page: int = 1):
    """Homepage with paginated posts"""
    per_page = 6
    search_query = request.args.get("q", "").strip()
    category_slug = request.args.get("category")
    tag_slug = request.args.get("tag")
    
    query = Post.query.filter_by(is_published=True)
    
    # Search functionality
    if search_query:
        query = query.filter(
            or_(
                Post.title.contains(search_query),
                Post.content.contains(search_query),
                Post.excerpt.contains(search_query),
            )
        )
    
    # Filter by category
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)
    
    # Filter by tag
    if tag_slug:
        tag = Tag.query.filter_by(slug=tag_slug).first()
        if tag:
            query = query.filter(Post.tags.contains(tag))
    
    # Get featured posts
    featured_posts = Post.query.filter_by(is_published=True, is_featured=True).order_by(desc(Post.created_at)).limit(3).all() if page == 1 else []
    
    # Pagination
    pagination = query.order_by(desc(Post.created_at)).paginate(page=page, per_page=per_page, error_out=False)
    
    # Get categories and tags for sidebar
    categories = Category.query.order_by(Category.name).all()
    popular_tags = db.session.query(Tag, func.count(post_tags.c.post_id).label("count")).join(post_tags).group_by(Tag).order_by(desc("count")).limit(10).all()
    
    return render_template(
        "index.html",
        pagination=pagination,
        posts=pagination.items,
        featured_posts=featured_posts,
        categories=categories,
        popular_tags=popular_tags,
        search_query=search_query,
        current_category=category_slug,
        current_tag=tag_slug,
    )


@app.route("/post/<string:slug>")
def post_detail(slug: str):
    """Display single post with comments"""
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    # Only show published posts to non-admins
    if not post.is_published and (not session.get("user_id") or not User.query.get(session["user_id"]).is_admin):
        abort(404)
    
    # Track view
    if post.is_published:
        ip_address = request.remote_addr
        user_agent = request.headers.get("User-Agent", "")
        
        # Avoid duplicate views from same IP in short time
        recent_view = PostView.query.filter_by(
            post_id=post.id,
            ip_address=ip_address
        ).filter(PostView.viewed_at > datetime.utcnow() - timedelta(hours=1)).first()
        
        if not recent_view:
            view = PostView(post_id=post.id, ip_address=ip_address, user_agent=user_agent)
            db.session.add(view)
            post.increment_views()
            db.session.commit()
    
    # Convert markdown to HTML
    post.content_html = markdown_to_html(post.content)
    
    # Get related posts (same category)
    related_posts = Post.query.filter(
        Post.category_id == post.category_id,
        Post.id != post.id,
        Post.is_published == True
    ).order_by(desc(Post.created_at)).limit(3).all()
    
    # Get approved comments
    comments = post.comments.filter_by(is_approved=True).all()
    
    return render_template(
        "post_detail.html",
        post=post,
        related_posts=related_posts,
        comments=comments,
    )


@app.route("/category/<string:slug>")
def category_posts(slug: str):
    """Display posts by category"""
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get("page", 1, type=int)
    per_page = 6
    
    pagination = Post.query.filter_by(
        category_id=category.id,
        is_published=True
    ).order_by(desc(Post.created_at)).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        "category.html",
        category=category,
        pagination=pagination,
        posts=pagination.items,
    )


@app.route("/tag/<string:slug>")
def tag_posts(slug: str):
    """Display posts by tag"""
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    page = request.args.get("page", 1, type=int)
    per_page = 6
    
    pagination = tag.posts.filter_by(is_published=True).order_by(desc(Post.created_at)).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        "tag.html",
        tag=tag,
        pagination=pagination,
        posts=pagination.items,
    )


# ==================== AUTHENTICATION ROUTES ====================

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    if "user_id" in session:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        # Validation
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")
        
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")
        
        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("register.html")
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return render_template("register.html")
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return render_template("register.html")
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        
        # First user becomes admin
        if User.query.count() == 0:
            user.is_admin = True
        
        db.session.add(user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    if "user_id" in session:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["is_admin"] = user.is_admin
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            if remember:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            
            next_url = request.args.get("next") or url_for("index")
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(next_url)
        else:
            flash("Invalid username or password.", "danger")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    """User logout"""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


# ==================== ADMIN ROUTES ====================

@app.route("/admin")
@admin_required
def admin_dashboard():
    """Admin dashboard with statistics"""
    stats = {
        "total_posts": Post.query.count(),
        "published_posts": Post.query.filter_by(is_published=True).count(),
        "draft_posts": Post.query.filter_by(is_published=False).count(),
        "total_views": db.session.query(func.sum(Post.views_count)).scalar() or 0,
        "total_comments": Comment.query.count(),
        "pending_comments": Comment.query.filter_by(is_approved=False).count(),
        "total_users": User.query.count(),
        "total_categories": Category.query.count(),
        "total_tags": Tag.query.count(),
    }
    
    # Recent posts
    recent_posts = Post.query.order_by(desc(Post.created_at)).limit(5).all()
    
    # Popular posts
    popular_posts = Post.query.filter_by(is_published=True).order_by(desc(Post.views_count)).limit(5).all()
    
    # Recent comments
    recent_comments = Comment.query.order_by(desc(Comment.created_at)).limit(5).all()
    
    return render_template(
        "admin_dashboard.html",
        stats=stats,
        recent_posts=recent_posts,
        popular_posts=popular_posts,
        recent_comments=recent_comments,
    )


@app.route("/admin/posts")
@admin_required
def admin_posts():
    """Admin post management"""
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "all")
    
    query = Post.query
    
    if search:
        query = query.filter(
            or_(
                Post.title.contains(search),
                Post.content.contains(search),
            )
        )
    
    if status_filter == "published":
        query = query.filter_by(is_published=True)
    elif status_filter == "draft":
        query = query.filter_by(is_published=False)
    
    posts = query.order_by(desc(Post.created_at)).all()
    
    return render_template("admin_posts.html", posts=posts, search=search, status_filter=status_filter)


@app.route("/admin/posts/create", methods=["GET", "POST"])
@admin_required
def create_post():
    """Create new post"""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        excerpt = request.form.get("excerpt", "").strip()
        category_id = request.form.get("category_id", type=int)
        tag_names = request.form.get("tags", "").strip()
        is_published = request.form.get("is_published") == "on"
        is_featured = request.form.get("is_featured") == "on"
        
        if not title or not content:
            flash("Title and content are required.", "danger")
            categories = Category.query.order_by(Category.name).all()
            return render_template("create_edit_post.html", mode="create", categories=categories)
        
        # Generate slug
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Post.query.filter_by(slug=slug).first() is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Create post
        post = Post(
            title=title,
            slug=slug,
            content=content,
            excerpt=excerpt or content[:200] + "..." if len(content) > 200 else content,
            author_id=session["user_id"],
            category_id=category_id if category_id else None,
            is_published=is_published,
            is_featured=is_featured,
        )
        
        # Calculate reading time
        post.reading_time = post.calculate_reading_time()
        
        # Set published_at if publishing
        if is_published:
            post.published_at = datetime.utcnow()
        
        # Handle tags
        if tag_names:
            tag_list = [t.strip() for t in tag_names.split(",")]
            for tag_name in tag_list:
                tag_slug = slugify(tag_name)
                tag = Tag.query.filter_by(slug=tag_slug).first()
                if not tag:
                    tag = Tag(name=tag_name, slug=tag_slug)
                    db.session.add(tag)
                post.tags.append(tag)
        
        db.session.add(post)
        db.session.commit()
        
        flash("Post created successfully.", "success")
        return redirect(url_for("admin_posts"))
    
    categories = Category.query.order_by(Category.name).all()
    return render_template("create_edit_post.html", mode="create", categories=categories)


@app.route("/admin/posts/<int:post_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_post(post_id: int):
    """Edit existing post"""
    post = Post.query.get_or_404(post_id)
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        excerpt = request.form.get("excerpt", "").strip()
        category_id = request.form.get("category_id", type=int)
        tag_names = request.form.get("tags", "").strip()
        is_published = request.form.get("is_published") == "on"
        is_featured = request.form.get("is_featured") == "on"
        
        if not title or not content:
            flash("Title and content are required.", "danger")
            categories = Category.query.order_by(Category.name).all()
            return render_template("create_edit_post.html", mode="edit", post=post, categories=categories)
        
        # Update slug if title changed
        if title != post.title:
            base_slug = slugify(title)
            slug = base_slug
            counter = 1
            while Post.query.filter(Post.slug == slug, Post.id != post.id).first() is not None:
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug
        
        # Update fields
        post.title = title
        post.content = content
        post.excerpt = excerpt or content[:200] + "..." if len(content) > 200 else content
        post.category_id = category_id if category_id else None
        post.is_featured = is_featured
        post.reading_time = post.calculate_reading_time()
        
        # Handle publish status
        was_published = post.is_published
        post.is_published = is_published
        if is_published and not was_published:
            post.published_at = datetime.utcnow()
        
        # Update tags
        post.tags.clear()
        if tag_names:
            tag_list = [t.strip() for t in tag_names.split(",")]
            for tag_name in tag_list:
                tag_slug = slugify(tag_name)
                tag = Tag.query.filter_by(slug=tag_slug).first()
                if not tag:
                    tag = Tag(name=tag_name, slug=tag_slug)
                    db.session.add(tag)
                post.tags.append(tag)
        
        db.session.commit()
        flash("Post updated successfully.", "success")
        return redirect(url_for("admin_posts"))
    
    categories = Category.query.order_by(Category.name).all()
    current_tags = ", ".join([tag.name for tag in post.tags])
    return render_template("create_edit_post.html", mode="edit", post=post, categories=categories, current_tags=current_tags)


@app.route("/admin/posts/<int:post_id>/delete", methods=["POST"])
@admin_required
def delete_post(post_id: int):
    """Delete post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully.", "success")
    return redirect(url_for("admin_posts"))


@app.route("/admin/categories", methods=["GET", "POST"])
@admin_required
def admin_categories():
    """Manage categories"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        
        if not name:
            flash("Category name is required.", "danger")
        else:
            slug = slugify(name)
            if Category.query.filter_by(slug=slug).first():
                flash("Category already exists.", "danger")
            else:
                category = Category(name=name, slug=slug, description=description)
                db.session.add(category)
                db.session.commit()
                flash("Category created successfully.", "success")
        
        return redirect(url_for("admin_categories"))
    
    categories = Category.query.order_by(Category.name).all()
    return render_template("admin_categories.html", categories=categories)


@app.route("/admin/categories/<int:category_id>/delete", methods=["POST"])
@admin_required
def delete_category(category_id: int):
    """Delete category"""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted successfully.", "success")
    return redirect(url_for("admin_categories"))


@app.route("/admin/comments")
@admin_required
def admin_comments():
    """Manage comments"""
    comments = Comment.query.order_by(desc(Comment.created_at)).all()
    return render_template("admin_comments.html", comments=comments)


@app.route("/admin/comments/<int:comment_id>/approve", methods=["POST"])
@admin_required
def approve_comment(comment_id: int):
    """Approve comment"""
    comment = Comment.query.get_or_404(comment_id)
    comment.is_approved = True
    db.session.commit()
    flash("Comment approved.", "success")
    return redirect(url_for("admin_comments"))


@app.route("/admin/comments/<int:comment_id>/delete", methods=["POST"])
@admin_required
def delete_comment(comment_id: int):
    """Delete comment"""
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully.", "success")
    return redirect(url_for("admin_comments"))


# ==================== COMMENT ROUTES ====================

@app.route("/post/<string:slug>/comment", methods=["POST"])
@login_required
def add_comment(slug: str):
    """Add comment to post"""
    post = Post.query.filter_by(slug=slug).first_or_404()
    content = request.form.get("content", "").strip()
    
    if not content:
        flash("Comment cannot be empty.", "danger")
        return redirect(url_for("post_detail", slug=slug))
    
    comment = Comment(
        content=content,
        post_id=post.id,
        author_id=session["user_id"],
        is_approved=True if session.get("is_admin") else False,  # Auto-approve admin comments
    )
    
    db.session.add(comment)
    db.session.commit()
    
    if session.get("is_admin"):
        flash("Comment added successfully.", "success")
    else:
        flash("Comment submitted and pending approval.", "info")
    
    return redirect(url_for("post_detail", slug=slug))


# ==================== API ROUTES ====================

@app.route("/api/posts")
def api_posts():
    """REST API endpoint for posts"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    per_page = min(per_page, 50)  # Limit to 50
    
    posts = Post.query.filter_by(is_published=True).order_by(desc(Post.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        "posts": [{
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "excerpt": post.excerpt,
            "created_at": post.created_at.isoformat(),
            "views_count": post.views_count,
            "author": post.author.username,
        } for post in posts.items],
        "total": posts.total,
        "page": posts.page,
        "pages": posts.pages,
    })


@app.route("/api/posts/<int:post_id>")
def api_post_detail(post_id: int):
    """REST API endpoint for single post"""
    post = Post.query.get_or_404(post_id)
    
    if not post.is_published:
        abort(404)
    
    return jsonify({
        "id": post.id,
        "title": post.title,
        "slug": post.slug,
        "content": post.content,
        "excerpt": post.excerpt,
        "created_at": post.created_at.isoformat(),
        "views_count": post.views_count,
        "author": post.author.username,
        "category": post.category.name if post.category else None,
        "tags": [tag.name for tag in post.tags],
    })


# ==================== RSS FEED ====================

@app.route("/feed")
def rss_feed():
    """RSS feed for blog posts"""
    posts = Post.query.filter_by(is_published=True).order_by(desc(Post.created_at)).limit(20).all()
    
    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>My Premium Blog</title>
        <link>{request.url_root}</link>
        <description>Latest blog posts</description>
        <language>en-us</language>
        <lastBuildDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
"""
    
    for post in posts:
        rss_xml += f"""
        <item>
            <title>{post.title}</title>
            <link>{request.url_root}post/{post.slug}</link>
            <description><![CDATA[{post.excerpt or post.content[:200]}]]></description>
            <pubDate>{post.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
            <guid>{request.url_root}post/{post.slug}</guid>
        </item>
"""
    
    rss_xml += """
    </channel>
</rss>"""
    
    response = make_response(rss_xml)
    response.headers["Content-Type"] = "application/rss+xml"
    return response


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    db.session.rollback()
    return render_template("500.html"), 500


# ==================== INITIALIZATION ====================

def migrate_database():
    """Migrate existing database to new schema"""
    with app.app_context():
        from sqlalchemy import inspect, text
        
        inspector = inspect(db.engine)
        
        # First, ensure all new tables exist (users, categories, tags, etc.)
        db.create_all()
        
        # Ensure we have at least one user for author_id defaults
        if User.query.count() == 0:
            admin = User(
                username="admin",
                email="admin@blog.com",
                is_admin=True,
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("✓ Created default admin user for migration")
        
        first_user = User.query.first()
        default_author_id = first_user.id if first_user else 1
        
        # Check if posts table exists and migrate it
        if 'posts' in inspector.get_table_names():
            # Get existing columns
            existing_columns = [col['name'] for col in inspector.get_columns('posts')]
            
            # Columns to add if missing (author_id handled separately)
            columns_to_add = [
                ('excerpt', 'TEXT', None),
                ('featured_image', 'VARCHAR(255)', None),
                ('is_featured', 'BOOLEAN', 'DEFAULT 0'),
                ('views_count', 'INTEGER', 'DEFAULT 0'),
                ('reading_time', 'INTEGER', None),
                ('published_at', 'DATETIME', None),
                ('category_id', 'INTEGER', None)
            ]
            
            # Add missing columns (except author_id)
            for column_name, column_type, default_clause in columns_to_add:
                if column_name not in existing_columns:
                    try:
                        alter_sql = f"ALTER TABLE posts ADD COLUMN {column_name} {column_type}"
                        if default_clause:
                            alter_sql += f" {default_clause}"
                        db.session.execute(text(alter_sql))
                        db.session.commit()
                        print(f"✓ Added column '{column_name}' to posts table")
                    except Exception as e:
                        print(f"✗ Error adding column '{column_name}': {e}")
                        db.session.rollback()
            
            # Handle author_id separately (add as nullable, then update, then make NOT NULL if needed)
            if 'author_id' not in existing_columns:
                try:
                    # Add as nullable first
                    db.session.execute(text(f"ALTER TABLE posts ADD COLUMN author_id INTEGER DEFAULT {default_author_id}"))
                    db.session.commit()
                    print("✓ Added column 'author_id' to posts table")
                    
                    # Update any NULL values
                    if first_user:
                        db.session.execute(text(f"UPDATE posts SET author_id = {default_author_id} WHERE author_id IS NULL"))
                        db.session.commit()
                        print("✓ Updated existing posts with author_id")
                except Exception as e:
                    print(f"✗ Error adding author_id: {e}")
                    db.session.rollback()
            
            # Create indexes if they don't exist
            try:
                db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_posts_is_featured ON posts(is_featured)"))
                db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_posts_views_count ON posts(views_count)"))
                db.session.commit()
            except Exception:
                pass  # Indexes may already exist


def create_tables():
    """Create database tables and default admin user"""
    with app.app_context():
        # Run migration first for existing databases
        migrate_database()
        
        # Create all tables (this won't recreate existing ones)
        db.create_all()
        
        # Create default admin user if no users exist
        if User.query.count() == 0:
            admin = User(
                username="admin",
                email="admin@blog.com",
                is_admin=True,
            )
            admin.set_password("admin123")  # Change this in production!
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created: username='admin', password='admin123'")
        
        # Create default category if none exist
        if Category.query.count() == 0:
            category = Category(name="Uncategorized", slug="uncategorized", description="Default category")
            db.session.add(category)
            db.session.commit()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True, host="0.0.0.0", port=5000)