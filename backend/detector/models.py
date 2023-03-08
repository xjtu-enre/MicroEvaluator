from django.db import models
from project.models import Version, Project


# Create your models here.
# 存储产生衰退的模块信息，每次前台点击查看根因时使用规则进行扫描
class DecayData(models.Model):
    start = models.ForeignKey(Version, related_name='start_version',
                                    on_delete=models.CASCADE,
                                    null=False,
                                    blank=True,
                                    verbose_name='衰退开始版本')
    end = models.ForeignKey(Version, related_name='end_version',
                                    on_delete=models.CASCADE,
                                    null=False,
                                    blank=True,
                                    verbose_name='衰退结束版本')
    project = models.ForeignKey(Project,
                                    on_delete=models.CASCADE,
                                    null=False,
                                    blank=True,
                                    verbose_name='所属项目')
    module = models.CharField(max_length=50, null=True, verbose_name='衰退模块')
    problem_metric = models.CharField(max_length=50, null=True, verbose_name='问题指标')
    problem_degree = models.CharField(max_length=50, null=True, verbose_name='衰退程度')

    class Meta:
        db_table = 'DecayData'
