from rest_framework.response import Response
from rest_framework.decorators import api_view

from  myapp.system.models import User
# Create your views here.
@api_view()
def index(request):
  content = {
    'user':str(request.user),
    'auth':str(request.auth)
  }
  return Response(content)

@api_view()
def db(request):
  user = User.objects.create(username='admin',passsword='123456')
  user.save()
  return Response({'status':'ok'})
