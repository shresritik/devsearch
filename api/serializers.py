# serializers converts python objects to Json format
from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields='__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'


class ProjectSerializer(serializers.ModelSerializer):
    # for the boject relationship(many to many and foreign key) in their parent to get their values we override it
    owner=ProfileSerializer(many=False)
    tags=TagSerializer(many=True)
    # adding attribute using serializer model field here reviews is not shown as it is the child element
    reviews=serializers.SerializerMethodField()
    class Meta:
        model=Project
        fields='__all__'
    
    # the attribute of the serializermethodfield should start with get_
    def get_reviews(self,obj):
        reviews=obj.review_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return serializer.data

