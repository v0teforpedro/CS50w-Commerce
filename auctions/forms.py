from django import forms

from .models import Listing


class ListingCreateForm(forms.ModelForm):
    # This is how you can disable field via init
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     var = self.fields['created_by']
    #     var.disabled = True
    #     var.visible = False

    class Meta:
        model = Listing
        fields = '__all__'

        exclude = ['is_active', 'created_by']
