---
name: drf-serializers
description: DRF serializer patterns for validation, nested data, and write operations.
---

# DRF Serializer Patterns

## ModelSerializer

```python
from rest_framework import serializers
from app.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "created_at"]
        read_only_fields = ["id", "created_at"]
```

## Custom Validation

```python
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "name", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
```

## Nested Serializers

```python
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street", "city", "country"]

class UserDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "address"]
```

## SerializerMethodField

```python
class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()
```

## Write Nested Data

```python
def create(self, validated_data):
    tags_data = validated_data.pop("tags", [])
    post = Post.objects.create(**validated_data)
    post.tags.set(tags_data)
    return post
```
