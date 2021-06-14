from django.db.models.functions.datetime import ExtractDay
from django.shortcuts import redirect, render, get_object_or_404
from .models import Task
from django.contrib.auth.models import User
from django.db.models.functions import ExtractMonth, ExtractYear
import datetime, calendar
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
import pytz

TZ = pytz.timezone('Asia/Dhaka')

@login_required(login_url='login')
def home_view(request):
    today = datetime.datetime.now(TZ)

    month_data_points = {} 
    for i in range(12):
        date = today - relativedelta(months=i)
        day, month, year = date.day, date.month, date.year
        num_of_done = Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, is_done=True).count()
        num_of_undone = Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, is_done=False).count()
        month_data_points[(year, month)] = [num_of_done, num_of_undone]
    
    day_data_points = {} 
    for i in range(30):
        date = today - datetime.timedelta(days=i)
        day, month, year = date.day, date.month, date.year
        num_of_done = Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, date_created__day=day, is_done=True).count()
        num_of_undone = Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, date_created__day=day, is_done=False).count()
        day_data_points[(year, month, day)] = [num_of_done, num_of_undone]

    done = Task.objects.filter(author=request.user, is_done=True).count()
    undone = Task.objects.filter(author=request.user, is_done=False).count()

    return render(request, 'tasks/home.html', {'done':done,'undone':undone, 
                                               'day_data_points':day_data_points, 
                                               'month_data_points':month_data_points})

@login_required(login_url='login')
def months_view(request):
    def month_str(i):
        return calendar.month_name[i]
    tasks = Task.objects.filter(author=request.user)
    years = tasks.annotate(year=ExtractYear('date_created')).values_list('year', flat=True).distinct()
    years = sorted(years, reverse=True)
    month_dict = {}
    for x in years:
        months = Task.objects.filter(author=request.user, date_created__year = x).annotate(month=ExtractMonth('date_created')).values_list('month', flat=True).distinct()
        months = sorted(months, reverse=True)
        strs = map(month_str, months)
        final_months = zip(months, strs)
        month_dict[x] = final_months
    return render(request, 'tasks/months.html', {'months':month_dict})

@login_required(login_url='login')
def month_view(request, year, month):
    days = Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month).annotate(day=ExtractDay('date_created')).values_list('day')
    days = sorted(days, reverse=True)
    year = int(year)
    month = int(month)
    tasks_dict = {}
    for day_query in days:
        day = day_query[0]
        tasks = Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, date_created__day=day)
        done = Task.objects.filter(author=request.user, is_done=True, date_created__year=year, date_created__month=month, date_created__day=day).count()/Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, date_created__day=day).count()
        tasks_dict[datetime.date(year,month,day)] = tasks, round(done*100,1), day
    return render(request, 'tasks/month.html', {'days':tasks_dict})

@login_required(login_url='login')
def day_view(request,year, month,  day):
    tasks = Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, date_created__day=day)
    done = Task.objects.filter(author=request.user, is_done=True, date_created__year=year, date_created__month=month, date_created__day=day).count()/Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, date_created__day=day).count()
    return render(request,  'tasks/specific_day.html', {'done': round(100*done,1), 'tasks':tasks})

@login_required(login_url='login')
def add_task(request):
    if request.method == 'POST':
        new_task = Task(description=request.POST['description'],
                        author=request.user)
        new_task.save()
    return redirect('today')

@login_required(login_url='login')
def today_view(request):
    year = datetime.datetime.now(TZ).year
    month = datetime.datetime.now(TZ).month
    day = datetime.datetime.now(TZ).day
    tasks = Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, date_created__day=day).order_by('-date_created')
    try:    
        done = Task.objects.filter(author=request.user, is_done=True, date_created__year=year, date_created__month=month, date_created__day=day).count()/Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, date_created__day=day).count()
    except:
        done = 0
    return render(request,  'tasks/today.html', {'done': round(100*done,1), 'tasks':tasks})

@login_required(login_url='login')
def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    if request.user == task.author:
        task.delete()
    return redirect('today')

@login_required(login_url='login')
def mark_done(request, pk):
    task = Task.objects.get(pk=pk)
    if request.user == task.author:
        task.is_done = True
        task.save()
    return redirect('today')

@login_required(login_url='login')
def bring_back_to_today(request, pk):
    task = Task.objects.get(pk=pk)
    if request.user == task.author:
        task.date_created = datetime.datetime.now()
        task.save()
    return redirect('today')
    

