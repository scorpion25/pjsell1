from django import forms

class UploadExcelForm(forms.Form):  # ✅ com "Form", no singular
    arquivo = forms.FileField(label='Selecione um arquivo Excel')
