import hashlib
import os
from datetime import datetime
import requests
from PIL import Image
import io


def generate_hash(title, content):
    hash_object = hashlib.sha256((title + content).encode())
    return hash_object.hexdigest()


def save_data(title, content, image_url):
    date_str = datetime.now().strftime("%Y-%m-%d")
    content_hash = generate_hash(title, content)

    # Directory for this blog's data
    blog_dir = os.path.join('data', title)
    images_dir = os.path.join(blog_dir, 'images')
    posts_dir = os.path.join(blog_dir, 'posts')

    # Ensure directories exist
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(posts_dir, exist_ok=True)

    # Filenames
    image_filename = f"{date_str}_{content_hash}.png"
    post_filename = f"{date_str}_{content_hash}.txt"

    # Check if this post already exists to avoid duplicates
    if not os.path.exists(os.path.join(posts_dir, post_filename)):
        # Save Image
        image_response = requests.get(image_url)
        image = Image.open(io.BytesIO(image_response.content))
        image_path = os.path.join(images_dir, image_filename)
        image.save(image_path)

        # Save Content and Title
        post_path = os.path.join(posts_dir, post_filename)
        with open(post_path, "w") as file:
            file.write(f"Title: {title}\nContent: {content}")
    else:
        print(f"Duplicate content detected for '{title}'. Skipping...")

# Example usage
# blog_name = 'example_blog'
# title = 'Example Post Title'
# content = 'This is the post content.'
# image_url = 'http://example.com/image.png'
# save_data(blog_name, title, content, image_url)
