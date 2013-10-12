from __future__ import unicode_literals
# Create your views here.

# remember, always include project info id.

from .forms import FileUploadForm, PermChoiceForm, MessageInfoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from project_info.models import ProjectInfo, Message
from file_info.models import FileInfo, UniqueFile

from .utils import gen_MD5_of_UploadedFile, message_judge_func, \
                   judge_downloadable, get_display_message_list

from prototype.decorators import require_user_in
from prototype.utils import extract_from_GET, url_with_querystring
from project_info.utils import judge_func as project_judge_func

from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper



@login_required
@require_user_in(
        project_judge_func,
        'project_info_id', 
        (ProjectInfo, True, ('normal_group',))
)
def create_message(request, project_info_id, message_id):
    project_info_id = int(project_info_id)
    project_info = get_object_or_404(ProjectInfo, id=project_info_id)
    if message_id == None:
        # create_message
        message = Message(project_info=project_info,
                          creator=request.user)
        message.save()
        return redirect('create_message_page',
                        project_info_id=project_info_id,
                        message_id=message.id)
    else:
        message_id = int(message_id)
        message = get_object_or_404(Message, 
                                    project_info=project_info,
                                    id=message_id)
    
    # process form
    if request.method == 'POST':
        file_upload_form = FileUploadForm(request.POST, request.FILES)
        perm_choice_form = PermChoiceForm(request.POST)
        message_info_form = MessageInfoForm(request.POST)

        if message_info_form.is_valid():
            message.title = message_info_form.cleaned_data['title']
            message.description = message_info_form.cleaned_data['description']
            message.post_flag = True
            message.save()
            
            # redirect to somewhere

        if file_upload_form.is_valid() and perm_choice_form.is_valid():
            uploaded_file = request.FILES['uploaded_file']
            owner_perm = perm_choice_form.cleaned_data['owner_perm']
            group_perm = perm_choice_form.cleaned_data['group_perm']
            everyone_perm = perm_choice_form.cleaned_data['everyone_perm']

            # check unique
            md5 = gen_MD5_of_UploadedFile(uploaded_file)
            unique_file = UniqueFile.objects.filter(md5=md5)
            if not unique_file:
                unique_file = UniqueFile(md5=md5)
                unique_file.save()
                unique_file.file.save(md5, uploaded_file)
            else:
                unique_file = unique_file[0]
            # save file info
            file_info = FileInfo(file_name=uploaded_file.name,
                                 owner_perm=owner_perm,
                                 group_perm=group_perm,
                                 everyone_perm=everyone_perm,
                                 unique_file=unique_file)
            file_info.save()
            file_info.owner.add(request.user)

            message.file_info.add(file_info)
        return redirect('create_message_page',
                        project_info_id=project_info_id,
                        message_id=message.id)
    else:
        file_upload_form = FileUploadForm()
        perm_choice_form = PermChoiceForm(initial={
                    'owner_perm': FileInfo.READ_AND_WRITE, 
                    'everyone_perm': FileInfo.READ, 
                    'group_perm': FileInfo.READ
                    })
        message_info_form = MessageInfoForm()

    # rendering
    # generate uploaded file list

    # notice that file_name could be duplicate,
    # so it can not be the key for dict.
    display_file_info = {file_info.id: file_info.file_name\
                                for file_info in message.file_info.all()}
    render_data_dict = {
            'project_info_id': int(project_info_id),
            'file_upload_form': file_upload_form,
            'perm_choice_form': perm_choice_form,
            'post_message_form': message_info_form,
            'message_id': message.id,
            'file_info_list': display_file_info,
    }
    return render(request,
                  'file_info/create_message_page.html',
                  render_data_dict)


@login_required
@require_user_in(
        message_judge_func,
        'message_id', 
        (Message, True, (None,))
)
def delete_file_from_message(
        request, project_info_id, message_id,
        file_info_id):
    project_info_id = int(project_info_id)
    message_id = int(message_id)
    file_info_id = int(file_info_id)
    message = get_object_or_404(Message, id=message_id)
    file_info = get_object_or_404(message.file_info, id=file_info_id)

    # once a ForeignKey is delete, 
    # its related entity will remove the link as well.
    file_info.delete()

    # judge to remove unique file
    unique_file = file_info.unique_file
    if unique_file.fileinfo_set.count() == 0:
        unique_file.delete()

    return redirect('create_message_page',
                    project_info_id=project_info_id,
                    message_id=message.id)

@login_required
@require_user_in(
        project_judge_func,
        'project_info_id', 
        (ProjectInfo, True, ('normal_group',))
)
def show_project_related_message(request, project_info_id):
    project_info_id = int(project_info_id)
    project_info = get_object_or_404(ProjectInfo, id=project_info_id)
    # extract message
    display_message_list = get_display_message_list(
                                project_info.message_set.filter(post_flag=True),
                                request.user)
    render_data_dict = {
            'message_list': display_message_list,
            'project_info_id': project_info_id,
            'project_name': project_info.name,
            'project_description': project_info.project_description,
    }
    return render(request,
                  'file_info/project_related_message_page.html',
                  render_data_dict)

# for content type detection
from django.utils.http import urlencode
import os
import mimetypes
mimetypes.init()
# 
@login_required
@require_user_in(
        project_judge_func,
        'project_info_id', 
        (ProjectInfo, True, ('normal_group',))
)
def download_file(request,
                  project_info_id,
                  file_info_id):
    project_info_id = int(project_info_id)
    file_info_id = int(file_info_id)
    project_info = get_object_or_404(ProjectInfo, id=project_info_id)
    file_info = get_object_or_404(FileInfo, id=file_info_id)
    if judge_downloadable(file_info,
                          project_info,
                          request.user):
        unique_file = file_info.unique_file
        file_wrapper = FileWrapper(unique_file.file)
        # get content type
        # ugly code
        # http://blog.robotshell.org/2012/deal-with-http-header-encoding-for-file-download/
        file_name = file_info.file_name
        encode_file_name = urlencode(((file_name, ''),)).rstrip('=')

        content_type = os.path.splitext(file_name)[-1]
        content_type = mimetypes.types_map.get(content_type,
                                               'application/octet-stream')
        response = HttpResponse(file_wrapper, 
                                content_type=content_type)
        response['Content-Disposition'] = \
                        "attachment; filename={0}; filename*=utf-8''{0}".format(encode_file_name)
        response['Content-Length'] = unique_file.file.size
        return response
    else:
        raise Http404
        



