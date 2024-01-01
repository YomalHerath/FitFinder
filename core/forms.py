from django import forms
from core.models import ProductReview, ThreadComment, UploadedImage

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


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']



class StyleForm(forms.Form):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    AGE_RANGE_CHOICES = [('16-25', '16-25'), ('26-35', '26-35'), ('36-45', '36-45'), ('46-55', '46-55'), ('56-65', '56-65')]

    # Updated to include all colors
    FAVORITE_COLOR_CHOICES = [
        ('Red', 'Red'), ('Blue', 'Blue'), ('Green', 'Green'), ('Black', 'Black'), 
        ('White', 'White'), ('Yellow', 'Yellow'), ('Pink', 'Pink'), ('Gray', 'Gray'), 
        ('Purple', 'Purple'), ('Orange', 'Orange'), ('Brown', 'Brown'), ('Teal', 'Teal'), 
        ('Maroon', 'Maroon'), ('Cyan', 'Cyan'), ('Magenta', 'Magenta'), ('Lime', 'Lime'), 
        ('Indigo', 'Indigo'), ('Violet', 'Violet')
    ]

    SEASON_CHOICES = [('Spring', 'Spring'), ('Summer', 'Summer'), ('Autumn', 'Autumn'), ('Winter', 'Winter')]
    OCCASION_CHOICES = [('Casual', 'Casual'), ('Formal', 'Formal'), ('Party', 'Party'), ('Sport', 'Sport')]
    CLOTHING_TYPE_CHOICES = [('T-shirt', 'T-shirt'), ('Shirt', 'Shirt'), ('Jeans', 'Jeans'), ('Trousers', 'Trousers'), ('Dress', 'Dress'), ('Skirt', 'Skirt'), ('Jacket', 'Jacket')]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    age_range = forms.ChoiceField(choices=AGE_RANGE_CHOICES)
    favorite_color = forms.ChoiceField(choices=FAVORITE_COLOR_CHOICES)
    season = forms.ChoiceField(choices=SEASON_CHOICES)
    occasion = forms.ChoiceField(choices=OCCASION_CHOICES)
    clothing_type = forms.ChoiceField(choices=CLOTHING_TYPE_CHOICES)
