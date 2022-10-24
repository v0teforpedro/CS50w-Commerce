from django import forms

from .models import Listing, Category


class ListingCreateForm(forms.ModelForm):
    # This is how you can disable field via init
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     var = self.fields['created_by']
    #     var.disabled = True

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Listing
        fields = (
            'name',
            'start_price',
            'image',
            'categories',
            'description',
        )
        widgets = {
            'categories': forms.Textarea(attrs={'rows': 5, 'cols': 10}),
            'start_price': forms.NumberInput(attrs={'step': 0.25}),
        }

        exclude = ['is_active', 'created_by']
