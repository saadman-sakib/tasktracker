from django.db.models.functions.datetime import ExtractDay
from django.shortcuts import redirect, render, get_object_or_404
from .models import Task
from django.contrib.auth.models import User
from django.db.models.functions import ExtractMonth, ExtractYear
import datetime, calendar
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home_view(request):
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    month_list = []
    i = current_month
    j = i-12
    while i != j:
        x = i % 12 or 12
        month_list.append((current_year,x))
        i = i-1
        if i == 0:
            current_year -= 1
    data_points = {}
    for year, month in month_list:
        num_of_done = Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, is_done=True).count()
        num_of_undone = Task.objects.filter(author=request.user, date_created__year=year, date_created__month=month, is_done=False).count()
        data_points[(year,month)] = [num_of_done, num_of_undone]

    done = Task.objects.filter(author=request.user, is_done=True).count()
    undone = Task.objects.filter(author=request.user, is_done=False).count()

    return render(request, 'tasks/home.html', {'done':done,'undone':undone, 'data_points':data_points})

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
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
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
    

