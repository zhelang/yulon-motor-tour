# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import validate_email, RegexValidator
from .models import (
    CustomersType,
    ServicesType,
    TimeSlot
)


class CustomerDetailsForm(forms.Form):
    county = [
        ('63', '臺北市'),
        ('65', '新北市'),
        ('10017', '基隆市'),
        ('68', '桃園市'),
        ('10018', '新竹市'),
        ('10004', '新竹縣'),
        ('10005', '苗栗縣'),
        ('66', '臺中市'),
        ('10007', '彰化縣'),
        ('10008', '南投縣'),
        ('10009', '雲林縣'),
        ('10020', '嘉義市'),
        ('10010', '嘉義縣'),
        ('67', '臺南市'),
        ('64', '高雄市'),
        ('10013', '屏東縣'),
        ('10002', '宜蘭縣'),
        ('10015', '花蓮縣'),
        ('10014', '臺東縣'),
        ('10016', '澎湖縣'),
        ('09007', '連江縣'),
        ('09020', '金門縣'),
    ]
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message='行動電話號碼格式必須是「0910123456」或「+886910123456」，請再次確認電話號碼。')
    name = forms.CharField(label='姓名:',
                           required=True,
                           widget=forms.TextInput(attrs={'placeholder': '請輸入姓名', 'class': 'form-control'}))
    email = forms.EmailField(label='電子信箱:',
                             required=True,
                             validators=[validate_email],
                             widget=forms.TextInput(attrs={'placeholder': '請輸入電子信箱',
                                                           'class': 'form-control',
                                                           'type': 'email'
                                                           }))
    phone = forms.CharField(label='行動電話:',
                            required=True,
                            validators=[phone_regex],
                            widget=forms.TextInput(attrs={'placeholder': '請輸入行動電話號碼', 'class': 'form-control'})
                            )
    phone2 = forms.CharField(label='其他聯絡電話:',
                             required=False,
                             widget=forms.TextInput(attrs={'placeholder': '請輸入其他聯絡電話號碼', 'class': 'form-control'})
                             )
    address = forms.ChoiceField(label='居住地:',
                                required=True,
                                choices=county,
                                widget=forms.Select(attrs={'placeholder': '請選擇居住地', 'class': 'form-control'})
                                )


class ServicesTypeCreateForm(forms.ModelForm):

    class Meta:
        model = ServicesType
        fields = '__all__'
        widgets = {
                'service_title': forms.TextInput(attrs={'type': 'text',
                                                        'class': 'form-control',
                                                        'id': 'classname',
                                                        'aria-describedby': 'class2',
                                                        'placeholder': '課程名稱'
                                                        }),
                'service_description': forms.Textarea(attrs={'type': 'text',
                                                             'class': 'form-control froala-editor',
                                                             'id': 'classinfo'
                                                             }),
                'session_time_length': forms.NumberInput(attrs={'type': 'text',
                                                                'class': 'form-control',
                                                                'id': 'classcost'
                                                                }),
                'service_fee': forms.NumberInput(attrs={'type': 'text',
                                                        'class': 'form-control',
                                                        'id': 'classcost',
                                                        'placeholder': '請設定課程費用'
                                                        }),
                'service_type_image': forms.FileInput(attrs={'type': 'file',
                                                             'class': 'form-control-file btn btn-outline-secondary',
                                                             'id': 'classimg',
                                                             'aria-describedby': 'classimg'
                                                             }),
                'service_note': forms.TextInput(attrs={'type': 'text',
                                                       'class': 'form-control',
                                                       'id': 'classname',
                                                       'aria-describedby': 'class2',
                                                       'placeholder': '備註'
                                                       }),
                'service_code': forms.TextInput(attrs={'type': 'text',
                                                       'class': 'form-control',
                                                       'id': 'classname',
                                                       'aria-describedby': 'class2',
                                                       'placeholder': '請設定課程代碼'
                                                       })
            }


class CustomersTypeForm(forms.ModelForm):

    class Meta:
        model = CustomersType
        fields = '__all__'
        widgets = {
                'customer_title': forms.TextInput(attrs={'type': 'text',
                                                         'class': 'form-control',
                                                         'id': 'customName',
                                                         'aria-describedby': 'class2',
                                                         'placeholder': '客群名稱'
                                                         }),
                'customer_description': forms.Textarea(attrs={'type': 'text',
                                                              'class': 'form-control froala-editor',
                                                              'id': 'customInfo',
                                                              'placeholder': '請輸入說明描述'
                                                              }),
                'customers_type_image': forms.FileInput(attrs={'type': 'file',
                                                               'class': 'form-control-file',
                                                               'id': 'customImage',
                                                               'aria-describedby': 'customImage'
                                                               }),
                'customer_code': forms.TextInput(attrs={'type': 'text',
                                                        'class': 'form-control',
                                                        'id': 'customCode',
                                                        'aria-describedby': 'customCode',
                                                        'placeholder': '請設定客群代碼'
                                                        }),
                'available_service': forms.SelectMultiple(attrs={'class': 'form-control',
                                                                 'id': 'customServices'
                                                                 }),
                'active': forms.CheckboxInput(attrs={'type': 'checkbox',
                                                     'class': 'form-check-input ml-1',
                                                     'id': 'customEnable'
                                                     })
            }


class TimeSlotAdminForm(forms.ModelForm):

    class Meta:
        model = TimeSlot
        exclude = ['date', 'end_time', 'remain_mainpower']
        widgets = {
                  'start_time': forms.TimeInput(attrs={'class': 'form-control col-12'}),
                  'available_manpower': forms.NumberInput(attrs={'class': 'form-control col-12'}),
                  'capacity': forms.NumberInput(attrs={'class': 'form-control col-12'}),
                  'active': forms.CheckboxInput(attrs={'type': 'checkbox',
                                                       'class': 'form-check-input',
                                                       'id': 'customEnable'
                                                       })
                  }
