import json
import requests
import re
from io import BytesIO
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.utils.text import slugify
import docx2txt
from bs4 import BeautifulSoup

from .models import Post


def extract_text_from_docx(docx_file):
    """Extract text content from DOCX file."""
    try:
        docx_bytes = BytesIO(requests.get(docx_file.url).content)
        text = docx2txt.process(docx_bytes)
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""


def text_to_html_paragraphs(text):
    """Convert plain text to HTML paragraphs following cecab logic."""
    if not text:
        return ""
    
    # Replace multiple newlines with a single newline to avoid empty paragraphs
    text = re.sub(r'\n\s*\n', '\n', text)
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Wrap each line in a <p> tag and join them
    return ''.join(f'<p>{line.strip()}</p>\n' for line in lines)


def split_html_by_paragraphs(html_text):
    """
    Split HTML by paragraph tags using BeautifulSoup.
    Returns a list of strings, each containing a full paragraph element.
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    paragraphs = soup.find_all('p')
    return [str(p) for p in paragraphs]


def process_html_content(post, html_paragraphs):
    """Process HTML content to add images and videos from post."""
    full = split_html_by_paragraphs(html_paragraphs)
    new_full = []
    
    for p in full:
        if not p.strip():
            continue
            
        temp = p
        
        # Handle S3 images
        if "https://" in p and (".jpg" in p or ".png" in p or ".jpeg" in p or ".gif" in p):
            p = p.replace("<p>", '').replace("</p>", '')
            temp = f"<img class='video-view' src='{p.strip()}' alt='{post.title}' />"
        
        # Handle YouTube URLs
        elif "youtube.com" in p or "youtu.be" in p:
            p = p.replace("<p>", '').replace("</p>", '')
            p = p.strip()
            # Convert youtube URL to embed
            youtube_id = p.split('v=')[-1] if 'v=' in p else p.split('/')[-1]
            embed_url = f"https://www.youtube.com/embed/{youtube_id}"
            temp = f"<div class='ratio ratio-16x9 video-view'><iframe src='{embed_url}?rel=0' title='YouTube video' allowfullscreen></iframe></div>"
        
        new_full.append(temp)
    
    return ''.join(new_full)


def generate_processed_json(post):
    """Generate JSON file with processed HTML content."""
    if not post.text_file:
        return None
    
    try:
        # Extract text from DOCX
        extracted_text = extract_text_from_docx(post.text_file)
        
        # Extract beginning (first 97 chars without newlines + "..." = 100 chars max)
        clean_text = extracted_text.replace('\n', '')
        beginning = (clean_text[:97] + "...") if len(clean_text) > 97 else clean_text
        
        # Convert to HTML paragraphs and remove all newlines
        html_text = text_to_html_paragraphs(extracted_text).replace("\n", "")
        
        # Process HTML with images and videos
        processed_text = process_html_content(post, html_text)
        
        # Save beginning as description if not already set
        if not post.description or post.description.startswith("Através desse seviço"):
            post.description = beginning

            Post.objects.filter(pk=post.pk).update(description=beginning, text=processed_text)
        else:
            Post.objects.filter(pk=post.pk).update(text=processed_text)
        
        # Create file name
        file_name = f"processed_{post.slug}_{post.id}.json"
        file_path = f"cms/posts/processed/{file_name}"
        
        # Save only processed text to JSON
        file_content = json.dumps({"text": processed_text}, ensure_ascii=False, indent=2)
        
        # This uses Django's default file storage
        from django.core.files.storage import default_storage
        file_url = default_storage.save(file_path, ContentFile(file_content.encode('utf-8')))
        
        print(f"Generated processed JSON: {file_url}")
        return file_url
        
    except Exception as e:
        print(f"Error generating processed JSON: {e}")
        return None


@receiver(post_save, sender=Post)
def process_post_text_file(sender, instance, created, update_fields, **kwargs):
    """
    Signal handler to process text_file when Post is created or updated.
    Generates HTML JSON file with processed content.
    """
    # Only process if text_file exists and was changed
    if instance.text_file:
        # Check if text_file was modified
        if update_fields is None or 'text_file' in update_fields or created:
            print(f"Processing text_file for Post: {instance.title}")
            
            # Generate processed JSON
            processed_file = generate_processed_json(instance)
            
            if processed_file:
                print(f"Successfully generated processed file: {processed_file}")
                # Update the instance with the processed file
                instance.processed_text_file = processed_file
                # Use update to avoid recursive signal
                Post.objects.filter(pk=instance.pk).update(processed_text_file=processed_file)
