import json
from django.core.management.base import BaseCommand
from cms.models import Post

class Command(BaseCommand):
    help = 'Extracts the string from the "text" key in processed_text_file and saves to post_text'

    def handle(self, *args, **options):
        # Filter posts that have a processed_text_file
        posts = Post.objects.filter(processed_text_file__isnull=False)
        
        updated_count = 0
        for post in posts:
            try:
                # Open the JSON file
                with post.processed_text_file.open('r') as f:
                    data = json.load(f)
                    
                    # Extract only the value associated with the "text" key
                    # This removes the {"text": "..."} wrapper
                    if isinstance(data, dict) and 'text' in data:
                        post.text = data['text']
                        post.save(update_fields=['text'])
                        updated_count += 1
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error on Post {post.id}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully cleaned {updated_count} posts.'))