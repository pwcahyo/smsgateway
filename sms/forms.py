from django import forms
from dal import autocomplete
from .models import Person, Job, Major, NextMajor, School, Parent, Outbox, Graduate, MessageStatus

class SendSMSForm(forms.ModelForm):
	class Meta:
		model = Outbox
		fields = ['person', 'text', 'school', 'major', 'graduate']

	def __init__(self, *args, **kwargs):
		super(SendSMSForm, self).__init__(*args, **kwargs)
		self.fields['person'].label = '* Nama'
		self.fields['school'].label = '** Sekolah'
		self.fields['major'].label = '** Jurusan'
		self.fields['graduate'].label = '** Tahun Lulus'
		self.fields['text'].label = 'Pesan SMS'
		self.fields['person'].required = False
		self.fields['school'].required = False
		self.fields['major'].required = False
		self.fields['graduate'].required = False
		self.fields['text'].required = True

