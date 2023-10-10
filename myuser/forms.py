from django.forms import ModelForm


class EmployeeForm(ModelForm):

    class Meta:
        model = ModelForm
        fields = ('department',)
