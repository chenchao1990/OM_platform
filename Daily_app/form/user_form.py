#!/usr/bin/env python
# _*_coding:utf-8 _*_

from django import forms


class UserInfo(forms.Form):

    username = forms.CharField(error_messages={'required': u"用户名不能为空"},
                               widget=forms.TextInput(attrs={'placeholder': u'username',
                                                             }

                                                  ),

                               )
    password = forms.CharField(error_messages={'required': u"密码不能为空"},
                               widget=forms.PasswordInput(attrs={'placeholder': u'password',
                                                                 }
                                                  ),
                               )

