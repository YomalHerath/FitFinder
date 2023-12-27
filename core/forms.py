from django import forms
from core.models import ProductReview, ThreadComment

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = ProductReview
        fields = ['review', 'rating'] 


class ThreadCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = ThreadComment
        fields = ['comment']