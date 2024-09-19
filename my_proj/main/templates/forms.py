from django import forms
from main.models import Service, Appointment, Client, Employee

class AddReviewForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя', widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
    phone = forms.CharField(max_length=20, label='Ваш номер телефона', widget=forms.TextInput(attrs={'placeholder': 'Ваш номер телефона'}))
    review = forms.CharField(max_length=Appointment.REVIEW_MAX_LENGTH, widget=forms.Textarea(attrs={'placeholder': 'Ваш отзыв'}))
    image = forms.ImageField(label="Фото", required=False)

class AddServiceModelForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'duration', 'price')

class CustomAppointmentForm(forms.Form):
    client_name = forms.CharField(label='Имя клиента', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
    client_phone = forms.CharField(label='Номер телефона', max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Ваш номер телефона'}))
    client_email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'Ваш email'}))
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), label='Выберите мастера')
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='Выберите услугу')
    appointment_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label='Дата и время')
    