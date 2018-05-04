from django import forms

class Send_Data(forms.Form):
    send_to = forms.EmailField(label='Send To Email')
    subject = forms.CharField(required=False, label='Subject')
    message = forms.CharField(required=False, label='Message', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(Send_Data, self).__init__(*args, **kwargs)
        self.fields['send_to'].widget.attrs['placeholder'] = 'JonDoe@example.com'
        self.fields['subject'].widget.attrs['placeholder'] = 'Write your subject here...'
        self.fields['message'].widget.attrs['placeholder'] = 'Write your message here...'
