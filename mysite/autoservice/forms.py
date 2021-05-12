from .models import OrderComment
from django import forms


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ('content', 'order', 'user',)
        widgets = {'order': forms.HiddenInput(), 'user': forms.HiddenInput()}