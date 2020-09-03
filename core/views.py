from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Serie, SerieSeason, Episode, Movie, Category, Film, Category, Translator
from django.views.generic.list import MultipleObjectMixin


class HomeView(ListView):
    model = Serie
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_movie_list'] = Movie.objects.order_by('-publish_date')[:6]
        context['serie_list'] = Serie.objects.order_by('-publish_date')[:6]
        context['genres_list'] = Category.objects.order_by('name')
        context['episode_list'] = Episode.objects.order_by('-id')[:10]
        return context


class GenresView(DetailView, MultipleObjectMixin):
    model = Category
    template_name = "genres.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        object_list = Film.objects.filter(category=self.get_object())
        context = super(GenresView, self).get_context_data(object_list=object_list, **kwargs)
        context['genres_list'] = Category.objects.order_by('name')
        return context


class TranslatorView(DetailView):
    model = Translator
    template_name = "list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['episode_list'] = Episode.objects.filter(translator=self.object)
        context['movie_list'] = Movie.objects.filter(translator=self.object)
        context['genres_list'] = Category.objects.order_by('name')
        return context


class SeriesListView(ListView):
    model = Serie
    template_name = "film_list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres_list'] = Category.objects.order_by('name')
        return context


class MoviesListView(ListView):
    model = Movie
    template_name = "film_list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres_list'] = Category.objects.order_by('name')
        return context


class MovieView(DetailView):
    model = Movie
    template_name = "movie.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['serie_list'] = Serie.objects.order_by('-publish_date')[:6]
        context['movie_list'] = Movie.objects.order_by('-publish_date')[:6]
        context['genres_list'] = Category.objects.order_by('name')
        return context


class SerieView(DetailView):
    model = Serie
    template_name = "serie.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['season_list'] = SerieSeason.objects.filter(serie=self.object).order_by('id')
        context['serie_list'] = Serie.objects.order_by('-publish_date')[:6]
        context['movie_list'] = Movie.objects.order_by('-publish_date')[:6]
        context['genres_list'] = Category.objects.order_by('name')
        return context


class SeasonView(DetailView):
    model = SerieSeason
    template_name = "season.html"

    def get_queryset(self):
        qs = super(SeasonView, self).get_queryset()
        return qs.filter(
            serie__slug=self.kwargs['serie_slug'],
            slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['episode_list'] = Episode.objects.filter(season=self.object).order_by('ep_number')
        context['season_list'] = SerieSeason.objects.filter(serie=self.object.serie).order_by('id')
        context['serie_list'] = Serie.objects.order_by('-publish_date')[:6]
        context['movie_list'] = Movie.objects.order_by('-publish_date')[:6]
        context['genres_list'] = Category.objects.order_by('name')
        return context


class EpisodeView(DetailView):
    model = Episode
    template_name = "episode.html"

    def get_queryset(self):
        qs = super(EpisodeView, self).get_queryset()
        return qs.filter(
            season__slug=self.kwargs['season_slug'],
            slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['episode_list'] = Episode.objects.filter(season=self.object.season).order_by('ep_number')
        context['season_list'] = SerieSeason.objects.filter(serie=self.object.season.serie).order_by('id')
        context['serie_list'] = Serie.objects.order_by('-publish_date')[:6]
        context['movie_list'] = Movie.objects.order_by('-publish_date')[:6]
        context['genres_list'] = Category.objects.order_by('name')
        return context
