from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name
class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()  # В минутах
    price = models.DecimalField(max_digits=10, decimal_places=2)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('completed', 'Выполнено'),
        ('canceled', 'Отменено'),
    ]
   
    REVIEW_MAX_LENGTH = 350

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    # поля для отзыва и фотографии
    review = models.TextField(null=True, blank=True, max_length=REVIEW_MAX_LENGTH)  
    image = models.ImageField(upload_to='uploads', null=True, blank=True)  

    def __str__(self):
        return f"{self.client} - {self.service} - {self.appointment_date}"