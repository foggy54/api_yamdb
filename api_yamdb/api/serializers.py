from rest_framework import serializers

from .models import User, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'password')
        model = User
        
        
class EmailRegistration(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        user = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError(
                'Отзыв создан. Можно создавать только один отзыв.'
            )
        return data

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        read_only_fields = (
            'id',
            'pub_date',
            'author'
        )
        model = Review
