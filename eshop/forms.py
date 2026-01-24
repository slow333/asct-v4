from django import forms

class AddProductForm(forms.Form):
    quantity = forms.IntegerField(
        label='수량',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 50,
            'step': 1,
            'style': 'width: 80px; text-align: center;'
        })
    )
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)