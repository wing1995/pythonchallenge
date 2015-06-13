from .models import Message, Member
from rest_framework import serializers

'''创建序列化类，将social实例转化成json格式，并输出相应的messages'''


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    age = serializers.SerializerMethodField('get_age')

    class Meta:
        model = Message
        fields = ('id', 'age', 'like', 'sex', 'created',)

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'username', 'messages',)





