from rest_framework import serializers
from .models import ImageData

class ImageDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    sha1 = serializers.CharField(max_length=40)
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    type = serializers.CharField(max_length=10)

    def create(self, validated_data):
        return ImageData.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.sha1 = validated_data.get('sha1', instance.sha1)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.type = validated_data.get('type', instance.type)

        instance.save()
        return instance
