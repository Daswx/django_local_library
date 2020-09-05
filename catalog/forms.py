import datetime
from django import forms
from catalog.models import BookInstance, Book
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy


class RenewBookForm(forms.Form):
	
	renewal_date = forms.DateField(help_text='Enter a valid date')

	def clean_renewal_date(self):
		data = self.cleaned_data['renewal_date']

		if data < datetime.date.today():
			raise ValidationError(ugettext_lazy('Invalid date - renewal in past'))
		
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(ugettext_lazy('Invalid date - renewal more than 4 weeks ahead'))

		return data



class RenewBookModelForm(forms.ModelForm):

	def clean_due_back(self):
		data = self.cleaned_data['due_back']

		if data < datetime.date.today():
			raise ValidationError(ugettext_lazy('Invalid date - renewal in past'))

		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(ugettext_lazy('Invalid date - renewal more than 4 weeks ahead'))

		return data

	class Meta:
		model = BookInstance
		fields = ['due_back']
		labels = {'due_back': ugettext_lazy('Renewal date')}
		help_texts = {'due_back': ugettext_lazy('Enter a date between now and 4 weeks (default 3).')}




class CreateBookModelForm(forms.ModelForm):
	class meta:
		model = Book
		fields = '__all__'
