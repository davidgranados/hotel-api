from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def _create_user(self, email: str, password: str = None, **extra_fields):
        """
        Create and save a user with the given email, and password.
        :param email: email field
        :param password: password field
        :param extra_fields: extra fields
        :return: created User
        :rtype: Users
        """
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str = None, **extra_fields):
        """
        :param email: email field
        :param password: password field
        :param extra_fields: extra fields
        :return: created User
        :rtype: User
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email: str, password: str = None, **extra_fields):
        """
        Creates and saves a new user.
        :param email: email field
        :param password: password field
        :param extra_fields: extra fields
        :return: created user
        :rtype: User
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
