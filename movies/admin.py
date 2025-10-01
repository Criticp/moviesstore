from django.contrib import admin
from .models import Movie, Review, Petition, PetitionVote


class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "requested_by", "created_at")
    search_fields = ("title", "requested_by__username", "reason")
    list_filter = ("created_at",)
    list_display_links = ("id", "title")


@admin.register(PetitionVote)
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ("id", "petition", "user", "created_at")
    search_fields = ("petition__title", "user__username")
    list_filter = ("created_at",)
    list_display_links = ("id", "petition")