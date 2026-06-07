from django.db import models
import requests
from bs4 import BeautifulSoup


class Article(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=150)
    publish_date = models.DateField()
    description = models.TextField()
    link = models.URLField()
    suggested_reading_time = models.IntegerField()
    created_at = models.DateTimeField()
    thumbnail_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'articles'
        managed = True

    def __str__(self):
        return self.title

    def fetch_thumbnail(self):
        if not self.link:
            return None
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/117.0.0.0 Safari/537.36"
                )
            }
            response = requests.get(self.link, timeout=5, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Try og:image (property or name)
                og_image = (
                    soup.find("meta", property="og:image") or 
                    soup.find("meta", attrs={"name": "og:image"}) or
                    soup.find("meta", attrs={"name": "twitter:image"})
                )

                if og_image and og_image.get("content"):
                    self.thumbnail_url = og_image["content"]
                    self.save(update_fields=["thumbnail_url"])
                    return self.thumbnail_url

                # Fallback to first <img>
                first_img = (
                    soup.select_one("article img") or 
                    soup.select_one("main img") or 
                    soup.find("img")
                )
                if first_img and first_img.get("src"):
                    self.thumbnail_url = first_img["src"]
                    self.save(update_fields=["thumbnail_url"])
                    return self.thumbnail_url

        except Exception as e:
            print(f"[ERROR] Failed to fetch thumbnail from {self.link}: {e}")
        return None
