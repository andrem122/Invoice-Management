from django import forms

class Send_Data(forms.Form):
    """Allows users to send data from a page at a certain frequency"""
    send_to  = forms.EmailField(label='Send To Email')
    message  = forms.CharField(required=False, label='Message', widget=forms.Textarea)
    approved = forms.BooleanField(required=False)
    rejected = forms.BooleanField(required=False)
    new      = forms.BooleanField(required=False)
    completed      = forms.BooleanField(required=False)


    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['send_to'].widget.attrs['placeholder'] = 'JonDoe@example.com'
        self.fields['message'].widget.attrs['placeholder'] = 'Write your message here...'
