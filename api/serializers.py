from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class JWTSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name',
                  'username', 'email', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializerGet(serializers.ModelSerializer):
    genre = GenreSerializer(many=True,)
    category = CategorySerializer(allow_null=True,)
    rating = serializers.IntegerField(required=False,)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')


class TitleSerializerPost(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError('duplicate entry')
        super().validate(data)
        return data

    def validate_score(self, value):
        if value > 0 and value <= 10:
            return value
        raise serializers.ValidationError('Score must be between 1 and 10')


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')
