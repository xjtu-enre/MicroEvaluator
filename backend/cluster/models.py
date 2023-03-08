from django.db import models
from project.models import Version

# class FileAttribute(models.Model):
#     file_extension = models.CharField(default='',
#                                       max_length=10,
#                                       verbose_name='文件类型')
#     file_name = models.CharField(default='',
#                                  max_length=100,
#                                  verbose_name='文件名称')
#     status = models.BooleanField(verbose_name='是否解析', null=True)
#     parent_file = models.ForeignKey(to='self',
#                                     on_delete=models.CASCADE,
#                                     null=True,
#                                     blank=True,
#                                     verbose_name='上级文件',
#                                     related_name='children')

    # class Meta:
    #     abstract = True


class CatelogueAttributes(models.Model):
    name = models.CharField(default='',
                            max_length=150,
                            verbose_name='文件名称',
                            null=True)
    color = models.CharField(default='#FFFFFF',
                             max_length=30,
                             verbose_name='圆圈颜色',
                             null=True)
    relation = models.TextField(default='',
                                verbose_name='依赖变化',
                                null=True,
                                blank=True)
    version_project = models.ForeignKey(Version,
                                       on_delete=models.CASCADE,
                                       null=True,
                                       blank=True,
                                       verbose_name='所属项目')

    class Meta:
        abstract = True


class ClusterData(CatelogueAttributes):
    changeLoc = models.IntegerField(default=0, verbose_name='修改频率', null=True)
    value = models.FloatField(default=0.0, verbose_name='半径', null=True)
    parent_node = models.ForeignKey(to='self',
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    verbose_name='父类结点',
                                    related_name='children')
    cluster = models.SmallIntegerField(verbose_name='目录级别',
                                       default=0,
                                       null=False)
    cluster_algo = models.CharField(default='', max_length=30, null=False)

    class Meta:
        db_table = 'ClusterData'
        verbose_name = 'ClusterData'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class CatelogueData(CatelogueAttributes):
    # TODO 采用递归序列化recursive
    CATELOGUE_TYPE = (
        (1, '一级目录'),
        (2, '二级目录'),
    )
    changeLoc = models.IntegerField(default=0, verbose_name='修改频率', null=True)
    value = models.FloatField(default=0.0, verbose_name='半径', null=True)
    parent_catelogue = models.ForeignKey(to='self',
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True,
                                         verbose_name='父类目录',
                                         related_name='children')
    catelogue_type = models.SmallIntegerField(choices=CATELOGUE_TYPE,
                                              verbose_name='目录级别',
                                              default=1,
                                              null=False)

    class Meta:
        db_table = 'CatelogueData'
        verbose_name = 'CatelogueData'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class TreeMapData(CatelogueAttributes):
    end = models.BooleanField(default=False, null=True, blank=True)
    value = models.CharField(default='', max_length=50, null=True, blank=True)
    qualifiedName = models.CharField(default='',
                                     max_length=150,
                                     verbose_name='文件完整名称',
                                     null=True,
                                     blank=True)
    parent_catelogue = models.ForeignKey(to='self',
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True,
                                         verbose_name='父类目录',
                                         related_name='children')
    catelogue_type = models.SmallIntegerField(verbose_name='目录级别',
                                              default=1,
                                              null=False)

    class Meta:
        db_table = 'TreeMapData'
        verbose_name = 'TreeMapData'
        verbose_name_plural = verbose_name
        ordering = ['id']


# class SectionAttribute(models.Model):
#     version_project = models.ForeignKey(VersionProject,
#                                 on_delete=models.CASCADE,
#                                 null=True,
#                                 blank=True,
#                                 verbose_name='所属项目')
#
#     class Meta:
#         abstract = True


# class SectionNodes(SectionAttribute):
#     _id = models.IntegerField(default=0, null=False)
#     isHonor = models.SmallIntegerField(default=0, null=False)
#     category = models.CharField(default='', max_length=30, null=False)
#     qualifiedName = models.CharField(default='', max_length=200, null=False)
#     name = models.CharField(default='', max_length=100, null=False)
#     File = models.CharField(default='', max_length=150, null=True)
#     packageName = models.CharField(default='', max_length=100, null=True)
#     hidden = models.BooleanField(default=False)
#     modifiers = models.CharField(max_length=30, null=True)
#     _global = models.BooleanField(null=True)
#     mode_type = models.CharField(default='',
#                                  max_length=100,
#                                  verbose_name='模式类型',
#                                  null=True)
#
#     class Meta:
#         db_table = 'SectionNodeFile'
#         verbose_name = 'SectionNodeFile'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self._id
#
#
# class SectionEdges(SectionAttribute):
#     source = models.IntegerField(default=0, null=False)
#     target = models.IntegerField(default=0, null=False)
#     sourceFile = models.CharField(default='', max_length=150, null=True)
#     sourcePackageName = models.CharField(default='', max_length=100, null=True)
#     # 0 原生 1 伴生
#     sourceIsHonor = models.SmallIntegerField(default=0, null=False)
#     targetFile = models.CharField(default='', max_length=150, null=True)
#     targetPackageName = models.CharField(default='', max_length=100, null=True)
#     targetIsHonor = models.SmallIntegerField(default=0, null=False)
#     value = models.CharField(default='',
#                              max_length=30,
#                              null=True,
#                              verbose_name='依赖关系')
#     mode_type = models.CharField(default='',
#                                  max_length=50,
#                                  verbose_name='模式类型',
#                                  null=True)
#
#     class Meta:
#         db_table = 'SectionEdgeFile'
#         verbose_name = 'SectionEdgeFile'
#         verbose_name_plural = verbose_name