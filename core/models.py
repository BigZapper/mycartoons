from django.db import models
from django.shortcuts import reverse
from django_extensions.db.fields import AutoSlugField

TYPE_CHOICES = (
    ('S', 'Phim bộ'),
    ('M', 'Phim lẻ')
)
STATUS_CHOICES = (
    ('HT', 'Hoàn thành'),
    ('DC', 'Đang sub'),
    ('DR', 'Drop')
)


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = AutoSlugField(populate_from=['name', ])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:genres", kwargs={
            'slug': self.slug
        })


class Translator(models.Model):
    name = models.CharField(max_length=50, default='')
    fb = models.CharField(max_length=200, default='')
    slug = AutoSlugField(populate_from=['name', ])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:translator", kwargs={
            'slug': self.slug
        })


class Film(models.Model):
    title = models.CharField(max_length=100, default='', blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    views = models.IntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2)
    typ = models.CharField(choices=TYPE_CHOICES, max_length=2)
    poster_url = models.CharField(max_length=255, blank=True, null=True)
    banner_url = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    imdb = models.FloatField(default=0)
    publish_date = models.DateField(auto_now=True)
    slug = AutoSlugField(populate_from=['title', ])
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def get_type(self):
        pass


class Serie(Film):

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:serie", kwargs={
            'slug': self.slug
        })

    def get_type(self):
        return "Serie"


class Movie(Film):
    url_fb = models.CharField(max_length=1000, blank=True, null=True)
    url_gd = models.CharField(max_length=1000, blank=True, null=True)
    trailer = models.CharField(max_length=255)
    translator = models.ManyToManyField(Translator)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:movie", kwargs={
            'slug': self.slug
        })

    def get_type(self):
        return "Movie"


class SerieSeason(models.Model):
    season_number = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    poster_url = models.CharField(max_length=255, blank=True, null=True)
    banner_url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2)
    episode_total = models.IntegerField()
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    slug = models.SlugField()
    imdb = models.FloatField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.serie.title + ' Mùa ' + str(self.season_number)

    def get_absolute_url(self):
        return reverse("core:season", kwargs={
            'serie_slug': self.serie.slug,
            'slug': self.slug
        })


class Episode(models.Model):
    ep_number = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=200)
    publish_date = models.DateField(auto_now=True)
    url_fb = models.CharField(max_length=1000, blank=True, null=True)
    url_gd = models.CharField(max_length=1000, blank=True, null=True)
    views = models.IntegerField(default=0)
    season = models.ForeignKey(SerieSeason, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from=['title', ])
    thumbnail_url = models.CharField(max_length=200)
    imdb = models.FloatField(default=0)
    translator = models.ManyToManyField(Translator)

    def __str__(self):
        return str(self.season) + ' Tập ' + str(self.ep_number)

    def get_absolute_url(self):
        return reverse("core:episode", kwargs={
            'serie_slug': self.season.serie.slug,
            'season_slug': self.season.slug,
            'slug': self.slug
        })
