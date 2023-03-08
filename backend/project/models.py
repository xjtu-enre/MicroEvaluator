from django.db import models
from user.models import User


class CommonAttribute(models.Model):
    timestamp = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        abstract = True


# Create your models here.
class Project(CommonAttribute):
    projectname = models.CharField(max_length=500, null=False)
    url = models.CharField(max_length=500, null=False)
    description = models.TextField()
    ismicro = models.BooleanField(default=0)
    process = models.IntegerField(default=0)
    language = models.CharField(max_length=50, null=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE,
    #                             null=True,
    #                             blank=True,
    #                             verbose_name='所属用户')

    class Meta:
        db_table = 'Project'


class Version(CommonAttribute):
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                verbose_name='所属项目')
    loc = models.IntegerField(max_length=50, default=0)
    score = models.FloatField(max_length=50, default=0)
    version = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'Version'
        ordering = ['-timestamp']
