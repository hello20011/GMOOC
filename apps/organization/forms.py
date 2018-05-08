from django.forms import ModelForm, forms

from operation.models import UserAsk

import re


class UserAskForm(ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        rc = re.compile(r"^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$")
        if rc.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号非法', code='mobile_invalid')