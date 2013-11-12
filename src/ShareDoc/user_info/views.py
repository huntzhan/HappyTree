from __future__ import unicode_literals
# django dependency
from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
# auth dependency
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required_or_403
from guardian.decorators import permission_required
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm
from guardian.shortcuts import get_users_with_perms
from guardian.shortcuts import get_objects_for_user
# model
from guardian.models import User
from guardian.models import Group
from user_info.models import UserInfo
from real_group.models import RealGroup 
# form
# decorator
from django.utils.decorators import method_decorator
# util
# python library
import operator
import re


class HomePage(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomePage, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request,
                      'user_info/home.html')
                      
    def post(self, request):
        project_set = get_objects_for_user(request.user,
                                           'project.project_membership')
        message_set = []
        for project in project_set:
            message_set.extend(project.messages.filter(post_flag=True))
        message_set = sorted(
            message_set,
            key=lambda x: x.post_time,
            reverse=True
        )

        return render(request,
                      'message/message_list.html',
                      {'message_set': message_set})


class UserPage(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserPage, self).dispatch(*args, **kwargs)

    def get(self, request, user_info_id):
        user_info = get_object_or_404(UserInfo, id=int(user_info_id))
        return render(request,
                      'user_info/user_page.html',
                      {'user_info': user_info})

    def _handler_factory(self, request):
        if 'load_message_list' in request.POST:
            return self._message_list_handler

    def _message_list_handler(self, request, user_info):
        message_set = user_info.messages.filter(post_flag=True)
        message_set = sorted(
            message_set,
            key=lambda x: x.post_time,
            reverse=True
        )

        return render(request,
                      'message/message_list.html',
                      {'message_set': message_set})

    def post(self, request, user_info_id):
        user_info = get_object_or_404(UserInfo, id=int(user_info_id))
        handler = self._handler_factory(request)
        return handler(request, user_info)
