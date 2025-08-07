from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Excel Dosyası',
        help_text='Sadece .xlsx veya .xls dosyaları kabul edilir.',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        })
    )
    
    def clean_excel_file(self):
        file = self.cleaned_data['excel_file']
        if file:
            if not file.name.endswith(('.xlsx', '.xls')):
                raise forms.ValidationError('Sadece Excel dosyaları (.xlsx, .xls) yükleyebilirsiniz.')
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError('Dosya boyutu 10MB\'dan küçük olmalıdır.')
        return file
