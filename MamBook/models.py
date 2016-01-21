from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    class Meta:
        db_table = 'profile'

    owner = models.ForeignKey(User)
    csrf_token = models.CharField(max_length=255)
    current_version_progress = models.CharField(max_length=100)
    current_version_achievement = models.CharField(max_length=100)

    def __str__(self):
        return self.owner.username


class Baby(models.Model):
    class Meta:
        db_table = 'baby'

    parent = models.ForeignKey(Profile)
    birthday = models.DateField()
    current_age = models.DateField()
    name = models.CharField(max_length=50)
    avatar = models.ImageField()

    def __str__(self):
        return self.name


class Achievement(models.Model):  # all achievements in db
    class Meta:                   # parsed
        db_table = 'achievement'

    title = models.CharField(max_length=256)
    content = models.TextField()
    year = models.IntegerField()
    month = models.IntegerField()
    number = models.IntegerField()

    def __str__(self):
        return self.title


class BabyAchievements(models.Model):  # relations of babies and their achievements
    class Meta:
        db_table = 'baby-achievement'

    id_child = models.ForeignKey(Baby)
    id_achievement = models.ForeignKey(Achievement)
    activation_date = models.DateTimeField(null=True)
    status = models.BooleanField(default=None)
    is_activate = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.id_child.name, self.id_achievement.title)


class Category(models.Model):  # parsed
    class Meta:
        db_table = 'category'

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Progress(models.Model):  # parsed
    class Meta:
        db_table = 'progress'

    title = models.CharField(max_length=256)
    content = models.TextField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    category = models.ForeignKey(Category)
    do_advice = models.TextField()
    not_do_advice = models.TextField()

    def __str__(self):
        return self.title


class SelfDevelopment(models.Model):  # parsed
    class Meta:
        db_table = 'self-development'

    title = models.CharField(max_length=256)
    content = models.TextField()
    day = models.IntegerField()

    def __str__(self):
        return self.title


class VersionsControl(models.Model):
    class Meta:
        db_table = 'versions_control'

    table_name = models.CharField(max_length=128)
    latest_version = models.CharField(max_length=32)

    def __str__(self):
        return '%s - %s' % (self.table_name, self.latest_version)
