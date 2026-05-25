from django.core.management.base import BaseCommand
from django.db.models import Q
from cms.models import Post
from cms.signals import generate_processed_json

class Command(BaseCommand):
    help = 'Process all posts with text_file (.docx) and generate processed JSON files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Reprocess all posts, even if they already have processed_text_file',
        )
        parser.add_argument(
            '--id',
            type=int,
            help='Process a specific post by ID',
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Show debug information about available posts',
        )

    def handle(self, *args, **options):
        # Debug mode - show available posts
        if options['debug']:
            self.stdout.write(self.style.SUCCESS('\n📊 Debug Information:'))
            total_posts = Post.objects.count()
            self.stdout.write(f'Total posts: {total_posts}')
            
            posts_with_text_file = Post.objects.filter(text_file__isnull=False).count()
            self.stdout.write(f'Posts with text_file: {posts_with_text_file}')
            
            posts_with_processed = Post.objects.filter(text_file__isnull=False).exclude(
                Q(processed_text_file__isnull=True) | Q(processed_text_file='')
            ).count()
            self.stdout.write(f'Posts with processed_text_file: {posts_with_processed}')
            
            posts_to_process = Post.objects.filter(text_file__isnull=False).filter(
                Q(processed_text_file__isnull=True) | Q(processed_text_file='')
            ).count()
            self.stdout.write(f'Posts to process: {posts_to_process}\n')
            
            if posts_with_text_file > 0:
                self.stdout.write('Posts with text_file:')
                for p in Post.objects.filter(text_file__isnull=False):
                    processed_status = '✓' if p.processed_text_file else '✗'
                    self.stdout.write(f'  [{processed_status}] ID: {p.id}, Title: {p.title}, Slug: {p.slug}')
            return
        
        # Get posts to process
        if options['id']:
            # Process specific post
            try:
                posts = Post.objects.filter(id=options['id'], text_file__isnull=False)
                if not posts.exists():
                    self.stdout.write(self.style.ERROR(f'Post with ID {options["id"]} not found or has no text_file'))
                    return
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))
                return
        elif options['all']:
            # Reprocess all posts with text_file
            posts = Post.objects.filter(text_file__isnull=False)
        else:
            # Process only posts without processed_text_file (null or empty)
            posts = Post.objects.filter(text_file__isnull=False).filter(
                Q(processed_text_file__isnull=True) | Q(processed_text_file='')
            )
        
        total = posts.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS('No posts to process'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Processing {total} posts...'))
        
        processed_count = 0
        failed_count = 0
        
        for idx, post in enumerate(posts, 1):
            try:
                self.stdout.write(f'[{idx}/{total}] Processing: {post.title} (ID: {post.id})...')
                
                # Generate processed JSON
                processed_file = generate_processed_json(post)
                
                if processed_file:
                    # Update the post with the processed file
                    post.processed_text_file = processed_file
                    post.save()
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Generated: {processed_file}'))
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Description: {post.description[:250]}...'))
                    processed_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ Failed to generate processed file'))
                    failed_count += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error processing post: {e}'))
                failed_count += 1
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Successfully processed: {processed_count}/{total}'))
        if failed_count > 0:
            self.stdout.write(self.style.WARNING(f'Failed: {failed_count}/{total}'))
        self.stdout.write('='*50)
