from __future__ import unicode_literals

import hashlib

def gen_MD5_of_UploadedFile(file):
    m = hashlib.md5()
    while True:
        data = file.read()
        if not data:
            return m.hexdigest()
        m.update(data)

def message_judge_func(message, request):
    return message.creator == request.user

def get_display_message_list(message_set, user):
    display_message_list = []
    for message in message_set:
        project_info = message.project_info
        display_message = {}
        # text
        display_message['title'] = message.title
        display_message['description'] = message.description
        display_message['project_name'] = project_info.name
        display_message['project_info_id'] = project_info.id
        # files
        file_list = []
        display_message['file_info_list'] = file_list
        for file_info in message.file_info.all():
            display_file_info = {}
            display_file_info['id'] = file_info.id
            display_file_info['name'] = file_info.file_name
            display_file_info['downloadable'] = judge_downloadable(file_info,
                                                                   project_info,
                                                                   user)
            file_list.append(display_file_info)
        display_message_list.append(display_message)
    return display_message_list


def judge_downloadable(file_info, project_info, user):
    require_perm = [file_info.READ, file_info.READ_AND_WRITE]
    # super group perm
    for group_info in project_info.super_group.all():
        if group_info.group.user_set.filter(username=user.username):
        # user in super group, return all perm
            return True
    # owner perm
    if file_info.owner == user:
        # user's owner, return file's owner_perm
        if file_info.owner_perm in require_perm:
            return True
        return False
    # group perm
    has_intersection = False
    for group_info in project_info.normal_group.all():
        user_set = group_info.group.user_set
        if user_set.filter(username=file_info.owner.username) \
                and user_set.filter(username=user.username):
            # file's owner and user in the same group
            group_perm = file_info.group_perm
            # Notice that the perm of multi-group is the lowest perm
            # among the perm of groups.
            if group_perm not in require_perm:
                return False
            # mark intersection
            has_intersection = True
    if has_intersection:
        return True 
    # everyone's perm
    if file_info.everyone_perm in require_perm:
        return True
    return False


