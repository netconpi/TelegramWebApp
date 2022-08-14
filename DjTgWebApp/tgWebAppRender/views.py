from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.conf import settings
import requests

from .models import *
import datetime


def send_telegram(chat_id, message):
    token = settings.TG_TOKEN
    # chat_id = update.message.chat_id
    url_req = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    results = requests.get(url_req)
    res = results.json()
    return res


class AddCompany(CreateView):
    model = Company
    fields = [
        'telegram_id',
    	'name', 
    	'description', 
    	'work_time', 
    	'meet_timing', 
    	'meet_timing_end', 
    	'duration', 
    	'whatsapp', 
    	'meeting_link', 
    	'skype',
    	'tg_link',
    	'email',
    	'password_unsafe',
    ]
    success_url = reverse_lazy('add-company')
    template_name = 'tgWebAppRender/add-company.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        send_telegram(form.cleaned_data['telegram_id'], f"Ваш аккаунт был создан! Поздравляем. Наименование аккаунта: {form.cleaned_data['name']}")
        return super(AddCompany, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        
class LoginHome(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/login-home.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/login-home.html', context)

class LoginIn(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/login-in.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/login-in.html', context)

class CalendarTaskList(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/calendar-task-list.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/calendar-task-list.html', context)

def create_event(request):

    if request.method == "POST":
        return render(request, 'tgWebAppRender/404.html', context={'notifications': request})
    else:
        tg_id = request.GET.get('tg_id')
        # Form custom validation
        data = {
            'telegram_id': request.GET.get('telegram_id'),
            'company_name': request.GET.get('company_name'),
            'company_description': request.GET.get('company_description'),
            'date': request.GET.get('date'),
            'time_start': request.GET.get('time_start'),
            'time_end': request.GET.get('time_end'),
            'reminder': request.GET.get('reminder'),
            'category': request.GET.get('category'),
        }
        if not data['telegram_id']:
            return render(request, 'tgWebAppRender/create_event.html', context={'notifications': request})
        else:
            important = 0
            if data['company_name'] != None and data['company_name'] != '':
                important += 1
            if data['company_description'] != None and data['company_description'] != '':
                important += 1
            if data['date'] != None and data['date'] != '':
                important += 1
            if data['time_start'] != None and data['time_start'] != '':
                important += 1
            if data['time_end'] != None and data['time_end'] != '':
                important += 1

            if important == 5: 
                event = Event(
                    created_by = data['telegram_id'],
                    name = data['company_name'],
                    description = data['company_description'],
                    meet_timing = f"{data['date']} {data['time_start']} {data['time_end']}",
                )
                event.save()
                send_telegram(data['telegram_id'], f"Событие: {data['company_name']} -- было добавлено! ")
                return render(request, 'tgWebAppRender/create_event.html', context={'close': 1})
            else:
                return render(request, 'tgWebAppRender/create_event.html', context={'warn': 1})
            


class CardAdd(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/card-add.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/card-add.html', context)

class CardChoose(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/card-choose.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/card-choose.html', context)

class ClientFreeTimes(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/client-free-times.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/client-free-times.html', context)

class ClientProfile(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/client-profile.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/client-profile.html', context)

class Components(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/components.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/components.html', context)

class index(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/index.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/index.html', context)

class LkSubscribed(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/lk-subscribed.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/lk-subscribed.html', context)

def lk(request):
    tg_id = request.GET.get('tg_id')
    company = Company.objects.filter(telegram_id=tg_id)
    try:
        return render(request, 'tgWebAppRender/client-profile.html', context={'company': company[0]})
    except Exception as e:
        return render(request, 'tgWebAppRender/client-profile.html', context={'company': ''})

def notifications(request):
    # main render logic 
    tg_id = request.GET.get('tg_id')
    notifications = Notification.objects.filter(to_user=tg_id)
    try:
        return render(request, 'tgWebAppRender/notifications.html', context={'notifications': notifications})
    except Exception as e:
        return render(request, 'tgWebAppRender/notifications.html', context={'notifications': ''})

class SubscribeChoose(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/subscribe-choose.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/subscribe-choose.html', context)

class NotFound(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/404.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/404.html', context)
