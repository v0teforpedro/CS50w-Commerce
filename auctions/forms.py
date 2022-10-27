from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Submit

from django import forms

from .models import Bid, Category, Listing


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


class BidCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.add_layout(FieldWithButtons(
            Field('amount', placeholder='Make your bid...', step='0.25'),
            Submit('bid', 'Place Bid', css_class='btn-secondary'),
            input_size="input-group",
        ))

    class Meta:
        model = Bid
        fields = (
            'amount',
        )
        # labels = {
        #     'amount': ''
        # }
        # widgets = {
        #     'amount': forms.NumberInput(attrs={
        #         'step': 0.25,
        #         'class': 'form-control',
        #         'placeholder': 'Make your bid...',
        #         'aria-describedby': 'button-addon2',
        #         'aria-label': 'Make your bid...',
        #     }),
        # }
