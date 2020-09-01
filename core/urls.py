from django.urls import path
from .views import HomeView, SerieView, EpisodeView, SeasonView, MovieView, GenresView, SeriesListView, MoviesListView, TranslatorView

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('serie/<slug>/', SerieView.as_view(), name='serie'),
    path('movie/<slug>/', MovieView.as_view(), name='movie'),
    path('genres/<slug:slug>/', GenresView.as_view(), name='genres'),
    path('series-list/', SeriesListView.as_view(), name='series_list'),
    path('translator/<slug:slug>/', TranslatorView.as_view(), name='translator'),
    path('movies-list/', MoviesListView.as_view(), name='movies_list'),
    path('serie/<slug:serie_slug>/<slug:slug>/', SeasonView.as_view(), name='season'),
    path('serie/<slug:serie_slug>/<slug:season_slug>/<slug:slug>/', EpisodeView.as_view(), name='episode')
]
