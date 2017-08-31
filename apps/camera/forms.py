from django.forms import ModelForm

from apps.camera.models import Camera


class CameraForm(ModelForm):
    """
    Camera form used to add or update a camera in the Video Monitor platform.
    TODO: Develop this form
    """

    class Meta:
        model = Camera
        fields = ['name', 'description', 'comments', 'url', 'is_visible']
