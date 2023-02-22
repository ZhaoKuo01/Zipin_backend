from django.db import models


# 单产品评测总表
class Note(models.Model):
    au_id = models.BigIntegerField()
    body = models.TextField()
    title = models.CharField(max_length=15)
    tag = models.CharField(max_length=10)
    put_time = models.DateTimeField(auto_now_add=True)
    like_num = models.IntegerField()
    coll_num = models.IntegerField()

    def __str__(self):
        return self.body


# 用户信息表
class Userinfo(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=24)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    identity = models.CharField(max_length=10,default="normal")
    is_active = models.BooleanField(default=0)

    def __str__(self):
        return self.username


class Maincomn(models.Model):
    # 评论的文章id
    pa_id = models.BigIntegerField()
    # 评论发布者用户名
    u_name = models.CharField(max_length=20)
    # 评论发布者id
    u_id = models.BigIntegerField()

    content = models.CharField(max_length=100)
    p_time = models.DateTimeField(auto_now_add=True)
    like_num = models.IntegerField()


class Subcomn(models.Model):
    pa_id = models.BigIntegerField(default=0)
    # 评论的评论id
    m_id = models.BigIntegerField()
    # 评论发布者用户名
    u_name = models.CharField(max_length=20)
    # 评论发布者id
    u_id = models.BigIntegerField()

    content = models.CharField(max_length=100)
    p_time = models.DateTimeField(auto_now_add=True)
    like_num = models.IntegerField()


class MyCollection(models.Model):
    user = models.ForeignKey(to=Userinfo, on_delete=models.CASCADE)
    note = models.ForeignKey(to=Note, on_delete=models.CASCADE)
    collect_time = models.DateTimeField(auto_now_add=True)


class MyLike(models.Model):
    user = models.ForeignKey(to=Userinfo, on_delete=models.CASCADE)
    note = models.ForeignKey(to=Note, on_delete=models.CASCADE)
    like_time = models.DateTimeField(auto_now_add=True)


class NoteImage(models.Model):
    note = models.ForeignKey(to=Note, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="img_url/")
    create_time = models.DateTimeField(auto_now_add=True)
