from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.core.mail import send_mail
# from django.contrib.auth.models import PermissionsMixin, UserManager
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.utils.translation import ugettext_lazy as _
# from django.utils import timezone


# class CustomUserManager(UserManager):
#     """ユーザーマネージャー"""
#     use_in_migrations = True

#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self._create_user(email, password, **extra_fields)

# # Create your models here.
# class CustomUser(AbstractBaseUser, PermissionsMixin):
    
#     """カスタムユーザーモデル.
#     usernameの代わりにemailを使うようにしている。
#     """

#     email = models.EmailField(_('email address'), unique=True)
#     first_name = models.CharField(_('first name'), max_length=30, blank=True)
#     last_name = models.CharField(_('last name'), max_length=150, blank=True)

#     is_staff = models.BooleanField(
#         _('staff status'),
#         default=False,
#         help_text=_(
#             'Designates whether the user can log into this admin site.'),
#     )
#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

#     objects = CustomUserManager()

#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')

#     def get_full_name(self):
#         """Return the first_name plus the last_name, with a space in
#         between."""
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()

#     def get_short_name(self):
#         """Return the short name for the user."""
#         return self.first_name

#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """Send an email to this user."""
#         send_mail(subject, message, from_email, [self.email], **kwargs)

#     @property
#     def username(self):
#         """username属性のゲッター

#         他アプリケーションが、username属性にアクセスした場合に備えて定義
#         メールアドレスを返す
#         """
#         return self.email

# class WorkPlace(models.Model):

#     """ WorkPlace モデル　"""
#     class Meta:
#         #テーブル名を定義
#         db_table = 'WorkPlace'

#     name = models.CharField("ワークプレース",max_length = 128)
#     work_place_url = models.CharField("slac url", max_length=100, null=True)

#     members = models.ManyToManyField("CustomUser",
#                                      through="WorkPlacePersonRelation")  # 追加


# class WorkPlacePersonRelation(models.Model) :

#     """ WorkPlace＆Person リレーション モデル　"""
#     class Meta:
#         #テーブル名を定義
#         db_table = 'Relation_WorkPlacePerson'

#     NOT_EXIT = 0 # 0:離席
#     EXIT = 1     #1:着席

#     workPlace = models.ForeignKey("WorkPlace", on_delete=models.CASCADE)
#     User = models.ForeignKey("CustomUser", on_delete=models.CASCADE)

#     login_status = models.IntegerField("ログインステータス") # 0:離席　1:着席


# class Channel(models.Model):

#     """ Channel モデル　"""
#     class Meta:
#         #テーブル名を定義
#         db_table = 'Channel'
    
#     Channel_name = models.CharField("チャンネル",max_length = 128)

#     WorkPlace =models.ManyToManyField("WorkPlace")

# class direct_message(models.Model):

#     """　direct_message情報　モデル　"""
#     class Meta:
#         #テーブル名を定義
#         db_table = 'direct_message'

#     message = models.TextField("メッセージ")
#     WorkPlace = models.ForeignKey("WorkPlace", on_delete=models.CASCADE)
#     from_member = models.ForeignKey("CustomUser", on_delete=models.CASCADE,related_name = "from_member")
#     to_member = models.ForeignKey("CustomUser",
#                                   on_delete=models.CASCADE,
#                                   related_name="to_member")
#     send_time = models.DateTimeField("送信時刻")

# class Channel_message(models.Model):

#     """　Channel_message情報　モデル　"""
#     class Meta:
#         #テーブル名を定義
#         db_table = 'Channel_message'

#     message = models.TextField("メッセージ")
#     WorkPlace = models.ForeignKey("WorkPlace", on_delete=models.CASCADE)
#     send_member = models.ForeignKey("CustomUser",
#                                     on_delete=models.CASCADE,
#                                     related_name="send_member")
#     send_time = models.DateTimeField("送信時刻")
