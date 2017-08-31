from datetime import datetime
from math import floor

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from apps.camera.forms import CameraForm
from apps.camera.models import Camera

"""
Camera views created to manage the camera CRUD operation.
"""


class CameraIndexView(LoginRequiredMixin, ListView):
    """
    View that is used to show all the cameras that exist in the Video Monitor platform.
    Receives optional parameters to show alert functions:
    @param result (optional) - Shows alert functions accordingly

        Camera added - YWRkZWQ=
        Camera edited - ZWRpdGVk
        Camera deleted - ZGVsZXRlZA==

    TODO: Develop this view
    """

    template_name = 'camera/camera_index.html'
    model = Camera

    def get_alert_information(self):
        """
        Function used to generate the alert string based on the return result by URL
        :return: String containing the result message
        """
        if 'result' in self.kwargs:
            if self.kwargs['result'] == 'YWRkZWQ=':
                return _("A new camera was added with success!")
            if self.kwargs['result'] == 'ZWRpdGVk':
                return _("The camera information was edited with success!")
            if self.kwargs['result'] == 'ZGVsZXRlZA==':
                return _("The camera information was deleted with success!")

    def get_context_data(self, **kwargs):
        context = super(CameraIndexView, self).get_context_data(**kwargs)
        context['page_title'] = _('WEBCAMS')
        context['title'] = _('Webcam list')
        context['camera_active'] = 'active'
        context['result'] = self.get_alert_information()

        return context


class CameraDetailView(LoginRequiredMixin, DetailView):
    """
    View that is used to show the camera information that exists in the Video Monitor platform.
    TODO: Develop this view
    """

    template_name = "camera/camera_base.html"
    model = Camera

    def get_context_data(self, **kwargs):
        context = super(CameraDetailView, self).get_context_data(**kwargs)
        context['page_title'] = _('WEBCAMS')
        context['title'] = _('Webcam detail view')
        context['camera_active'] = 'active'
        context['progress'] = self.get_profile_completion()

        return context

    def get_profile_completion(self):
        """
        This function is used to calculate the total percentage of the camera's profile completion.
        :return: the calculated percentage
        """
        camera = self.get_object()
        filled_fields = 0
        total_fields = len(camera._meta.fields)

        for field in camera._meta.fields:
            if getattr(camera, field.name):
                filled_fields += 1

        progression = floor((filled_fields / total_fields) * 100)

        return progression


class CameraAddView(LoginRequiredMixin, CreateView):
    """
    View that is used to add a new camera in the Video Monitor platform.
    TODO: Develop this view
    """

    model = Camera
    form_class = CameraForm
    template_name = 'camera/camera_form.html'

    def get_context_data(self, **kwargs):
        context = super(CameraAddView, self).get_context_data(**kwargs)
        context['page_title'] = _('WEBCAMS')
        context['title'] = _('Add a new webcam')
        context['camera_active'] = 'active'
        context['is_new_camera'] = True

        return context

    def form_valid(self, form):
        return super(CameraAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('camera:index', kwargs={'result': 'YWRkZWQ='})


class CameraEditView(LoginRequiredMixin, UpdateView):
    """
    View that is used to edit a camera in the Video Monitor platform.
    TODO: Develop this view
    """

    model = Camera
    form_class = CameraForm
    template_name = 'camera/camera_form.html'

    def get_context_data(self, **kwargs):
        context = super(CameraEditView, self).get_context_data(**kwargs)
        context['page_title'] = _('WEBCAMS')
        context['title'] = _('Edit webcam')
        context['camera_active'] = 'active '
        context['is_new_camera'] = False

        return context

    def form_valid(self, form):
        form.instance.last_updated = datetime.now()
        return super(CameraEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('camera:index', kwargs={'result': 'ZWRpdGVk'})


class CameraDeleteView(LoginRequiredMixin, DeleteView):
    """
    View that is used to delete a camera in the Video Monitor platform. Accessed via AJAX call
    TODO: Develop this view
    """
    model = Camera
    template_name = 'camera/camera_delete_modal.html'

    def dispatch(self, *args, **kwargs):

        id = self.get_object().id

        response = super(CameraDeleteView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok", "id": id}
            return JsonResponse(response_data)
        else:
            # POST request (not ajax) will do a redirect to success_url
            return response

    def get_success_url(self):
        return reverse_lazy('camera:index', kwargs={'result': 'ZGVsZXRlZA=='})
