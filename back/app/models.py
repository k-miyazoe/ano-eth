from pyexpat import model
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')

        email = self.normalize_email(email)
        #文字列を小文字に変換
        email = email.lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('status', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('status', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("メールアドレス", max_length=255, unique=True)
    username = models.CharField("名前", max_length=255)
    status = models.BooleanField(help_text='学生ならfalse')
    #not null制約解除
    eth_stock = models.IntegerField(null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #追加
    user_group = models.CharField("グループ",max_length=10)
    
    objects = UserManager()

    #USERNAME_FIELDで指定したフィールドは、ログイン認証やメール送信などで利用します。
    # ここをemailにすることでメールアドレスでのログインが可能になります。
    # 指定したフィールドは一意である必要があるため、ここで指定できるフィールドはunique=Trueである必要があります。
    USERNAME_FIELD = 'email'
    #ターミナルでユーザー作成（manage.py createsuperuser）するときに表示される項目です。
    # ユーザーは指定した項目の値を入力するよう求められます。
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Ether(models.Model):
    user_id      = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name    = models.CharField(null=True,max_length=255)
    ether_address = models.CharField(default="address",max_length=100)
    ether_password = models.CharField(default="password",max_length=20)
    ether_wallet   = models.IntegerField(default=0)
    ether_anonymous = models.BooleanField()
    ether_account_name = models.CharField(max_length=30)

class Question(models.Model):
    ether_id = models.ForeignKey(Ether, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=50)
    question_content = models.TextField()
    question_source_code = models.TextField(null=True)
    question_post_time = models.DateTimeField(auto_now_add=True)
    question_status = models.BooleanField(default=False)
    question_value = models.IntegerField(default=0)
    question_number_of_responses = models.IntegerField(default=0)

class Answer(models.Model):
    ether_id = models.ForeignKey(Ether, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer_content = models.TextField()
    answer_source_code = models.TextField(null=True)
    #作成日は自動で保存 フロント側でデータいらない
    answer_post_time = models.DateTimeField(auto_now_add=True)
    answer_value = models.IntegerField(default=0)
    answer_best = models.BooleanField(default=False)
   
    