# coding:utf-8
from django import template

register = template.Library()


@register.filter
def get_group_name(user):
    '''
          获得用户的组名
    '''
    groups = user.groups.all()
    group = groups[0]
    return english_to_chinese(group.name)


@register.filter
def english_to_chinese(input_str):
    '''
          英译汉
    '''
    my_dict = {'admin': '管理员', 'normal': '普通用户', 'audit': '审计员'}
    return my_dict[input_str]
