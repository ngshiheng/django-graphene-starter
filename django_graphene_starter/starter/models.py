from django.db import models


class Reporter(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Publication(models.Model):
    title = models.CharField(max_length=256)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=256)
    pub_date = models.DateField(auto_now_add=True)
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, related_name='articles')
    publications = models.ManyToManyField(Publication, related_name='articles')

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ['headline']
