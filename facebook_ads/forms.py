from django.utils.translation import ugettext as _
from django import forms
from models import AdAccount

class StatisticImportForm(forms.Form):
    account = forms.CharField(label=_('Account'), widget=forms.Select())
    csv  = forms.FileField(label=_('CSV file with facebook statistic'))

    def __init__(self, *args, **kwargs):
        super(StatisticImportForm, self).__init__(*args, **kwargs)
        self.fields['account'].widget.choices = [(account.account_id, account) for account in AdAccount.objects.all()]