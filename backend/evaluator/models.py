from project.models import *


class MetricAttribute(models.Model):
    metric = models.CharField(max_length=50, null=False)
    value = models.FloatField(max_length=50, default=0)

    class Meta:
        abstract = True


class ProjectMetricData(MetricAttribute):
    version = models.ForeignKey(Version,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                verbose_name='所属版本')

    class Meta:
        db_table = 'ProjectMetricData'


class ModuleMetricData(MetricAttribute):
    module = models.CharField(max_length=50, null=True)
    version = models.ForeignKey(Version,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                verbose_name='所属版本')

    class Meta:
        db_table = 'ModuleMetricData'


class ClassMetricData(MetricAttribute):
    classname = models.CharField(max_length=100, null=True)
    module = models.ManyToManyField(ModuleMetricData)

    class Meta:
        db_table = 'ClassMetricData'


class MethodMetricData(MetricAttribute):
    method = models.CharField(max_length=100, null=True)
    classname = models.ManyToManyField(ClassMetricData)

    class Meta:
        db_table = 'MethodMetricData'
