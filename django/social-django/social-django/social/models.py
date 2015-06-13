from django.db import models


class Profile(models.Model):  # 账户附加信息
    text = models.CharField(max_length=4096)

    def __str__(self):
        if self.member:
            return self.member.username + ": " + self.text  # 如果是会员，将会返回会员的名字和附加信息
        return self.text  # 如果是游客，将只返回附加信息


class Message(models.Model):  # 社交网站上的信息模型
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    age = models.IntegerField()  # 用户年龄
    sex = models.CharField('sex', choices=(('M', 'Male'), ('F', 'Female')),
                           max_length=1)  # 性别
    like = models.CharField(max_length=20)  # 喜好

    class Meta:
        ordering = ('created',)  # 依据创建时间排序

    def __str__(self):
        if self.member:
            return self.member.username + "like" + self.like  # 如果是会员，将会返回会员的喜好
        return self.like  # 如果是游客，将只返回部分信息


class Member(models.Model):  # 用户信息
    username = models.CharField(max_length=16, primary_key=True)  # 用户名
    password = models.CharField(max_length=16)  # 密码
    profile = models.OneToOneField(Profile, null=True)  # 账户附加信息，而且和Profile模型是一对一关系
    following = models.ManyToManyField("self", symmetrical=False)  # 收听对象，可以多人参与
    messages = models.OneToOneField(Message, null=True)  # 个人信息

    def __str__(self):
        return self.username












