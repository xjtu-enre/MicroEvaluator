# Create your views here.
# django自带用户类
from rest_framework.decorators import action
from user.models import User
from backend.utils.response import APIResponse
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet
from user.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 根据这方法可以看出请求的是谁，返回哪个序列化器
    # def get_serializer_class(self):
    #     if self.action == 'lastdata':
    #         return BookSerializer
    #     else:
    #         return BookSerializer

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            # # 提取特征文件->存储可视化数据->存储聚类数据->存储度量数据
            # version_projects = VersionProject.objects.filter(project=serializer.data['id']).all()
            # version_info = self.get_version_info(version_projects)
            # task_id = storeData.delay(version_info, serializer.data['projectname'], serializer.data['url'], serializer.data['ismicro'])
            return APIResponse(HTTP_200_OK, 'success', str('task_id'))
        except:
            print(serializer.data)
            return APIResponse(HTTP_204_NO_CONTENT, 'fail', serializer.data)

    #     # 检测用户已登录过点击注册则跳转主页，注销才能重新注册，会保存15分钟登录状态
    #     if request.user.is_authenticated:
    #         return redirect(reverse('index'))
    #     return render(request, 'register.html')
    #
    #     # 注册
    #     username = request.POST.get('username', '')  # 用户名
    #     password = request.POST.get('password', '')  # 密码
    #     check_password = request.POST.get('check_password', '')  # 确认密码
    #
    #     # 检测密码与确认密码一致
    #     if password != check_password:
    #         messages.success(request, "密码不一致")
    #         return redirect(reverse('register'))
    #
    #     # 检测是否为空
    #     if username == '' or password == '' or check_password == '':
    #         messages.success(request, "不能为空!")
    #         return redirect(reverse('register'))
    #
    #     # 检测当前账号是否注册过并提示用户
    #     exists = user.objects.filter(username=username).exists()
    #     if exists:
    #         messages.success(request, "该账号已注册!")
    #         return redirect(reverse('register'))
    #     user.objects.create_user(username=username, password=password)
    #     return redirect(reverse('login'))


# 登录
# class LoginViewSet(ModelViewSet):
#
#     def get(self, request):
#         # 检测用户已登录过点击注册则跳转主页，注销才能重新登录，会保存15分钟登录状态
#         if request.user.is_authenticated:
#             return redirect(reverse('index'))
#         return render(request, 'login.html')
#
#     def post(self, request):
#         # 登录
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         check_password = request.POST.get('check_password', '')
#
#         # 判断当前用户是否存在,不存在则重新注册
#         exists = User.objects.filter(username=username).exists()
#         if not exists:
#             messages.success(request, "该账号不存在，请重新注册!")
#             return redirect(reverse('login'))
#
#         # 检测是否为空
#         if username == '' or password == '' or check_password == '':
#             messages.success(request, "不能为空!")
#             return redirect(reverse('login'))
#
#         # 验证账号密码正确
#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect(reverse('index'))
#         else:
#             messages.success(request, "密码错误")
#             return redirect(reverse('login'))