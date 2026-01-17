from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue, Favorite
from .forms import VenueForm, EventForm, EventFormAdmin, VenueFormAdmin, FavoriteForm
from django.urls import reverse_lazy
import calendar
from django.contrib.auth.models import User
from django.http import HttpResponse

# 달력 만들기
from calendar import HTMLCalendar
from datetime import datetime
import calendar

# 이전 페이지로 이동하는 함수 ===========================================
def store_previous_page(request):
    if request.method == 'GET':
        referer = request.META.get('HTTP_REFERER')
        if referer and request.path not in referer:
            request.session['previous_page'] = referer

# 달력 만들기(일자 별로 event 표시) ===========================================
class EventsCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None, events=None):
        self.year = year
        self.month = month
        self.events = events
        super(EventsCalendar, self).__init__()

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday bg-light"></td>'

        events_html = ""
        if self.events:
            day_events = [t for t in self.events if t.start_date and t.start_date.day == day]
            for t in day_events:
                events_html += f'<div><a href="/apps/events/event_details/{t.id}" class="badge bg-primary text-white" style="font-size: 0.7rem; display: block; margin-bottom: 2px; {t.is_completed and 'text-decoration: line-through;' or 'text-decoration: none;'}">{t.title[:10]}...</a></div>'
        
        return f'<td class="{self.cssclasses[weekday]} border" style="height: 100px; vertical-align: top; width: 14.28%;"><div class="fw-bold mb-1">{day}</div>{events_html}</td>'

    def formatmonth(self, withyear=True):
        v = super().formatmonth(self.year, self.month, withyear) # type: ignore
        return v.replace('<table border="0" cellpadding="0" cellspacing="0" class="month">', '<table class="table table-bordered text-start">')

# 전체 달력과 일정 표시
def index(request, year=None, month=None):
    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month

    # Calendar setup
    queryset = Event.objects.filter(start_date__year=year, start_date__month=month)
    cal = EventsCalendar(year, month, queryset).formatmonth(withyear=True)
    queryset = queryset.order_by('start_date').order_by('is_completed')
    
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Previous/Next Month Calculation
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1

    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year = year + 1

    month_name = list(calendar.month_name)[month]
    time = datetime.now().strftime('%I:%M:%S %p')
    context = {'cal': cal, 'year': year, 'month': month, 
            'time': time, 'month_name': month_name,
            'page_obj': page_obj, 'today': datetime.today(),
            'prev_year': prev_year, 'prev_month': prev_month,
            'next_year': next_year, 'next_month': next_month,
    }
    return render(request, 'events/index.html', context )

# favorites 사진 ===========================================================
def favorites_list(request):
    favotrites = Favorite.objects.all().order_by('name')

    search_fatorites = request.GET.get('searched', '')
    if search_fatorites:
        favotrites = favotrites.filter(name__icontains=search_fatorites)
    
    pagenator = Paginator(favotrites, 8)
    page = request.GET.get('page')
    page_obj = pagenator.get_page(page)
    
    context = {
        'page_obj': page_obj,}
    return render(request, 'events/favorites_list.html', context)

def favorite_details(request, favorite_id):
    favorite = get_object_or_404(Favorite, pk=favorite_id)
    return render(request, 'events/favorite_details.html', {'favorite': favorite})

def favorite_update(request, favorite_id):
    if not request.user.is_authenticated:
        return redirect('login')
    favorite = Favorite.objects.get(pk=favorite_id)

    store_previous_page(request)

    form = FavoriteForm(request.POST or None, request.FILES or None, instance=favorite)
    if form.is_valid():
        form.save()
        return redirect(request.session.pop('previous_page', 'events:favorites-list'))
    return render(request, 'events/favorite_update.html', {'favorite': favorite, 'form': form})

def favorite_create(request):
    if request.method == 'POST':
        form = FavoriteForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('events:favorites-list')
    else:
        form = FavoriteForm()
    return render(request, 'events/favorite_create.html', {'form': form})

def favorite_delete(request, favorite_id):
    favorite = Favorite.objects.get(pk=favorite_id)
    if request.method == 'POST':
        favorite.delete()
        return redirect('events:favorites-list')

# venue ===========================================================
def venues_list(request):
    venues = Venue.objects.all().order_by('name')
    search_venue = request.GET.get('searched', '')
    
    if search_venue:
        venues = venues.filter(name__icontains=search_venue)
    
    pagenator = Paginator(venues, 10)
    page = request.GET.get('page')
    page_obj = pagenator.get_page(page)
    
    return render(request, 'events/venues_list.html', {'page_obj': page_obj, })

def venue_create(request):
    if not request.user.is_authenticated:
        messages.success(request, "장소를 생성하려면 로그인이 필요합니다.")
        return redirect('login')
    if request.method == 'POST':
        if request.user.is_superuser:
            form = VenueFormAdmin(request.POST, request.FILES or None,)
        else:
            form = VenueForm(request.POST, request.FILES or None,)
        if form.is_valid():
            venue = form.save(commit=False)
            if not request.user.is_superuser:
                venue.owner = request.user
            venue.save()
            messages.success(request, '새로운 장소가 생성되었습니다')
            return redirect('events:venue-details', venue_id=venue.id)
    else:
        if request.user.is_superuser:
            form = VenueFormAdmin()
        else:
            form = VenueForm()
        return render(request, 'events/venue_create.html', {'form': form })

def venue_details(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    try:
        owner_name = User.objects.get(pk=venue.owner.id) # type: ignore
    except User.DoesNotExist:
        owner_name = "지정한 소유자가 없습니다."
    return render(request, 'events/venue_details.html', {'venue': venue, 'owner_name': owner_name })

def venue_update(request, venue_id):
    if not request.user.is_authenticated:
        messages.success(request, "장소를 수정하려면 로그인이 필요합니다.")
        return redirect('login')
    venue = Venue.objects.get(pk=venue_id)
    
    store_previous_page(request)

    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect(request.session.pop('previous_page', 'events:venues-list'))
    return render(request, 'events/venue_update.html', {'venue': venue, 'form': form})

def venue_delete(request, venue_id):
    if not request.user.is_authenticated:
        messages.success(request, "장소를 삭제하려면 로그인이 필요합니다.")
        return redirect('login')
    venue = Venue.objects.get(pk=venue_id)
    if request.method == 'POST':
        venue.delete()
        return redirect('events:venues-list')

# events ==============================================
def events_list(request):
    events = Event.objects.all().order_by('-start_date')
    search_event = request.GET.get('searched', '')
    search_is_completed = request.GET.get('is_completed', '')
    
    if search_is_completed:
        events = events.filter(is_completed=search_is_completed)
    
    if search_event:
        events = events.filter(title__icontains=search_event)
    
    pagenator = Paginator(events, 6)
    page = request.GET.get('page')
    page_obj = pagenator.get_page(page)
    
    return render(request, 'events/events_list.html',{'page_obj': page_obj,})

def event_create(request, venue_id=None):
    if not request.user.is_authenticated:
        messages.success(request, "이벤트를 생성하려면 로그인이 필요합니다.")
        return redirect('login')
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST or None)
        else:
            form = EventForm(request.POST or None)
        if form.is_valid():
            event = form.save(commit=False)
            if not request.user.is_superuser:
                event.manager = request.user
            if venue_id:
                venue = Venue.objects.get(pk=venue_id)
                event.venue = venue

            event.save()
            form.save_m2m()
            messages.info(request, "이벤트가 생성되었습니다.")
            return redirect('events:events-list')
    else:
        initial = {}
        if venue_id:
            venue = Venue.objects.get(pk=venue_id)
            initial['venue'] = venue
        if request.user.is_superuser:
            form = EventFormAdmin(initial=initial)
        else:
            form = EventForm(initial=initial)
    return render(request, 'events/event_create.html', {'form': form })

def event_details(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/event_details.html', {'event': event})

def event_update(request, event_id):
    if not request.user.is_authenticated:
        messages.success(request, "이벤트를 수정하려면 로그인이 필요합니다.")
        return redirect('login')
    event = Event.objects.get(pk=event_id)
    
    store_previous_page(request)

    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect(request.session.pop('previous_page', 'events:events-list'))
    return render(request, 'events/event_update.html', {'event': event, 'form': form})

def event_delete(request, event_id):
    if not request.user.is_authenticated:
        messages.success(request, "이벤트를 삭제하려면 로그인이 필요합니다.")
        return redirect('login')
    event = Event.objects.get(pk=event_id)
    event.delete()
    store_previous_page(request)
    
    return redirect(request.session.pop('previous_page', 'events:events-list'))

def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

# reportlab 설치 및 사용 ===========================================
# PDF generation imports(py -m pip install reportlab 명령어로 설치 필요)
import csv
import codecs
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter 
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont 

def venue_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    textobject = p.beginText()
    textobject.setTextOrigin(inch, inch)
    
    # 한글 폰트 등록 (Windows: malgun.ttf, Mac: AppleGothic.ttf 등)
    try:
        pdfmetrics.registerFont(TTFont('Malgun', 'malgun.ttf'))
        font_name = 'Malgun'
    except:
        font_name = 'Helvetica' # 폰트 파일이 없을 경우 기본 폰트 사용
    textobject.setFont(font_name, 15)

    venues = Venue.objects.all().order_by('name')
    lines = []
    for venue in venues:
        lines.append(f"Name: {venue.name}")
        lines.append(f"Address: {venue.address}")
        lines.append(f"Web: {venue.web}")
        lines.append(" ")

    for line in lines:
        textobject.textLine(line)
        # 페이지 넘김 처리
        if textobject.getY() > letter[1] - inch:
            p.drawText(textobject)
            p.showPage()
            textobject = p.beginText()
            textobject.setTextOrigin(inch, inch)
            textobject.setFont(font_name, 15)

    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='venues.pdf')

def venue_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'
    # 한글 깨짐 방지
    response.write(codecs.BOM_UTF8)
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Address', 'Web'])
    
    venues = Venue.objects.all().order_by('name')
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.web, ])
    
    return response

def venue_text(request):
    url_name = request.resolver_match
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="venue_text.txt"'
    
    venues =Venue.objects.all().order_by('name')
    lines = []
    for venue in venues:
        lines.append(f"{venue.name}\n")
        lines.append(f"{venue.address}\n")
        lines.append(f"{venue.web}\n")
        lines.append("\n")
    response.writelines(lines)
    return response