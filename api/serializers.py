from rest_framework.serializers import ModelSerializer
from .models import Note, Userinfo, Maincomn, Subcomn, MyCollection, MyLike


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class UserinfoSerializer(ModelSerializer):
    class Meta:
        model = Userinfo
        fields = '__all__'


class MaincomnSerializer(ModelSerializer):
    class Meta:
        model = Maincomn
        fields = '__all__'


class SubcomnSerializer(ModelSerializer):
    class Meta:
        model = Subcomn
        fields = '__all__'


class MycollectionSerializer(ModelSerializer):
    class Meta:
        model = MyCollection
        fields = '__all__'

class MylikeSerializer(ModelSerializer):
    class Meta:
        model = MyLike
        fields = '__all__'
