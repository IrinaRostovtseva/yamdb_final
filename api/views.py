from django.db.models import Avg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User

from .filters import TitleFilter
from .confirms import confirmation_code
from .models import Category, Genre, Title, Review, Comment
from .permissions import IsAdminOrOwner, IsAdminOrReadOnly, IsStaffOrReadOnly
from .serializers import (
    JWTSerializer,
    UserSerializer,
    GenreSerializer,
    TitleSerializerGet,
    TitleSerializerPost,
    RegistrationSerializer,
    CategorySerializer,
    CommentSerializer,
    ReviewSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_registration(request):
    email = request.data.get('email')
    serializer = RegistrationSerializer(data=request.data, partial=True)
    is_exists = User.objects.filter(email=email).exists()
    serializer.is_valid(raise_exception=True)
    if not is_exists:
        serializer.save()
    code = confirmation_code.get_encode_string(email.split('@')[0])
    subject = 'Подтверждение регистрации.'
    message = f'Код подтверждения  - {code}.'
    send_mail(subject, message, 'admin@yambd.ru',
              [email], fail_silently=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = JWTSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.data['email']
    code = request.data['confirmation_code']
    user = get_object_or_404(User, email=email)
    if not confirmation_code.is_same(email.split('@')[0], code):
        return Response({'confirmation_code': 'Неверный код подтверждения'},
                        status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response({'token': f'{token}'}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrOwner,)
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['username', ]

    @action(detail=True, url_path='profile', methods=['get'])
    def get_profile(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, url_path='profile', methods=['patch'])
    def edit_profile(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CDLViewSet(mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    pass


class CategoryViewSet(CDLViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(CDLViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializerPost
        return TitleSerializerGet

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')
        )


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrReadOnly,)

    def __get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.__get_title())

    def get_queryset(self):
        return Review.objects.filter(title=self.__get_title())


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrReadOnly,)

    def __get_review(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return get_object_or_404(Review,
                                 pk=self.kwargs.get("review_id"),
                                 title=title)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.__get_review())

    def get_queryset(self):
        return Comment.objects.filter(review=self.__get_review())
