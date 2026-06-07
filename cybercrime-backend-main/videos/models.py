from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Video(models.Model):
    id = models.CharField(primary_key=True, max_length=20)  
    type = models.CharField(max_length=100)  
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=150)
    publish_date = models.DateField()
    link = models.URLField()
    suggested_reading_time = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'videos'  
        managed = False
        
    def __str__(self):
        return self.title


class VideoProgress(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE, db_column='video_id')
    progress = models.FloatField(default=0.0)  # in seconds
    is_completed = models.BooleanField(default=False)  # new field
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'video_progress'
        unique_together = ('user_id', 'video_id')
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['video_id']),
        ]

