from django.core.management.base import BaseCommand
from articles.models import Article

class Command(BaseCommand):
    help = "Fetch and populate thumbnail_url for articles missing it."

    def handle(self, *args, **kwargs):
        articles = Article.objects.filter(thumbnail_url__isnull=True)
        count = 0

        for article in articles:
            self.stdout.write(f"Fetching thumbnail for: {article.title}")
            result = article.fetch_thumbnail()
            if result:
                self.stdout.write(self.style.SUCCESS(f"✔ Saved: {result}"))
                count += 1
            else:
                self.stdout.write(self.style.WARNING("✘ No thumbnail found."))

        self.stdout.write(self.style.SUCCESS(f"\nFinished! {count} articles updated."))
