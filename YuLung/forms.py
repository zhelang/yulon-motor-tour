# -*- coding: utf-8 -*-
from django import forms
from models import FAQ, SiteInfo, SEO, EmailTemplate
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm

class LoginForm(forms.Form):
    
    username = forms.CharField(label=u"Email" ,required = True, widget=forms.TextInput(attrs={'placeholder': u'請輸入 Email', 'class': 'form-control'}))
    password = forms.CharField(label=u"密碼",required = True, widget=forms.PasswordInput(attrs={'placeholder': u'請輸入密碼', 'class': 'form-control'}))

class RegisterForm(forms.Form):

    username = forms.EmailField(label=u"Email" ,required = True, widget=forms.TextInput(attrs={'placeholder': u'請輸入您的 Email', 'class': 'form-control'}))
    password = forms.CharField(label=u"密碼",required = True, widget=forms.PasswordInput(attrs={'placeholder': u'請輸入密碼', 'class': 'form-control'}))
    password_confirm = forms.CharField(label=u"確認密碼",required = True, widget=forms.PasswordInput(attrs={'placeholder': u'請再次輸入密碼', 'class': 'form-control'}))
    #name = forms.CharField(label=u"姓名", required = True, widget=forms.TextInput(attrs={'placeholder': u'請輸入您的姓名', 'class': 'form-control'}))
    #phone = forms.CharField(label=u"行動電話", required = True, widget=forms.TextInput(attrs={'placeholder': u'請輸入您的行動電話號碼', 'class': 'form-control'}))
 
class AdminLoginForm(forms.Form):
    
    username = forms.CharField(label=u"Email" ,required = True, widget=forms.TextInput(attrs={'placeholder': u'請輸入 Email',
                                                                                                      'class':'form-control',
                                                                                                   }))
    password = forms.CharField(label=u"密碼",required = True, widget=forms.PasswordInput(attrs={'placeholder': u'請輸入密碼',
                                                                                                'class':'form-control',
                                                                                                'type':'password'
                                                                                              }))
class BannerCreateForm(forms.Form):
    
    banner_image = forms.ImageField(label=u'選擇圖檔', required = True, widget=forms.FileInput(attrs={'class':'form-control-file'})) 
    banner_description = forms.CharField(label=u'描述說明' , required = True, widget=forms.TextInput(attrs={'class':'form-control p-input'}))
    banner_url = forms.URLField(label=u'網址' , required = False, widget=forms.TextInput(attrs={'class':'form-control p-input'}))
    
class SEOAdminForm(forms.ModelForm):
    
    def __init__(self,*args, **kwargs):
        super(SEOAdminForm,self).__init__(*args, **kwargs)
        self.fields['img'].required = False
    
    class Meta:
        model = SEO
        fields = '__all__'
        img = forms.FileField(required=False)
        widgets = {'title':forms.TextInput(attrs={'class':'form-control','type':'text','aria-describedby':'seotitle'}),
                   'url_address':forms.URLInput(attrs={'class':'form-control','type':'text','aria-describedby':'seourl'}),
                   'description':forms.TextInput(attrs={'class':'form-control','type':'text'}),
                   'img':forms.FileInput(attrs={'class':'form-control-file','id':'thumbnail'}),
                   'type':forms.TextInput(attrs={'class':'form-control'})
                   }
    
    
class FAQAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(FAQAdminForm, self).__init__(*args, **kwargs)
        self.fields['answer'].widget = CKEditorWidget(attrs={'class':'form-control ckeditor'})
    class Meta:
        model = FAQ
        fields = '__all__'
        widgets = {'question':forms.TextInput(attrs={'class':'form-control p-input'}),
                   'priority':forms.TextInput(attrs={'class':'form-control p-input'}),
                   'active':forms.CheckboxInput(attrs={'class':'form-check-input ml-1'})
                  }
        
    
class SiteInfoAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SiteInfoAdminForm, self).__init__(*args, **kwargs)
        self.fields['site_info_content'].widget = CKEditorWidget(attrs={'class':'ckeditor'})
        
    class Meta:
        model = SiteInfo
        fields = '__all__'
        widgets = {
                'email':forms.TextInput(attrs={'class':'form-control','type':'text'}),
                'phone':forms.TextInput(attrs={'class':'form-control','type':'text'}),
                'address':forms.TextInput(attrs={'class':'form-control','type':'text'}),
            }
        
    
class AdminUserCreateForm(forms.Form):
        
    first_name = forms.CharField(label="first name" , required=True , widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'first name', 'type':'text'}))
    last_name = forms.CharField(label="last name" , required=True , widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'last name', 'type':'text'}))
    username = forms.CharField(label="Username" ,required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type':'text', 'aria-describedby':"useraccount"}))
    password = forms.CharField(label="Password" , required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'aria-describedby':"password"}))
    email = forms.CharField(label="Email" , required=True, widget=forms.EmailInput(attrs={'class':'form-control','aria-describedby':"email"}))
        

class EmailTemplateForm(forms.ModelForm):
        
    class Meta:
        model = EmailTemplate
        fields = '__all__'
        widgets = {
            'from_email':forms.EmailInput(attrs={'class':'form-control'}),
            'subject':forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'email_content':forms.Textarea(attrs={'class':'form-control','type':'text'})
        }
        
class AdminPasswordResetForm(PasswordResetForm):
    
    email = email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class':'form-control','aria-describedby':"emailHelp"}))

class AdminSetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(label=u"請輸入密碼", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label=u"請再次輸入密碼", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

