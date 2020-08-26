from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategotyAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "review", "text", "author", "pub_date",)


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "text", "author", "score", "pub_date",)


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "description", "category",)


admin.site.register(Category, CategotyAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
