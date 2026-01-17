from django import forms
from django.utils.safestring import mark_safe
from .models import Venue, Event, Favorite
from django.contrib.auth.models import User

class VenueFormAdmin(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'), 
        required=True, 
        label=mark_safe('<span style="display: inline-block; font-size: 1rem; margin: 10px; color: green;">장소 주인</span>'), 
        empty_label='장소 주인 선택',
        widget=forms.Select(attrs={
            'class': 'form-select', 'placeholder': '장소 주인 선택'}))
    class Meta:
        model = Venue
        fields = ['name', 'address', 'web', 'owner', 'venue_image']
        labels = {
            'name': '',
            'address': '',
            'web': '',
            'venue_image': '',
        }
    def __init__(self, *args, **kwargs):
        super(VenueFormAdmin, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].widget.attrs.update({'placeholder': f'{field.replace("_", " ").capitalize()}'})

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'web', 'venue_image']
        labels = {
            'name': '',
            'address': '',
            'web': '',
            'venue_image': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '장소 이름' }),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '주소' }),
            'web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': '웹사이트' }),
        }

    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
class VenueChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} ({obj.event_set.count()})" # type: ignore

class AttendeeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} ({obj.id})" # type: ignore
    
class EventFormAdmin(forms.ModelForm):
    venue = VenueChoiceField(
        queryset=Venue.objects.all().order_by('name'), 
        required=False, 
        label='', 
        empty_label='장소 선택',
        widget=forms.Select(attrs={
            'class': 'form-select', 'placeholder': '장소 선택'}))
    manager = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'), 
        required=False, 
        label='관리자',
        empty_label='관리자 선택',
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': '관리자 선택'}))
    attendees = AttendeeChoiceField(
        queryset=Favorite.objects.all().order_by('-name'), 
        required=False, 
        label =mark_safe('<span style="display: inline-block; font-size: 1rem; margin: 10px; color:red;">참석자</span>'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}))

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date','end_date', 'is_completed', 'venue', 'manager', 'attendees']
        labels = {
            'title': '',
            'start_date': '시작일시',
            'end_date': '종료일시',
            'is_completed': '',
            'description': '',
            'venue': '이벤트 장소',
            'attendees': '참석자',
            'manager': '관리자',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이벤트 이름' }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '이벤트 설명', 'required': 'false', 'rows': '3'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local','required': 'true'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 10px;font-size: 1.2rem;'}),
        }

class EventForm(forms.ModelForm):
    venue = VenueChoiceField(
        queryset=Venue.objects.all().order_by('name'), 
        required=False, 
        label='', 
        empty_label='장소 선택',
        widget=forms.Select(attrs={
            'class': 'form-select', 'placeholder': '장소 선택'}))
    attendees = AttendeeChoiceField(
        queryset=Favorite.objects.all().order_by('-name'), 
        required=False, 
        label =mark_safe('<span style="display: inline-block; font-size: 1rem; margin: 10px; color:red;">참석자</span>'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}))

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date','end_date', 'is_completed','venue', 'attendees']
        labels = {
            'title': '',
            'description': '',
            'start_date': '시작일시',
            'end_date': '종료일시',
            'is_completed': '',
            'venue': '이벤트 장소',
            'attendees': '참석자',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '이벤트 이름' }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '이벤트 설명', 'required': 'false', 'rows': '3'}),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 10px;font-size: 1.2rem;'}),
        }

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['name', 'description', 'image']
        labels = {
            'name': '',
            'description': '',
            'image': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름',}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '설명', 'rows': '2'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': '이미지',}),
        }