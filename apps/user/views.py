from datetime import datetime
from math import floor

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_validators_help_texts
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from apps.user.forms import UserForm

"""
User views created to manage the user CRUD operation.
"""


class UserIndexView(LoginRequiredMixin, ListView):
	"""
	View that is used to show all the users that exist in the Chronos platform.
	Receives optional parameters to show alert functions:
	@param result (optional) - Shows alert functions accordingly

		User added - YWRkZWQ=
		User edited - ZWRpdGVk
		User deleted - ZGVsZXRlZA==

	TODO: Develop this view
	"""

	template_name = 'user/user_index.html'
	model = User

	def get_alert_information(self):
		"""
		Function used to generate the alert string based on the return result by URL
		:return: String containing the result message
		"""
		if 'result' in self.kwargs:
			if self.kwargs['result'] == 'YWRkZWQ=':
				return _("A new user was added with success!")
			if self.kwargs['result'] == 'ZWRpdGVk':
				return _("The user information was edited with success!")
			if self.kwargs['result'] == 'ZGVsZXRlZA==':
				return _("The user information was deleted with success!")

	def get_context_data(self, **kwargs):
		context = super(UserIndexView, self).get_context_data(**kwargs)
		context['page_title'] = _('USERS')
		context['title'] = _('User list')
		context['user_active'] = 'active'
		context['result'] = self.get_alert_information()

		return context


class UserDetailView(LoginRequiredMixin, DetailView):
	"""
	View that is used to show the user information that exists in the Chronos platform.
	TODO: Develop this view
	"""

	template_name = "user/user_base.html"
	model = User

	def get_context_data(self, **kwargs):
		context = super(UserDetailView, self).get_context_data(**kwargs)
		context['page_title'] = _('USERS')
		context['title'] = _('User detail')
		context['user_active'] = 'active'
		context['progress'] = self.get_profile_completion()

		return context

	def get_profile_completion(self):
		"""
		This function is used to calculate the total percentage of the user's profile completion.
		:return: the calculated percentage
		"""
		user = self.get_object()
		filled_fields = 0
		total_fields = len(user._meta.fields)

		for field in user._meta.fields:
			if getattr(user, field.name):
				filled_fields += 1

		progression = floor((filled_fields / total_fields) * 100)

		return progression


class UserAddView(LoginRequiredMixin, CreateView):
	"""
	View that is used to add a new user in the Chronos platform.
	TODO: Develop this view
	"""

	model = User
	form_class = UserForm
	template_name = 'user/user_form.html'

	def get_context_data(self, **kwargs):
		context = super(UserAddView, self).get_context_data(**kwargs)
		context['page_title'] = _('USERS')
		context['title'] = _('Add new user')
		context['title'] = _('Add a new user')
		context['user_active'] = 'active'
		context['user_list'] = self.get_queryset()
		context['is_new_user'] = True
		context['help_text'] = password_validators_help_texts()

		return context

	def form_valid(self, form):
		return super(UserAddView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('user:index', kwargs={'result': 'YWRkZWQ='})


class UserEditView(LoginRequiredMixin, UpdateView):
	"""
	View that is used to edit an user in the Chronos platform.
	TODO: Develop this view
	"""

	model = User
	form_class = UserForm
	template_name = 'user/user_form.html'

	def get_context_data(self, **kwargs):
		context = super(UserEditView, self).get_context_data(**kwargs)
		context['page_title'] = _('USERS')
		context['title'] = _('Edit user')
		context['user_active'] = 'active'
		context['is_new_user'] = False
		context['help_text'] = password_validators_help_texts()

		return context

	def form_valid(self, form):
		return super(UserEditView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('user:index', kwargs={'result': 'ZWRpdGVk'})


class UserDeleteView(LoginRequiredMixin, DeleteView):
	"""
	View that is used to delete an user in the Chronos platform. Accessed via AJAX call
	TODO: Develop this view
	"""
	model = User
	template_name = 'user/user_delete_modal.html'

	def dispatch(self, *args, **kwargs):

		response = super(UserDeleteView, self).dispatch(*args, **kwargs)
		if self.request.is_ajax():
			response_data = {"result": "ok"}
			return JsonResponse(response_data)
		else:
			# POST request (not ajax) will do a redirect to success_url
			return response

	def get_success_url(self):
		return reverse_lazy('user:index', kwargs={'result': 'ZGVsZXRlZA=='})
