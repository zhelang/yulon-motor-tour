# -*- coding: utf-8 -*-
from django import forms
from models import FAQ, SiteInfo, SEO
from ckeditor.widgets import CKEditorWidget

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
    
    banner_image = forms.ImageField(label=u'選擇圖檔', required = True) 
    banner_description = forms.CharField(label=u'描述說明' , required = True)
    banner_url = forms.URLField(label=u'網址' , required = False)
    
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
                   'img':forms.FileInput(attrs={'class':'form-control-file btn btn-outline-secondary','id':'thumbnail'}),
                   'type':forms.TextInput(attrs={'class':'form-control'})
                   }
    
    
class FAQAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(FAQAdminForm, self).__init__(*args, **kwargs)
        self.fields['answer'].widget = CKEditorWidget()
    class Meta:
        model = FAQ
        fields = '__all__'
        
    
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
        
    
        
