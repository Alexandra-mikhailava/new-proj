from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import Client, Employee, Service, Appointment
from main.templates.forms import AddReviewForm, AddServiceModelForm, CustomAppointmentForm

def home(request):
    review_form = AddReviewForm()
    appointment_form = CustomAppointmentForm()
    success_message = None

    if request.method == 'POST':
        # Обработка формы отзыва
        if 'submit_review' in request.POST:
            review_form = AddReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                name = review_form.cleaned_data['name']
                phone_number = review_form.cleaned_data['phone']
                try:
                    client = Client.objects.get(name=name, phone_number=phone_number)
                    # Поиск последнего завершенного приема для этого клиента
                    appointment = Appointment.objects.filter(client=client, status='completed').order_by('-appointment_date').first()
                    if appointment:
                        appointment.review = review_form.cleaned_data['review']
                        if review_form.cleaned_data.get('image'):
                            appointment.image = review_form.cleaned_data['image']
                        appointment.save()
                        return redirect('home')
                    else:
                        review_form.add_error(None, 'Нет завершенных приемов для данного клиента.')
                except Client.DoesNotExist:
                    review_form.add_error('name', 'Клиент с указанными именем и номером телефона не найден.')

        # Обработка формы записи
        if 'submit_add_appointment' in request.POST:
            appointment_form = CustomAppointmentForm(request.POST)
            if appointment_form.is_valid():
                # Получаем или создаем клиента
                client_name = appointment_form.cleaned_data['client_name']
                client_phone = appointment_form.cleaned_data['client_phone']
                client_email = appointment_form.cleaned_data['client_email']

                client, created = Client.objects.get_or_create(
                    name=client_name,
                    phone_number=client_phone,
                    defaults={'email': client_email}
                )

                # Создаем новый Appointment
                appointment = Appointment(
                    client=client,
                    employee=appointment_form.cleaned_data['employee'],
                    service=appointment_form.cleaned_data['service'],
                    appointment_date=appointment_form.cleaned_data['appointment_date'],
                    status='planned'
                )
                appointment.save()
                success_message = "Ваша запись добавлена"  # Сообщение после добавления
                appointment_form = CustomAppointmentForm()  # Очищаем форму после успешного сохранения

    context = {
        'review_form': review_form,
        'appointment_form': appointment_form,
        'success_message': success_message,
    }

    return render(request, 'home_page.html', context)

def services_list(request):
    services = Service.objects.all()
    # Получить просмотренные услуги из сессии
    viewed_services = request.session.get('viewed_services', [])

    # Создать список кортежей (услуга, форма для редактирования этой услуги)
    service_forms = [(service, AddServiceModelForm(instance=service)) for service in services]
    
    # Инициализация форм и сообщений
    add_form = AddServiceModelForm()
    appointment_form = CustomAppointmentForm()
    success_message = None

    # Обработка POST-запросов
    if request.method == 'POST':
        # Проверить, добавляется ли новая услуга
        if 'submit_add_service' in request.POST:
            add_form = AddServiceModelForm(request.POST)
            if add_form.is_valid():
                new_service = add_form.save(commit=False)
                new_service.employee = Employee.objects.first()  # Связать с первым сотрудником
                new_service.save()
                return redirect('services_list')

        # Проверить, обновляется ли существующая услуга
        for service, form in service_forms:
            if f'submit_edit_service_{service.id}' in request.POST:
                form = AddServiceModelForm(request.POST, instance=service)
                if form.is_valid():
                    form.save()
                    return redirect('services_list')

        # Проверить, добавляется ли новая запись (Appointment)
        if 'submit_add_appointment' in request.POST:
            appointment_form = CustomAppointmentForm(request.POST)
            if appointment_form.is_valid():
                client_name = appointment_form.cleaned_data['client_name']
                client_phone = appointment_form.cleaned_data['client_phone']
                client_email = appointment_form.cleaned_data['client_email']

                client, created = Client.objects.get_or_create(
                    name=client_name,
                    phone_number=client_phone,
                    defaults={'email': client_email}
                )

                appointment = Appointment(
                    client=client,
                    employee=appointment_form.cleaned_data['employee'],
                    service=appointment_form.cleaned_data['service'],
                    appointment_date=appointment_form.cleaned_data['appointment_date'],
                    status='planned'
                )
                appointment.save()
                success_message = "Ваша запись добавлена"  # Сообщение об успешной записи
                appointment_form = CustomAppointmentForm()  # Очищаем форму после успешного сохранения

    context = {
        'services': services,
        'add_form': add_form,
        'service_forms': service_forms,
        'viewed_services': viewed_services,  # Передаем просмотренные услуги
        'appointment_form': appointment_form,
        'success_message': success_message,
    }
    
    return render(request, 'all_services.html', context)

def add_service(request):
    if request.method == 'POST':
        form = AddServiceModelForm(request.POST, request.FILES)
        if form.is_valid():
            service_entry = form.save(commit=False)
            service_entry.employee = request.user.employee
            service_entry.save()
            form.save_m2m()
            return redirect('services_list')
    else:
        form = AddServiceModelForm()
    
    return render(request, 'all_services.html', {'form': form})

def service_detail(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        # Получить список просмотренных услуг из сессии
        viewed_services = request.session.get('viewed_services', [])

        # Добавить текущий ID услуги, если он еще не в списке
        if service_id not in viewed_services:
            viewed_services.append(service_id)
            request.session['viewed_services'] = viewed_services  # Сохранить обратно в сессию

    except Service.DoesNotExist:
        return HttpResponseNotFound(f"Услуга с кодом {service_id} не найдена")

    return render(request, 'service_page.html', {'service_obj': service})

def add_appointment(request):
    form = CustomAppointmentForm()
    message = None

    if request.method == 'POST':
        form = CustomAppointmentForm(request.POST)
        if form.is_valid():
            client_name = form.cleaned_data['client_name']
            client_phone = form.cleaned_data['client_phone']
            client_email = form.cleaned_data['client_email']

            client, created = Client.objects.get_or_create(
                name=client_name,
                phone_number=client_phone,
                defaults={'email': client_email}
            )

            appointment = Appointment(
                client=client,
                employee=form.cleaned_data['employee'],
                service=form.cleaned_data['service'],
                appointment_date=form.cleaned_data['appointment_date'],
                status='planned'
            )
            appointment.save()
            form = CustomAppointmentForm()
            message = "Ваша запись добавлена"

    return render(request, 'add_appointment.html', {'form': form, 'message': message})

def contacts(request):
    return HttpResponse("test.html")
