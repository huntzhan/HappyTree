from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from user_status.models import UserInfo
from project_info.models import ProjectInfo
from group_info.models import GroupInfo

from .forms import ProjectNameHandlerForm, ProjectDescriptionHandlerForm


@login_required
def show_project_list(request):
    group_set = request.user.groups.all()
    group_info_set = [group.groupinfo for group in group_set]
    
    display_project_act_as_normaluser = {}
    display_project_act_as_manager = {} 
    for group_info in group_info_set:
        for project in group_info.normal_in_project.all():
            display_project_act_as_normaluser[project.id] = project.name
        
        for project in group_info.super_in_project.all():
            display_project_act_as_manager[project.id] = project.name

    # rendering
    render_data_dict = {
            'display_project_act_as_manager': display_project_act_as_manager,
            'display_project_act_as_normaluser': display_project_act_as_normaluser
    }
    return render(request,
                  'project_info/project_list_page.html',
                  render_data_dict) 

@login_required
def show_project_page(request, project_info_id):

    pass


@login_required
def create_project(request):
    if request.method == 'POST':
        form_project_name = ProjectNameHandlerForm(request.POST)
        form_project_description = ProjectDescriptionHandlerForm(request.POST)
        if form_project_name.is_valid() and form_project_description.is_valid():
            # create project info
            project_name = form_project_name.cleaned_data['project_name']
            project_description = \
                    form_project_description.cleaned_data['project_description']
            project_info = ProjectInfo(name=project_name,
                                       project_description=project_description)
            project_info.save()
            
            # create manager group and default group
            # manager group is for project management.
            # default group is for adding user individually.
            # create groups
            super_group_name = '[system][super_group][{0}][{1}]'.format(
                                            str(project_info.id), 
                                            str(request.user.id))
            default_group_name = '[system][normal_group][{0}][{1}]'.format(
                                            str(project_info.id), 
                                            str(request.user.id))
            super_group = Group(name=super_group_name)
            default_group = Group(name=default_group_name)
            super_group.save()
            default_group.save()
            # create relate group_infos
            super_group_info = GroupInfo(group=super_group,
                                         real_group=False)
            default_group_info = GroupInfo(group=default_group,
                                           real_group=False)
            super_group_info.save()
            default_group_info.save()
            # make connections
            # add user to super_group info manager
            super_group_info.manager_user.add(request.user)
            default_group_info.manager_user.add(request.user)
            # relate user to group
            request.user.groups.add(super_group)
            request.user.groups.add(default_group)

            # add super_group info to project info
            project_info.super_group.add(super_group_info)
            project_info.default_group.add(default_group_info)
            return redirect('project_page',
                             project_info_id=project_info.id)
    else:
        form_project_name = ProjectNameHandlerForm()
        form_project_description = ProjectDescriptionHandlerForm()

    #rendering
    render_data_dict= {
        'form_project_name': form_project_name,
        'form_project_description': form_project_description,
    }
    return render(request,
                  'project_info/create_project_page.html',
                  render_data_dict)
