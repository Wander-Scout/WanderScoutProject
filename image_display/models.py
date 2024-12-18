from django.db import models

class RSSItem(models.Model):
    # Info from the rss feed
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    #pulled based of the XML in the rss feed

    def __str__(self):
        return self.title

class ImageModel(models.Model):
    image_url = models.URLField(max_length=500)
    caption = models.CharField(max_length=200)

    def __str__(self):
        return self.caption