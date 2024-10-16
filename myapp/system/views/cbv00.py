from django.views import View
from django.http import HttpResponse

class UserView(View):
    def get(self,request):
        return HttpResponse('get')