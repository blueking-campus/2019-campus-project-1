from django.http import JsonResponse


class APIResult(JsonResponse):
    def __init__(self, code, data, message=''):
        assert isinstance(data, (list, dict))

        result = {
            'result': True,
            'code': code,
            'data': data,
            'message': message
        }

        super(APIResult, self).__init__(result)
