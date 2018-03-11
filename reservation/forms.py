# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import validate_email, RegexValidator
from models import *

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
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    name = forms.CharField(label=u'姓名:' , required=True, widget=forms.TextInput(attrs={'placeholder': u'請輸入姓名','class':'form-control'}))
    email = forms.EmailField(label=u'電子信箱:', required=True, validators=[validate_email],  widget=forms.TextInput(attrs={'placeholder': u'請輸入電子信箱','class':'form-control','type':'email'}))
    phone = forms.CharField(label=u'電話:', required=True, validators=[phone_regex],  widget=forms.TextInput(attrs={'placeholder': u'請輸入電話號碼','class':'form-control'}))
    address = forms.ChoiceField(label=u'居住地:',  choices=county, widget=forms.Select(attrs={'placeholder': u'請選擇居住地','class':'form-control'}))
    
    
class ServicesTypeCreateForm(forms.ModelForm):
    
    class Meta:
        model = ServicesType
        fields = '__all__'
        widgets = {
                'service_title' : forms.TextInput(attrs={'type':'text','class':'form-control','id':'classname', 'aria-describedby':'class2','placeholder':u'課程名稱'}),
                'service_description' : forms.Textarea(attrs={'type':'text' , 'class':'form-control froala-editor' ,'id':'classinfo'}),
                'session_time_length' : forms.NumberInput(attrs={'type':'text','class':'form-control','id':'classcost'}),
                'service_fee' : forms.NumberInput(attrs={'type':'text','class':'form-control','id':'classcost', 'placeholder':u'請設定課程費用'}),
                'service_type_image' : forms.FileInput(attrs={'type':'file','class':'form-control-file btn btn-outline-secondary','id':'classimg','aria-describedby':'classimg'}),
                'service_note' : forms.TextInput(attrs={'type':'text','class':'form-control','id':'classname', 'aria-describedby':'class2','placeholder':u'課程Note'}),
                'service_code' : forms.TextInput(attrs={'type':'text','class':'form-control','id':'classname', 'aria-describedby':'class2','placeholder':u'請設定課程代碼'})
            }
    
'''
class CustomersType(models.Model):
    
    customers_type_image = models.ImageField(upload_to='customers_type_image')
    customer_title = models.CharField(max_length=255)
    customer_description = models.CharField(max_length=1024)
    #session_time_lenth = models.DecimalField(max_digits=4 , decimal_places=2, validators=[MinValueValidator(0.0) , MaxValueValidator(9.0)])
    customer_code = models.CharField(max_length=5)
    available_service = models.ManyToManyField(ServicesType)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        #s = u''.join( (self.customer_code + '-' + self.customer_title.encode('ascii',errors='replace')))
    #return s.encode('utf-8').strip()
       return self.customer_code + '-' + self.customer_title
'''     
        
class CustomersTypeForm(forms.ModelForm):
    
    class Meta:
        model = CustomersType
        fields = '__all__'
        widgets = {
                'customer_title' : forms.TextInput(attrs={'type':'text','class':'form-control','id':'customName', 'aria-describedby':'class2','placeholder':u'客群名稱'}),
                'customer_description' : forms.Textarea(attrs={'type':'text' , 'class':'form-control froala-editor' ,'id':'customInfo' , 'placeholder':u'請輸入說明描述'}),
                'customers_type_image' : forms.FileInput(attrs={'type':'file','class':'form-control-file','id':'customImage','aria-describedby':'customImage'}),
                'customer_code' : forms.TextInput(attrs={'type':'text','class':'form-control','id':'customCode', 'aria-describedby':'customCode','placeholder':u'請設定客群代碼'}),
                'available_service' : forms.SelectMultiple(attrs={'class': 'form-control', 'id':'customServices'}),
                'active' : forms.CheckboxInput(attrs={'type':'checkbox','class':'form-check-input ml-1' , 'id':'customEnable'})
            }
        
        
        
class TimeSlotAdminForm(forms.ModelForm):
    
    class Meta:
        model = TimeSlot
        exclude = ['date','end_time','remain_mainpower']
        widgets={
                #'date': forms.DateInput(attrs={'class':'datepicker form-control col-12'}),
                'start_time':forms.TimeInput(attrs={'class':'form-control col-12'}),
                #'end_time':forms.TimeInput(attrs={'class':'form-control col-12'}),
                'available_manpower' : forms.NumberInput(attrs={'class':'form-control col-12'}),
                #'remain_mainpower':forms.NumberInput(attrs={'class':'form-control col-12'}),
                'capacity':forms.NumberInput(attrs={'class':'form-control col-12'}),
                'active':forms.CheckboxInput(attrs={'type':'checkbox','class':'form-check-input' , 'id':'customEnable'})
            }
        
        
        
        
        
        
        
        
