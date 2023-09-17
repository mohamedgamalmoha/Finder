from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.backends import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin
from django.views.generic.detail import BaseDetailView
from django.views.generic.base import TemplateResponseMixin, TemplateView

from djoser import utils

from .forms import ActivationForm, ResetUsernameForm, ResetPasswordForm


User = get_user_model()


class SuccessView(TemplateView):
    template_name = 'account/success.html'


class BaseUidAndTokenFormView(TemplateResponseMixin, SuccessMessageMixin, FormMixin, BaseDetailView):
    template_name = 'account/rest.html'
    form_class = None
    success_url = reverse_lazy('success')
    success_message: str

    def get_object(self, queryset=None):
        uid_parm = self.kwargs['uid']
        uid = utils.decode_uid(uid_parm)
        return get_object_or_404(User, pk=uid)

    def get_initial(self):
        initial = super().get_initial()
        initial['uid'] = self.kwargs['uid']
        initial['token'] = self.kwargs['token']
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class ActivationView(BaseUidAndTokenFormView):
    form_class = ActivationForm
    success_message = _('Activation is done')
    extra_context = {
        'title': _('Activate Email'),
        'action': _('Activate')
    }


class ResetUsernameView(BaseUidAndTokenFormView):
    form_class = ResetUsernameForm
    success_message = _('Successfully email is reset')
    extra_context = {
        'title': _('Reset Email'),
        'action': _('Reset')
    }


class ResetPasswordView(BaseUidAndTokenFormView):
    form_class = ResetPasswordForm
    success_message = _('Successfully password is reset')
    extra_context = {
        'title': _('Reset Password'),
        'action': _('Reset')
    }
