from models import FrontUserModel
import configs
from django.utils.deprecation import MiddlewareMixin
class AuthMiddleware(MiddlewareMixin):

	def process_request(self,request):

		if request.session.get(configs.LOGINED_KEY):

			if not hasattr(request,'front_user'):
				uid = request.session.get(configs.LOGINED_KEY)
				user = FrontUserModel.objects.filter(pk=uid).first()
				setattr(request,'front_user',user)