from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView


class LoginView(FormView):
	"""
	View that handles the login details and process in the Chronos platform.
	"""

	form_class = AuthenticationForm
	redirect_field_name = REDIRECT_FIELD_NAME
	template_name = 'login/login_form.html'

	@method_decorator(sensitive_post_parameters('password'))
	@method_decorator(csrf_protect)
	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		# Sets a test cookie to make sure the user has cookies enabled
		request.session.set_test_cookie()

		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		auth_login(self.request, form.get_user())

		# If the test cookie worked, go ahead and
		# delete it since its no longer needed
		if self.request.session.test_cookie_worked():
			self.request.session.delete_test_cookie()

		return super(LoginView, self).form_valid(form)

	def get_success_url(self):
		redirect_to = self.request.GET.get(self.redirect_field_name)
		if not is_safe_url(url=redirect_to, host=self.request.get_host()):
			redirect_to = reverse_lazy('camera:index')
		return redirect_to


class LogoutView(RedirectView):
	"""
	View that handles the logout process in the Chronos platform.
	"""

	url = reverse_lazy('login:index')

	def get(self, request, *args, **kwargs):
		auth_logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)
