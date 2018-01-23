from models import FrontUserModel
import configs
from django.shortcuts import redirect,reverse

def front_login_required(func):
	def wrapper(request,*args,**kwargs):
		uid = request.session.get(configs.LOGINED_KEY)
		if uid:
			return func(request,*args,**kwargs)
		else:
			url = reverse('front_signin')+'?next=' + request.path
			return redirect(url)
	return wrapper



