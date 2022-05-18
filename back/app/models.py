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
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
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
