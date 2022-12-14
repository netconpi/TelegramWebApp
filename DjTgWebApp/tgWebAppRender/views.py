from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.conf import settings
import requests
import datetime
from . import base_logic 

from .models import *
import datetime


# Working 

def send_telegram(chat_id, message):
    token = settings.TG_TOKEN
    # chat_id = update.message.chat_id
    url_req = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    results = requests.get(url_req)
    res = results.json()
    return res

def view_lk(request):
    tg_id = request.GET.get('tg_id')
    userapp = UserApp.objects.filter(telegram_id=tg_id)
    try:
        return render(request, 'tgWebAppRender/client_self_lk.html', context={'company': userapp[0]})
    except Exception as e:
        return render(request, 'tgWebAppRender/client_self_lk.html', context={'company': ''})

def executor_lk(request):
    tg_id = request.GET.get('tg_id')
    company = Company.objects.filter(telegram_id=tg_id)
    try:
        return render(request, 'tgWebAppRender/executor_lk.html', context={'company': company[0]})
    except Exception as e:
        return render(request, 'tgWebAppRender/executor_lk.html', context={'company': ''})

def basic_registration(request):
    data = {
        'telegram_id': request.POST.get('telegram_id'),
        'name': request.POST.get('name'),
        'description': request.POST.get('description'),
        'whatsapp': request.POST.get('whatsapp'),
        'email': request.POST.get('email'),
    }

    print(f'Basic reg: {data}')

    if request.method == "POST":

        r_context = {
            'error': 'Не все поля заполнены. Обратите внимание на поле: не получен телеграм-id! Напишите @ntcad'
        }

        # Useless additional check
        if data['name'] != '':
            not_fild = []
            for k, v in data.items():
                if v == '':
                    not_fild.append(k)

            if len(not_fild) == 0:
                new_user = UserApp(
                    telegram_id = data['telegram_id'],
                    name = data['name'],
                    description = data['description'],
                    email = data['email'],
                    whatsapp = data['whatsapp'],
                )

                try:
                    new_user.save()
                    send_telegram(data['telegram_id'], f"Поздравляю! Твой аккаунт успешно создан. Приятного использования")
                except Exception as e:
                    send_telegram(data['telegram_id'], f"Произошла ошибка, отправь @ntcad: {e}")
                    r_context['close'] = 1
                    return render(request, 'tgWebAppRender/user_registration.html', context=r_context)

            else:
                r_context['error'] = 'Вы не заполнили поля: \n'
                for i in not_fild:
                    r_context['error'] += f'- {i}\n'
                return render(request, 'tgWebAppRender/user_registration.html', context=r_context)

            return render(request, 'tgWebAppRender/user_registration.html', context={'close': True})
        else:
            return render(request, 'tgWebAppRender/user_registration.html', context=r_context)

    else:
        return render(request, 'tgWebAppRender/user_registration.html', context={'error': 'Обратите внимание на то, что все поля являются обязательными'})

def add_company(request):
    # print(request.POST)
    data = {
        'telegram_id': request.POST.get('telegram_id'),
    	'name': request.POST.get('name'),
    	'description': request.POST.get('description'),
    	'work_time': request.POST.getlist('work_time'),
    	'meet_timing': request.POST.get('meet_timing'),
    	'meet_timing_end': request.POST.get('meet_timing_end'),
    	'duration': request.POST.get('duration'),
    	'whatsapp': request.POST.get('whatsapp'),
    	'meeting_link':  request.POST.get('meeting_link'),
    	'skype': request.POST.get('skype'),
    	'tg_link': request.POST.get('tg_link'),
    	'email': request.POST.get('email'),
    	'password_unsafe':request.POST.get('password_unsafe'),
        'password_confirm_unsafe': request.POST.get('password_confirm_unsafe'),
    }

    not_filed = []
    for name, value in data.items():
        if value:
            pass
        else:
            not_filed.append(name)

    if len(not_filed) == len(data):
        return render(request, 'tgWebAppRender/add-company.html', context={})
    elif len(not_filed) >= 1:
        return render(request, 'tgWebAppRender/add-company.html', context={'not_filed': not_filed, 'data': data})
    else:
        new_company = Company(
            telegram_id=data['telegram_id'],
            name=data['name'],
            description=data['description'],
            work_time=data['work_time'],
            meet_timing=data['meet_timing'],
            meet_timing_end=data['meet_timing_end'],
            duration=data['duration'],
            email=data['email'],
            whatsapp=data['whatsapp'],
            meeting_link=data['meeting_link'],
            skype=data['skype'],
            tg_link=data['tg_link'],
            password_unsafe=data['password_unsafe'],
            password_confirm_unsafe=data['password_confirm_unsafe'],
        )
        try: 
            new_company.save()
            send_telegram(data['telegram_id'], f"🚀 Мы получили данные: {data['name']}, вы стали исполнителем!")
            return render(request, 'tgWebAppRender/add-company.html', context={'close': 1})

        except Exception as e:
            send_telegram(data['telegram_id'], f"{e}")


        return render(request, 'tgWebAppRender/add-company.html', context={'not_filed': not_filed, 'data': data})
        
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
        send_telegram(form.cleaned_data['telegram_id'], f"Мы получили данные: {form.cleaned_data['name']}, вы стали исполнителем!")
        return super(AddCompany, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        
def calendartasklist(request):
    # main render logic 
    # Trash moment 
    tg_id = request.GET.get('tg_id')
    date = request.GET.get('date')

    if date != None:
        events = Event.objects.filter(event_date__date=date)
    else:
        events = []

    return render(request, 'tgWebAppRender/calendar-task-list.html', {'date': date, 'events': events})

def create_event(request):

    if request.method == "POST":
        return render(request, 'tgWebAppRender/404.html', context={'notificat': request})
    else:
        tg_id = request.GET.get('tg_id')
        action = request.GET.get('action')
        edit_mode = request.GET.get('edit_mode')
        event_id = request.GET.get('event_id')
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
        tags = Tag.objects.filter(created_by__telegram_id = tg_id)
        print(tags)
        if not data['telegram_id']:
            return render(request, 'tgWebAppRender/create_event.html', context={'tags': tags})
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
                tmp_date_holder = data['date'].split('/')
                if len(tmp_date_holder) < 2:
                    return render(request, 'tgWebAppRender/create_event.html', context={'warn': 1, 'tags': tags})
                date_to_datetime = tmp_date_holder[2] + "-" + tmp_date_holder[1] + "-" + tmp_date_holder[0]
                del tmp_date_holder
                tag_id = request.GET.get('tag_id')
                if tag_id != '':
                    tag_object = Tag.objects.get(id=tag_id)
                else:
                    tag_object = None

                if not edit_mode:
                    event = Event(
                        company_link = Company.objects.get(telegram_id=data['telegram_id']),
                        created_by = data['telegram_id'],
                        name = data['company_name'],
                        description = data['company_description'],
                        meet_timing = f"{data['date']} {data['time_start']} {data['time_end']}",
                        event_date = f"{date_to_datetime} {data['time_start']}:00.000 +0300",
                        tag = tag_object
                    )
                    event.save()
                    send_telegram(data['telegram_id'], f"✅ Событие: {data['company_name']} -- было добавлено! ")
                    return render(request, 'tgWebAppRender/create_event.html', context={'close': 1})
                elif edit_mode == 'edit_mode':
                    print(event_id)
                    existing_event = Event.objects.filter(pk=event_id)
                    existing_event.update(
                        name=data['company_name'],
                        description = data['company_description'],
                        meet_timing = f"{data['date']} {data['time_start']} {data['time_end']}",
                        event_date = f"{date_to_datetime} {data['time_start']}:00.000 +0300",
                        tag = tag_object
                    )
                    send_telegram(data['telegram_id'], f"✏️ Событие: {data['company_name']} -- было отредактировано! ")
                    return render(request, 'tgWebAppRender/create_event.html', context={'close': 1})

            else:
                if not action:
                    return render(request, 'tgWebAppRender/create_event.html', context={'warn': 1, 'tags': tags})
                elif action == 'edit':
                    event_to_return = Event.objects.get(id=request.GET.get('event_id'))
                    return render(request, 'tgWebAppRender/create_event.html', context={'event': event_to_return})
                elif action == 'remove':
                    event_to_remove = Event.objects.filter(pk=event_id)
                    tg_id_event = event_to_remove[0].created_by
                    event_name = event_to_remove[0].name
                    event_to_remove.delete()
                    send_telegram(tg_id_event, f"🚫 Событие: {event_name} -- было удалено! ")
                    return render(request, 'tgWebAppRender/create_event.html', context={'close': 1})
                else:
                    return render(request, 'tgWebAppRender/404.html', context={})

def notifications(request):
    # main render logic 
    tg_id = request.GET.get('tg_id')
    notifications = Notification.objects.filter(to_user=tg_id)
    try:
        return render(request, 'tgWebAppRender/notifications.html', context={'notifications': notifications})
    except Exception as e:
        return render(request, 'tgWebAppRender/notifications.html', context={'notifications': ''})

class NotFound(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/404.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/404.html', context)

def display_event(request):
    print(request.method)

    if request.method == 'GET':

        tg_id = request.GET.get('telegram_id')
        event_id = request.GET.get('event_id')

        information_event = Event.objects.get(id=event_id)
        date_list = information_event.meet_timing.split()
        date_object = datetime.datetime.strptime(f'{date_list[0]} {date_list[1]}', '%d/%m/%Y %H:%M')

        # Maybe None, just need to check it 
        try:
            tag_name = information_event.tag.name
            tag_color = information_event.tag.color
        except Exception as e:
            tag_name = 'Не установлена'
            tag_color = 'grey'

        # User attending generation
        output_users_list = 'Произошла ошибка во время выполнения запроса '
        try:
            users_list = information_event.user_attached.all()
            user_len = len(users_list)
            output_users_list = ''

            for i in range(user_len):
                if user_len-1 != i:
                    output_users_list += f'{users_list[i].name}, '
                else:
                    output_users_list += f'{users_list[i].name}'

        except Exception as e:
            pass

        context = {
            'event': {
                'event_id': event_id,
                'telegram_id': tg_id,
                'name': information_event.name,
                'link_method': information_event.link_method,
                'descript': information_event.description,
                'day': f"{base_logic.dates_name[date_object.strftime('%A')]}, {date_list[1]}-{date_list[2]}",
                'attending': output_users_list,
                'category': tag_name,
                'categoty_color': tag_color,
            },
        }

        return render(request, 'tgWebAppRender/event_details.html', context)
    else:
        return render(request, 'tgWebAppRender/404.html', {})

def shared_list(request):
    # main render logic 
    tg_id = request.GET.get('tg_id')
    shared_companys = SharedCalendar.objects.filter(shared_with__telegram_id=tg_id)
    try:
        return render(request, 'tgWebAppRender/shared.html', context={'shared': shared_companys})
    except Exception as e:
        return render(request, 'tgWebAppRender/shared.html', context={'shared': ''})

def lk_shared(request):
    # Getting information form REQUEST 
    user_id = request.GET.get('user_id')
    owner_id = request.GET.get('owner_id')
    company = Company.objects.filter(telegram_id=owner_id)

    # Dates for record
    day = {
        0: '',
        1: '',
        2: '',
    }
    availability = {
        0: [],
        1: [],
        2: [],
    }
    # Working days list. Example [1, 2, 3]
    # Where 1 - Monday and etc
    working_days = base_logic.convert_strlist2list(
        company[0].work_time
    )
    # Getting UTC time + 3 hours to MSK time
    # Remove this if you will edit dajngo prj settings
    now_time = datetime.datetime.now() + datetime.timedelta(hours=3)
    # timestep, in registration field. need to count
    time_step = company[0].duration[:2]
    # Dates datetime-objects
    work_time_start = datetime.datetime.strptime(
        f"{now_time.strftime('%d/%m/%Y')} {company[0].meet_timing}", 
        '%d/%m/%Y %H:%M'
    )
    w_tm_bcup = [
        int(work_time_start.strftime("%H")),
        int(work_time_start.strftime("%M"))
    ]
    work_time_end = datetime.datetime.strptime(
        f"{now_time.strftime('%d/%m/%Y')} {company[0].meet_timing_end}", 
        '%d/%m/%Y %H:%M'
    )

    for i in range(3):

        while not base_logic.is_working_weekday(now_time, working_days):
            print('change')
            now_time += datetime.timedelta(days=1)
            work_time_start += datetime.timedelta(days=1)
            work_time_end += datetime.timedelta(days=1)
        day[i] = base_logic.dates_name[now_time.strftime('%A')]

        while work_time_start < work_time_end:
            previous = work_time_start
            work_time_start += datetime.timedelta(
                minutes=int(time_step)
            )
            nexx = work_time_start

            if (work_time_start >= now_time 
                    and now_time <= work_time_end):
                have_event = Event.objects.filter(
                    company_link=company[0],
                    event_date__year=now_time.strftime('%Y'),
                    event_date__month=now_time.strftime('%m'),
                    event_date__day=now_time.strftime('%d'),
                )

                if have_event:
                    print('no event')
                    for event in have_event:
                        event_time_start_obj = datetime.datetime.strptime(
                            f"{now_time.strftime('%d/%m/%Y')} {event.time_start}", 
                            '%d/%m/%Y %H:%M'
                        ) 
                        event_time_end_obj = datetime.datetime.strptime(
                            f"{now_time.strftime('%d/%m/%Y')} {event.time_end}", 
                            '%d/%m/%Y %H:%M'
                        ) 

                        if (event_time_start_obj <= previous 
                                and event_time_end_obj >= nexx):
                            pass
                        else:
                            availability[i].append(
                                f"{previous.strftime('%H:%M')} - {nexx.strftime('%H:%M')}"
                            )
                else:
                    availability[i].append(f"{previous.strftime('%H:%M')} - {nexx.strftime('%H:%M')}")

        now_time = now_time.replace(hour=00, minute=00)
        now_time += datetime.timedelta(days=1)
        work_time_start += datetime.timedelta(days=1)
        work_time_end += datetime.timedelta(days=1)
        work_time_start = work_time_start.replace(
            hour=w_tm_bcup[0], 
            minute=w_tm_bcup[1]
        )

    context_local = {'company': company[0], 'free': availability, 'day': day}

    try:
        return render(request, 'tgWebAppRender/client-profile.html', context=context_local)
    except Exception as e:
        return render(request, 'tgWebAppRender/client-profile.html', context={'company': ''})

# Pending

class ClientProfile(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/client-profile.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/client-profile.html', context)

class LkSubscribed(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/lk-subscribed.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/lk-subscribed.html', context)

class SubscribeChoose(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/subscribe-choose.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/subscribe-choose.html', context)

# Not used

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

# Technical 

class index(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/index.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/index.html', context)

class Components(View):
    # main render logic 
    def get(self, request):
        context = {}
        return render(request, 'tgWebAppRender/components.html', context) 
    # logic if i will need update page for actions
    def post(self, request):
        context = {}
        return render(request, 'tgWebAppRender/components.html', context)
