# backends.py
from django.contrib.auth import backends, get_user_model


UserModel = get_user_model()


class HashedPasswordAuthBackend(backends.ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        else:
            user = UserModel.objects.get(username=username)
            if user.password == password and self.user_can_authenticate(user):
                return user
        return super().authenticate(request, username, password, **kwargs)