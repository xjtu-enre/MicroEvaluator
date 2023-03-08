from rest_framework.response import Response


class APIResponse(Response):

    def __init__(self,
                 status_code,
                 msg,
                 data=None,
                 url=None,
                 headers=None,
                 content_type=None,
                 *args,
                 **kwargs):
        dic = {'code': status_code}
        if data is not None:
            dic['result'] = data
        dic['message'] = msg
        if url is not None:
            dic['url']=url
        super().__init__(data=dic,
                         status=status_code,
                         headers=headers,
                         content_type=content_type)
