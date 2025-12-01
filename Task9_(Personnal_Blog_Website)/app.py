from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-to-a-random-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_published = db.Column(db.Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Post {self.title!r}>"


def slugify(title: str) -> str:
    """
    Create a URL-friendly slug from a title.
    Very simple implementation – good enough for a personal blog.
    """
    import re

    slug = title.strip().lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def create_tables() -> None:
    """Ensure database tables exist."""
    with app.app_context():
        db.create_all()


@app.route("/")
@app.route("/page/<int:page>")
def index(page: int = 1):
    per_page = 5
    pagination = (
        Post.query.filter_by(is_published=True)
        .order_by(Post.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    return render_template("index.html", pagination=pagination, posts=pagination.items)


@app.route("/post/<string:slug>")
def post_detail(slug: str):
    post = Post.query.filter_by(slug=slug, is_published=True).first()
    if not post:
        abort(404)
    return render_template("post_detail.html", post=post)


@app.route("/admin/posts")
def admin_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("admin_posts.html", posts=posts)


@app.route("/admin/posts/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        is_published = request.form.get("is_published") == "on"

        if not title or not content:
            flash("Title and content are required.", "danger")
            return render_template("create_edit_post.html", mode="create")

        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Post.query.filter_by(slug=slug).first() is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1

        post = Post(
            title=title,
            slug=slug,
            content=content,
            is_published=is_published,
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully.", "success")
        return redirect(url_for("admin_posts"))

    return render_template("create_edit_post.html", mode="create")


@app.route("/admin/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id: int):
    post = Post.query.get_or_404(post_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        is_published = request.form.get("is_published") == "on"

        if not title or not content:
            flash("Title and content are required.", "danger")
            return render_template(
                "create_edit_post.html", mode="edit", post=post
            )

        if title != post.title:
            base_slug = slugify(title)
            slug = base_slug
            counter = 1
            while (
                Post.query.filter(Post.slug == slug, Post.id != post.id).first()
                is not None
            ):
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug

        post.title = title
        post.content = content
        post.is_published = is_published

        db.session.commit()
        flash("Post updated successfully.", "success")
        return redirect(url_for("admin_posts"))

    return render_template("create_edit_post.html", mode="edit", post=post)


@app.route("/admin/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id: int):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully.", "success")
    return redirect(url_for("admin_posts"))


@app.errorhandler(404)
def not_found(error):  # type: ignore[override]
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Ensure database tables exist before starting the server.
    create_tables()
    # For development convenience. In production, use a proper WSGI server.
    app.run(debug=True)


