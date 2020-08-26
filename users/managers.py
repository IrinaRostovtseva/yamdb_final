from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username,
                    email, password=None,
                    role='user', **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username,
                         email, password,
                         role='admin', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email,
                                password, role,
                                **extra_fields)
