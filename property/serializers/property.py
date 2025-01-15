from rest_framework import serializers
from ..models import Property, City, Owner


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='user__username', queryset=Owner.objects.all())
    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())
    image = serializers.SerializerMethodField()

    class Meta:
        model = Property
        exclude = ('id',)
        read_only_fields = ('created_at', 'updated_at')

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
