from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
from datetime import date
from datetime import datetime
from datetime import time
import random
import calendar
from calendar import HTMLCalendar
from .models import Zipcodes
from .models import Neighbors
from .models import Addresses
from .models import Verifications
from .models import Friends
from .models import Logins
from .models import Home_clicks
from .models import Verification_skips
from .models import Verify_laters
from .models import Verifiers
from .models import Friend_checks
from .models import Events
from .models import Location_filters
from .models import View_filters
from .models import Calendar_filters
from .models import Date_filters
from .models import Event_views
from .models import Friend_views
from .models import Friend_requests
from .models import Signouts
from .models import Visits

def ad():
    if Events.objects.filter(event_start_date = date.today(),
                             event_public = True,
                             event_private = False).first() == None:
        ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                            <br><br>Click here to plan an event to host.
                            <br><br>Want to host an event but not sure how? Click here!"""
        ad_name = 'No events? Create one!'
        ad_end_time = '23:59:59'
        Events.objects.create(
            event_id = Events.objects.order_by('-event_id').first().event_id+1,
            neighbor_id = 1,
            event_description = ad_description,
            event_name = ad_name,
            event_start_date = date.today(),
            event_end_date = date.today(),
            event_start_time = datetime.today().time(),
            event_end_time = ad_end_time,
            event_reoccur = 'No',
            event_address = 'Your street number and name here',
            event_city = 'City',
            event_state = 'State',
            event_zipcode = 'Zipcode',
            event_public = True,
            event_private = False,
            event_invitees = 'none',
            evented_when = datetime.today()
        )

def unverified_ad():
    if Events.objects.filter(event_start_date = date.today()).first() == None:
        ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                            <br><br>Click here to plan an event to host.
                            <br><br>Want to host an event but not sure how? Click here!"""
        ad_name = 'No events? Create one!'
        ad_end_time = '23:59:59'
        Events.objects.create(
            event_id = Events.objects.order_by('-event_id').first().event_id+1,
            neighbor_id = 1,
            event_description = ad_description,
            event_name = ad_name,
            event_start_date = date.today(),
            event_end_date = date.today(),
            event_start_time = datetime.today().time(),
            event_end_time = ad_end_time,
            event_reoccur = 'No',
            event_address = 'Your street number and name here',
            event_city = 'City',
            event_state = 'State',
            event_zipcode = 'Zipcode',
            event_public = False,
            event_private = False,
            event_invitees = 'none',
            evented_when = datetime.today()
        )

def zipcode_ad(request):
    zipcode_neighbor = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
    zipcode_query = Zipcodes.objects.get(zipcode_id = zipcode_neighbor.zipcode)
    if Events.objects.filter(event_start_date = date.today(), 
                             event_zipcode = zipcode_neighbor.zipcode,
                             event_private = False).first() == None:
        ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                            <br><br>Click here to plan an event to host.
                            <br><br>Want to host an event but not sure how? Click here!"""
        ad_name = 'No events? Create one!'
        ad_end_time = '23:59:59'
        Events.objects.create(
            event_id = Events.objects.order_by('-event_id').first().event_id+1,
            neighbor_id = 1,
            event_description = ad_description,
            event_name = ad_name,
            event_start_date = date.today(),
            event_end_date = date.today(),
            event_start_time = datetime.today().time(),
            event_end_time = ad_end_time,
            event_reoccur = 'No',
            event_address = 'Your street number and name here',
            event_city = zipcode_query.city,
            event_state = zipcode_query.state,
            event_zipcode = zipcode_neighbor.zipcode,
            event_public = False,
            event_private = False,
            event_invitees = 'none',
            evented_when = datetime.today()
        )

def neighborhood_ad(request):
    neighborhood_neighbor = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
    neighborhood_neighbor_address = Addresses.objects.get(neighbor_id = request.session.get('neighbor_id'))
    if Events.objects.filter(event_start_date = date.today(), 
                             neighborhood_id = neighborhood_neighbor.neighborhood_id,
                             event_private = False).first() == None:
        ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                            <br><br>Click here to plan an event to host.
                            <br><br>Want to host an event but not sure how? Click here!"""
        ad_name = 'No events? Create one!'
        ad_end_time = '23:59:59'
        Events.objects.create(
            event_id = Events.objects.order_by('-event_id').first().event_id+1,
            neighbor_id = 1,
            event_description = ad_description,
            event_name = ad_name,
            event_start_date = date.today(),
            event_end_date = date.today(),
            event_start_time = datetime.today().time(),
            event_end_time = ad_end_time,
            event_reoccur = 'No',
            event_address = 'Your street number and name here',
            event_city = neighborhood_neighbor_address.city,
            event_state = neighborhood_neighbor_address.state,
            event_zipcode = neighborhood_neighbor.zipcode,
            event_public = False,
            event_private = False,
            event_invitees = 'none',
            evented_when = datetime.today(),
            neighborhood_id = neighborhood_neighbor.neighborhood_id
        )

# 1. LANDING PAGE
def index(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    Visits.objects.create(
        visit_id = Visits.objects.order_by('-visit_id').first().visit_id+1,
        visit_ip = ip,
        visited_when = datetime.today()
    )

    try:
        request.session['neighbor_id']
    except KeyError:
        ad()
        # >= today's date events
        public_events_today_n_after = []
        for column in Events.objects.filter(event_public = True, 
                                            event_start_date__gte = date.today(),
                                            event_private = False).order_by('event_start_date',
                                                                            'event_start_time'):
            public_events_today_n_after.append({
                'event_id' : column.event_id,
                'event_name' : column.event_name,
                'event_start_date' : column.event_start_date,
                'event_end_date' : column.event_end_date,
                'event_start_time' : column.event_start_time,
                'event_end_time' : column.event_end_time,
                'event_zipcode' : column.event_zipcode
                })
        relogin_context = {'events_data' : public_events_today_n_after,
                            'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                            'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
        return render(request, 'index.html', relogin_context)
    
    remember_neighbor = Neighbors.objects.get(neighbor_id = Logins.objects.filter(login_ip = ip).order_by('-login_id').first().neighbor_id)
    if ip in list(Logins.objects.all().values_list('login_ip',flat=True)):
        if remember_neighbor.neighbor_id in list(Addresses.objects.all().values_list('neighbor_id', flat=True)):
            remember_neighbor_address = Addresses.objects.get(neighbor_id = Logins.objects.filter(login_ip = ip).order_by('-login_id').first().neighbor_id)
            if remember_neighbor.neighborhood_id != 0:
                zipcode_ad(request)
                neighborhood_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                    event_zipcode = remember_neighbor.zipcode,
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    neighborhood_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == remember_neighbor.zipcode,
                        'neighborhood_match' : column.neighborhood_id == remember_neighbor.neighborhood_id,
                        'city_match' : column.event_city == remember_neighbor_address.city
                        })
                remember_neighbor_context = {'events_data' : neighborhood_events_today_n_after,
                                    'neighbor_name' : remember_neighbor_address.first_name,
                                    'neighbor_username' : remember_neighbor.username,
                                    'verified' : remember_neighbor.verified,
                                    'address' : remember_neighbor_address.address,
                                    'profile_picture' : remember_neighbor.profile_picture,
                                    'neighbor_zipcode' : remember_neighbor.zipcode}
                return render(request, 'login.html', remember_neighbor_context)
            zipcode_ad(request)
            zipcode_events_today_n_after = []
            for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                event_zipcode = remember_neighbor.zipcode,
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                zipcode_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode,
                    'zipcode_match' : column.event_zipcode == remember_neighbor.zipcode,
                    'city_match' : column.event_city == remember_neighbor_address.city
                    })
            remember_neighbor_context = {'events_data' : zipcode_events_today_n_after,
                                'neighbor_name' : remember_neighbor_address.first_name,
                                'neighbor_username' : remember_neighbor.username,
                                'verified' : remember_neighbor.verified,
                                'address' : remember_neighbor_address.address,
                                'profile_picture' : remember_neighbor.profile_picture,
                                'neighbor_zipcode' : remember_neighbor.zipcode}
            return render(request, 'login.html', remember_neighbor_context)
        else:
            remember_neighbor_location = Zipcodes.objects.get(zipcode_id = remember_neighbor.zipcode)
            zipcode_ad(request)
            zipcode_events_today_n_after = []
            for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                event_zipcode = remember_neighbor.zipcode,
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                zipcode_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode,
                    'zipcode_match' : column.event_zipcode == remember_neighbor.zipcode,
                    'city_match' : column.event_city == remember_neighbor_location.city
                    })
            remember_neighbor_context = {'events_data' : zipcode_events_today_n_after,
                                'neighbor_name' : None,
                                'neighbor_username' : remember_neighbor.username,
                                'verified' : remember_neighbor.verified,
                                'address' : None,
                                'profile_picture' : remember_neighbor.profile_picture,
                                'neighbor_zipcode' : remember_neighbor.zipcode} # events_data, variable name should be consistent across htmls with blocks
            return render(request, 'login.html', remember_neighbor_context)
    else:
        ad()
        # >= today's date events
        public_events_today_n_after = []
        for column in Events.objects.filter(event_public = True, 
                                            event_start_date__gte = date.today(),
                                            event_private = False).order_by('event_start_date',
                                                                            'event_start_time'):
            public_events_today_n_after.append({
                'event_id' : column.event_id,
                'event_name' : column.event_name,
                'event_start_date' : column.event_start_date,
                'event_end_date' : column.event_end_date,
                'event_start_time' : column.event_start_time,
                'event_end_time' : column.event_end_time,
                'event_zipcode' : column.event_zipcode
                })
        index_context = {'events_data' : public_events_today_n_after,
                        'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                        'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
        return render(request, 'index.html', index_context)

def view_event_from_signout(request):
    request.session['event_view_id'] = Event_views.objects.order_by('-event_view_id').first().event_view_id+1
    request.session['event_id'] = request.POST.get('event_id')
    Event_views.objects.create(
        event_view_id = request.session.get('event_view_id'),
        neighbor_id = 1, # need to change to a "neighbor" that tracks general visitors to the website
        event_id = request.session.get('event_id'),
        event_viewed_when = datetime.today()
    )
    event_query = Events.objects.get(event_id = request.session.get('event_id'))
    event_planner = Neighbors.objects.get(neighbor_id = event_query.neighbor_id)
    event_planner_address = Addresses.objects.get(neighbor_id = event_query.neighbor_id)
    event_planning_context = {
        'event_name' : event_query.event_name,
        'event_description' : event_query.event_description,
        'event_start_date' : event_query.event_start_date,
        'event_end_date' : event_query.event_end_date,
        'event_start_time' : event_query.event_start_time,
        'event_end_time' : event_query.event_end_time,
        'event_description' : event_query.event_description,
        'event_address' : event_query.event_address,
        'event_city' : event_query.event_city,
        'event_state' : event_query.event_state,
        'event_zipcode' : event_query.event_zipcode,
        'event_planner_name' : event_planner_address.first_name + " " + event_planner_address.last_name,
        'event_planner_username' : event_planner.username, # need to add logic where if users are not friends, can only see username
        'event_viewer_is_event_planner' : False
    }
    return render(request, 'events.html', event_planning_context) # needs to redirect to the event page

def signup(request):
    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            signup_ip = x_forwarded_for.split(',')[0]
        else:
            signup_ip = request.META.get('REMOTE_ADDR')

        if Neighbors.objects.filter(email = request.POST.get('email')).first() != None:
            ad()
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            account_exists_context = {'events_data' : public_events_today_n_after,
                                      'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                                      'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls with blocks
            return render(request, 'account_exists.html', account_exists_context)
        else:
            request.session['neighbor_id'] = Neighbors.objects.order_by('-neighbor_id').first().neighbor_id+1

            current_verification_codes_in_db = []
            for column in Verifications.objects.order_by('neighbor_id'):
                current_verification_codes_in_db.append(column.verification_code)

            new_verification_code = random.randint(100001, 999999)
            while new_verification_code in current_verification_codes_in_db:
                new_verification_code = random.randint(100001, 999999)

            if new_verification_code not in current_verification_codes_in_db:
                Neighbors.objects.create(
                    neighbor_id = request.session.get('neighbor_id'),
                    signup_datetime = datetime.today(),
                    username = request.POST.get('username'),
                    email = request.POST.get('email'),
                    zipcode = request.POST.get('zipcode'),
                    password = make_password(request.POST.get('password')),
                )
                Verifications.objects.create(
                    verification_id = Verifications.objects.order_by('-verification_id').first().verification_id+1,
                    neighbor_id = request.session.get('neighbor_id'),
                    verification_code = new_verification_code,
                    code_generated_when = datetime.today()
                )
                Logins.objects.create(
                    login_id = Logins.objects.order_by('-login_id').first().login_id+1,
                    neighbor_id = request.session.get('neighbor_id'),
                    login_datetime = datetime.today(),
                    login_ip = signup_ip
                )
                return render(request,'account_verify_from_signup.html')

def home(request):
    try:
        request.session['neighbor_id']
    except KeyError:
        ad()
        # >= today's date events
        public_events_today_n_after = []
        for column in Events.objects.filter(event_public = True, 
                                            event_start_date__gte = date.today(),
                                            event_private = False).order_by('event_start_date',
                                                                            'event_start_time'):
            public_events_today_n_after.append({
                'event_id' : column.event_id,
                'event_name' : column.event_name,
                'event_start_date' : column.event_start_date,
                'event_end_date' : column.event_end_date,
                'event_start_time' : column.event_start_time,
                'event_end_time' : column.event_end_time,
                'event_zipcode' : column.event_zipcode
                })
        relogin_context = {'events_data' : public_events_today_n_after,
                            'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                            'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
        return render(request, 'relogin.html', relogin_context)

    Home_clicks.objects.create(
        home_click_id = Home_clicks.objects.order_by('-home_click_id').first().home_click_id+1,
        neighbor_id = request.session.get('neighbor_id'),
        home_clicked_when = datetime.today()
    )
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    remember_neighbor = Neighbors.objects.get(neighbor_id = Logins.objects.filter(login_ip = ip).order_by('-login_id').first().neighbor_id)
    if ip in list(Logins.objects.all().values_list('login_ip',flat=True)):
        if remember_neighbor.neighbor_id in list(Addresses.objects.all().values_list('neighbor_id', flat=True)):
            remember_neighbor_address = Addresses.objects.get(neighbor_id = Logins.objects.filter(login_ip = ip).order_by('-login_id').first().neighbor_id)
            if remember_neighbor.neighborhood_id != 0:
                zipcode_ad(request) # start here - change so the events users first seee when logging in are those in their neighborhood.
                neighborhood_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                    event_zipcode = remember_neighbor.zipcode,
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    neighborhood_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == remember_neighbor.zipcode,
                        'neighborhood_match' : column.neighborhood_id == remember_neighbor.neighborhood_id,
                        'city_match' : column.event_city == remember_neighbor_address.city
                        })
                remember_neighbor_context = {'events_data' : neighborhood_events_today_n_after,
                                    'neighbor_name' : remember_neighbor_address.first_name,
                                    'neighbor_username' : remember_neighbor.username,
                                    'verified' : remember_neighbor.verified,
                                    'address' : remember_neighbor_address.address,
                                    'profile_picture' : remember_neighbor.profile_picture,
                                    'neighbor_zipcode' : remember_neighbor.zipcode} # events_data, variable name should be consistent across htmls with blocks
                return render(request, 'login.html', remember_neighbor_context)
            zipcode_ad(request) # start here - change so the events users first seee when logging in are those in their neighborhood.
            zipcode_events_today_n_after = []
            for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                event_zipcode = remember_neighbor.zipcode,
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                zipcode_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode,
                    'zipcode_match' : column.event_zipcode == remember_neighbor.zipcode,
                    'city_match' : column.event_city == remember_neighbor_address.city
                    })
            remember_neighbor_context = {'events_data' : zipcode_events_today_n_after,
                                'neighbor_name' : remember_neighbor_address.first_name,
                                'neighbor_username' : remember_neighbor.username,
                                'verified' : remember_neighbor.verified,
                                'address' : remember_neighbor_address.address,
                                'profile_picture' : remember_neighbor.profile_picture,
                                'neighbor_zipcode' : remember_neighbor.zipcode} # events_data, variable name should be consistent across htmls with blocks
            return render(request, 'login.html', remember_neighbor_context)
        else:
            remember_neighbor_location = Zipcodes.objects.get(zipcode_id = remember_neighbor.zipcode)
            zipcode_ad(request) # start here - change so the events users first seee when logging in are those in their neighborhood.
            zipcode_events_today_n_after = []
            for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                event_zipcode = remember_neighbor.zipcode,
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                zipcode_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode,
                    'zipcode_match' : column.event_zipcode == remember_neighbor.zipcode,
                    'city_match' : column.event_city == remember_neighbor_location.city
                    })
            remember_neighbor_context = {'events_data' : zipcode_events_today_n_after,
                                'neighbor_name' : None,
                                'neighbor_username' : remember_neighbor.username,
                                'verified' : remember_neighbor.verified,
                                'address' : None,
                                'profile_picture' : remember_neighbor.profile_picture,
                                'neighbor_zipcode' : remember_neighbor.zipcode} # events_data, variable name should be consistent across htmls with blocks
            return render(request, 'login.html', remember_neighbor_context)
    else:
        ad()
        # >= today's date events
        public_events_today_n_after = []
        for column in Events.objects.filter(event_public = True, 
                                            event_start_date__gte = date.today(),
                                            event_private = False).order_by('event_start_date',
                                                                            'event_start_time'):
            public_events_today_n_after.append({
                'event_id' : column.event_id,
                'event_name' : column.event_name,
                'event_start_date' : column.event_start_date,
                'event_end_date' : column.event_end_date,
                'event_start_time' : column.event_start_time,
                'event_end_time' : column.event_end_time,
                'event_zipcode' : column.event_zipcode
                })
        index_context = {'events_data' : public_events_today_n_after,
                        'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                        'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
        return render(request, 'index.html', index_context)
        
def account_verify_from_signup(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        request.session['address_id'] = Addresses.objects.order_by('-address_id').first().address_id+1
        Addresses.objects.create(neighbor_id = request.session.get('neighbor_id'),
                                 address_id = request.session.get('address_id'),
                                 first_name = request.POST.get('first_name'),
                                 last_name = request.POST.get('last_name'),
                                 address = request.POST.get('address'),
                                 city = request.POST.get('city'),
                                 state = request.POST.get('state'))
        Neighbors.objects.filter(neighbor_id = request.session.get('neighbor_id')).update(zipcode = request.POST.get('zipcode'))
        currently_signed_up_neighbor = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
        currently_signed_up_neighbor_address = Addresses.objects.get(neighbor_id = request.session.get('neighbor_id'))
        zipcode_ad(request)
        zipcode_events_today_n_after = []
        for column in Events.objects.filter(event_start_date__gte = date.today(),
                                            event_zipcode = currently_signed_up_neighbor.zipcode,
                                            event_private = False).order_by('event_start_date',
                                                                            'event_start_time'):
            zipcode_events_today_n_after.append({
                'event_id' : column.event_id,
                'event_name' : column.event_name,
                'event_start_date' : column.event_start_date,
                'event_end_date' : column.event_end_date,
                'event_start_time' : column.event_start_time,
                'event_end_time' : column.event_end_time,
                'event_zipcode' : column.event_zipcode,
                'zipcode_match' : column.event_zipcode == currently_signed_up_neighbor.zipcode,
                'city_match' : column.event_city == currently_signed_up_neighbor_address.city
                })
        first_login_context = {'events_data' : zipcode_events_today_n_after,
                               'neighbor_name' : currently_signed_up_neighbor_address.first_name,
                               'verified' : currently_signed_up_neighbor.verified,
                               'address' : currently_signed_up_neighbor_address.address,
                               'profile_picture' : currently_signed_up_neighbor.profile_picture,
                               'neighbor_zipcode' : currently_signed_up_neighbor.zipcode} # events_data, variable name should be consistent across htmls with blocks
        return render(request, 'login.html', first_login_context)

def skip_verification(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        Verification_skips.objects.create(
            skip_id = Verification_skips.objects.order_by('-skip_id').first().skip_id+1,
            neighbor_id = request.session.get('neighbor_id'),
            skipped_when = datetime.today()
        )
        skipping_neighbor = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
        skipping_neighbor_location = Zipcodes.objects.get(zipcode_id = skipping_neighbor.zipcode)
        zipcode_ad(request)
        zipcode_events_today_n_after = []
        for column in Events.objects.filter(event_start_date__gte = date.today(),
                                            event_zipcode = skipping_neighbor.zipcode,
                                            event_private = False).order_by('event_start_date',
                                                                            'event_start_time'):
            zipcode_events_today_n_after.append({
                'event_id' : column.event_id,
                'event_name' : column.event_name,
                'event_start_date' : column.event_start_date,
                'event_end_date' : column.event_end_date,
                'event_start_time' : column.event_start_time,
                'event_end_time' : column.event_end_time,
                'event_zipcode' : column.event_zipcode,
                'zipcode_match' : column.event_zipcode == skipping_neighbor.zipcode,
                'city_match' : column.event_city == skipping_neighbor_location.city
                })
        skipping_neighbor_context = {'events_data' : zipcode_events_today_n_after,
                                     'neighbor_username' : skipping_neighbor.username,
                                     'neighbor_name' : None,
                                     'verified' : skipping_neighbor.verified,
                                     'address' : None,
                                     'profile_picture' : skipping_neighbor.profile_picture,
                                     'neighbor_zipcode' : skipping_neighbor.zipcode} # events_data, variable name should be consistent across htmls with blocks
        return render(request, 'login.html', skipping_neighbor_context)
            
# X. LOGIN PAGE
def login(request):
    if request.method == 'POST':
        login_email = request.POST.get('email')
        login_neighbor = Neighbors.objects.get(email = login_email)

        if check_password(request.POST.get('password'), login_neighbor.password):
            login_password = login_neighbor.password
        else:
            ad()
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            wrong_pass_context = {'events_data' : public_events_today_n_after,
                                  'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                                  'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'wrong_pass.html', wrong_pass_context)

        if login_neighbor != None:
            if login_email + login_password in login_neighbor.email + login_neighbor.password:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                concat_email_password_ip = []
                for column in Logins.objects.filter(neighbor_id = login_neighbor.neighbor_id):
                    concat_email_password_ip.append(login_neighbor.email + login_neighbor.password + column.login_ip)
                if login_email + login_password + ip in concat_email_password_ip:
                    request.session['neighbor_id'] = login_neighbor.neighbor_id
                    # if request.POST.get('login_rememberme') == None:
                    #     rememberme = False
                    # else:
                    #     rememberme = request.POST.get('login_rememberme')
                    Logins.objects.create(login_id = Logins.objects.order_by('-login_id').first().login_id+1, 
                                          neighbor_id = request.session.get('neighbor_id'), 
                                          login_datetime = datetime.today(), 
                                          login_ip = ip,
                                          # login_rememberme = rememberme
                                          )
                    if login_neighbor.neighbor_id in list(Addresses.objects.all().values_list('neighbor_id', flat=True)):
                        login_neighbor_address = Addresses.objects.get(neighbor_id = Logins.objects.filter(login_ip = ip).order_by('-login_id').first().neighbor_id)
                        if login_neighbor.neighborhood_id != 0:
                            zipcode_ad(request)
                            neighborhood_events_today_n_after = []
                            for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                                event_zipcode = login_neighbor.zipcode,
                                                                event_private = False).order_by('event_start_date',
                                                                                                'event_start_time'):
                                neighborhood_events_today_n_after.append({
                                    'event_id' : column.event_id,
                                    'event_name' : column.event_name,
                                    'event_start_date' : column.event_start_date,
                                    'event_end_date' : column.event_end_date,
                                    'event_start_time' : column.event_start_time,
                                    'event_end_time' : column.event_end_time,
                                    'event_zipcode' : column.event_zipcode,
                                    'zipcode_match' : column.event_zipcode == login_neighbor.zipcode,
                                    'neighborhood_match': column.neighborhood_id == login_neighbor.neighborhood_id,
                                    'city_match' : column.event_city == login_neighbor_address.city
                                    })
                            login_context = {
                                'events_data' : neighborhood_events_today_n_after,
                                'neighbor_username' : login_neighbor.username,
                                'neighbor_name' : login_neighbor_address.first_name,
                                'verified' : login_neighbor.verified,
                                'address' : login_neighbor_address.address,
                                'profile_picture' : login_neighbor.profile_picture,
                                'neighbor_zipcode' : login_neighbor.zipcode
                                } # events_data, variable name should be consistent across htmls with blocks
                            return render(request, 'login.html', login_context)
                        zipcode_ad(request)
                        zipcode_events_today_n_after = []
                        for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                            event_zipcode = login_neighbor.zipcode,
                                                            event_private = False).order_by('event_start_date',
                                                                                            'event_start_time'):
                            zipcode_events_today_n_after.append({
                                'event_id' : column.event_id,
                                'event_name' : column.event_name,
                                'event_start_date' : column.event_start_date,
                                'event_end_date' : column.event_end_date,
                                'event_start_time' : column.event_start_time,
                                'event_end_time' : column.event_end_time,
                                'event_zipcode' : column.event_zipcode,
                                'zipcode_match' : column.event_zipcode == login_neighbor.zipcode,
                                'city_match' : column.event_city == login_neighbor_address.city
                                })
                        login_context = {
                            'events_data' : zipcode_events_today_n_after,
                            'neighbor_username' : login_neighbor.username,
                            'neighbor_name' : login_neighbor_address.first_name,
                            'verified' : login_neighbor.verified,
                            'address' : login_neighbor_address.address,
                            'profile_picture' : login_neighbor.profile_picture,
                            'neighbor_zipcode' : login_neighbor.zipcode
                            } # events_data, variable name should be consistent across htmls with blocks
                        return render(request, 'login.html', login_context)
                    else:
                        login_neighbor_location = Zipcodes.objects.get(zipcode_id = login_neighbor.zipcode)
                        zipcode_ad(request)
                        zipcode_events_today_n_after = []
                        for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                            event_zipcode = login_neighbor.zipcode,
                                                            event_private = False).order_by('event_start_date',
                                                                                            'event_start_time'):
                            zipcode_events_today_n_after.append({
                                'event_id' : column.event_id,
                                'event_name' : column.event_name,
                                'event_start_date' : column.event_start_date,
                                'event_end_date' : column.event_end_date,
                                'event_start_time' : column.event_start_time,
                                'event_end_time' : column.event_end_time,
                                'event_zipcode' : column.event_zipcode,
                                'zipcode_match' : column.event_zipcode == login_neighbor.zipcode,
                                'city_match' : column.event_city == login_neighbor_location.city
                                })
                        login_context = {
                            'events_data' : zipcode_events_today_n_after,
                            'neighbor_username' : login_neighbor.username,
                            'neighbor_name' : None,
                            'verified' : login_neighbor.verified,
                            'address' : None,
                            'profile_picture' : login_neighbor.profile_picture,
                            'neighbor_zipcode' : login_neighbor.zipcode
                            } # events_data, variable name should be consistent across htmls with blocks
                        return render(request, 'login.html', login_context)
                else:
                    return render(request, 'ip_verif.html')
        else:
            ad()
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            wrong_pass_context = {'events_data' : public_events_today_n_after,
                                  'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                                  'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'wrong_pass.html', wrong_pass_context)

def account_verify_from_login(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        Verify_laters.objects.create(
            later_id = Verify_laters.objects.order_by('-later_id').first().later_id+1,
            neighbor_id = request.session.get('neighbor_id'),
            later_when = datetime.today()
        )
        return render(request, 'account_verify_from_signup.html') #create a new html for account verify from login?

def verify_with_code(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        Verifiers.objects.create(
            verifier_id = Verifiers.objects.order_by('-verifier_id').first().verifier_id+1,
            neighbor_id = request.session.get('neighbor_id'),
            verifier_when = datetime.today()
        )
        return render(request, 'code_verification.html')

def verified(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        if Verifications.objects.filter(neighbor_id = request.session.get('neighbor_id')).order_by('-code_generated_when').first().verification_code == request.POST.get('verification_code'):
            Neighbors.objects.filter(neighbor_id = request.session.get('neighbor_id')).update(verified = True)
            verifying_neighbor = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
            verifying_neighbor_address = Addresses.objects.get(neighbor_id = request.session.get('neighbor_id'))
            zipcode_ad(request)
            zipcode_events_today_n_after = []
            for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                event_zipcode = verifying_neighbor.zipcode,
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                zipcode_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode,
                    'zipcode_match' : column.event_zipcode == verifying_neighbor.zipcode,
                    'neighborhood_match' : column.neighborhood_id == verifying_neighbor.neighborhood_id,
                    'city_match' : column.event_city == verifying_neighbor_address.city
                    })
            verified_context = {
                'events_data' : zipcode_events_today_n_after,
                'neighbor_name' : verifying_neighbor_address.first_name,
                'verified' : verifying_neighbor.verified,
                'address' : verifying_neighbor_address.address,
                'profile_picture' : verifying_neighbor.profile_picture,
                'neighbor_zipcode' : verifying_neighbor.zipcode
            }
            return render(request, 'login.html', verified_context)
        else:
            return render(request, 'wrong_code.html')

def friends_check(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        neighbor_with_friends = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
        neighbor_with_friends_list = list(Friends.objects.filter(neighbor_id = request.session.get('neighbor_id')).values_list('friend_id',flat=True))
        Friend_checks.objects.create(
            friend_check_id = Friend_checks.objects.order_by('-friend_check_id').first().friend_check_id+1,
            neighbor_id = request.session.get('neighbor_id'),
            friend_check_when = datetime.today()
        )
        if neighbor_with_friends_list != []:
            # friends_ids = neighbor_with_friends.friends.split(',')
            friends_list = {}
            for friend_id in neighbor_with_friends_list:
                friends_list[friend_id] = str(list(Addresses.objects.filter(neighbor_id = friend_id).values_list('first_name', flat=True)) + list(Addresses.objects.filter(neighbor_id = friend_id).values_list('last_name', flat=True))).replace('[','').replace(']','').replace("'",'').replace(',','')
            friends_context = {'friends' : dict(sorted(friends_list.items(), key=lambda x:x[1]))}
            return render(request, 'friends.html', friends_context)
        else:
            if neighbor_with_friends.neighbor_id in list(Addresses.objects.all().values_list('neighbor_id', flat=True)):
                neighbor_with_friends_address = Addresses.objects.get(neighbor_id = request.session.get('neighbor_id'))
                if neighbor_with_friends.neighborhood_id != 0:
                    zipcode_ad(request)
                    neighborhood_events_today_n_after = []
                    for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                        event_zipcode = neighbor_with_friends.zipcode,
                                                        event_private = False).order_by('event_start_date',
                                                                                        'event_start_time'):
                        neighborhood_events_today_n_after.append({
                            'event_id' : column.event_id,
                            'event_name' : column.event_name,
                            'event_start_date' : column.event_start_date,
                            'event_end_date' : column.event_end_date,
                            'event_start_time' : column.event_start_time,
                            'event_end_time' : column.event_end_time,
                            'event_zipcode' : column.event_zipcode,
                            'zipcode_match' : column.event_zipcode == neighbor_with_friends.zipcode,
                            'neighborhood_match' : column.neighborhood_id == neighbor_with_friends.neighborhood_id,
                            'city_match' : column.event_city == neighbor_with_friends_address.city
                            })
                    no_friend_context = {
                        'events_data' : neighborhood_events_today_n_after,
                        'neighbor_username' : neighbor_with_friends.username,
                        'neighbor_name' : neighbor_with_friends_address.first_name,
                        'verified' : neighbor_with_friends.verified,
                        'address' : neighbor_with_friends_address.address,
                        'profile_picture' : neighbor_with_friends.profile_picture,
                        'friends' : neighbor_with_friends_list == [],
                        'neighbor_zipcode' : neighbor_with_friends.zipcode
                    }
                    return render(request, 'login.html', no_friend_context)
                zipcode_ad(request)
                zipcode_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                    event_zipcode = neighbor_with_friends.zipcode,
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    zipcode_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == neighbor_with_friends.zipcode,
                        'city_match' : column.event_city == neighbor_with_friends_address.city
                        })
                no_friend_context = {
                    'events_data' : zipcode_events_today_n_after,
                    'neighbor_username' : neighbor_with_friends.username,
                    'neighbor_name' : neighbor_with_friends_address.first_name,
                    'verified' : neighbor_with_friends.verified,
                    'address' : neighbor_with_friends_address.address,
                    'profile_picture' : neighbor_with_friends.profile_picture,
                    'friends' : neighbor_with_friends_list == [],
                    'neighbor_zipcode' : neighbor_with_friends.zipcode
                }
                return render(request, 'login.html', no_friend_context)
            else:
                neighbor_with_friends_location = Zipcodes.objects.get(zipcode_id = neighbor_with_friends.zipcode)
                zipcode_ad(request)
                zipcode_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                    event_zipcode = neighbor_with_friends.zipcode,
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    zipcode_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == neighbor_with_friends.zipcode,
                        'city_match' : column.event_city == neighbor_with_friends_location.city
                        })
                no_friend_context = {
                    'events_data' : zipcode_events_today_n_after,
                    'neighbor_username' : neighbor_with_friends.username,
                    'neighbor_name' : None,
                    'verified' : neighbor_with_friends.verified,
                    'address' : None,
                    'profile_picture' : neighbor_with_friends.profile_picture,
                    'friends' : neighbor_with_friends_list == [],
                    'neighbor_zipcode' : neighbor_with_friends.zipcode
                }
                return render(request, 'login.html', no_friend_context)

def plan_event(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        event_plan_description = request.POST.get('event_description')
        event_plan_name = request.POST.get('event_name')
        event_plan_start_date = request.POST.get('event_start_date')
        event_plan_end_date = request.POST.get('event_end_date')
        event_plan_start_time = request.POST.get('event_start_time')
        event_plan_end_time = request.POST.get('event_end_time')
        event_plan_reoccur = request.POST.get('event_reoccur')
        event_plan_address = request.POST.get('event_address')
        event_plan_city = request.POST.get('event_city')
        event_plan_state = request.POST.get('event_state')
        event_plan_zipcode = request.POST.get('event_zipcode')
        if request.POST.get('event_public') == None:
            event_plan_public = False
        else:
            event_plan_public = True
        event_exists_check = Events.objects.filter(event_description = event_plan_description,
                                                   event_name = event_plan_name,
                                                   event_start_date = event_plan_start_date,
                                                   event_end_date = event_plan_end_date,
                                                   event_start_time = event_plan_start_time,
                                                   event_end_time = event_plan_end_time,
                                                   event_reoccur = event_plan_reoccur,
                                                   event_address = event_plan_address,
                                                   event_city = event_plan_city,
                                                   event_state = event_plan_state,
                                                   event_zipcode = event_plan_zipcode,
                                                   event_public = event_plan_public)
        if event_exists_check.first() != None:
            event_existing_planner = Neighbors.objects.get(neighbor_id = event_exists_check.first().neighbor_id)
            event_existing_planner_address = Addresses.objects.get(neighbor_id = event_exists_check.first().neighbor_id)
            event_viewer_is_event_existing_planner = request.session.get('neighbor_id') == event_exists_check.first().neighbor_id
            event_exists_context = {
                'event_exists' : event_exists_check,
                'event_name' : event_plan_name,
                'event_description' : event_plan_description,
                'event_start_date' : datetime.strptime(event_plan_start_date,'%Y-%m-%d').strftime('%B %d, %Y'),
                'event_end_date' : datetime.strptime(event_plan_end_date,'%Y-%m-%d').strftime('%B %d, %Y'),
                'event_start_time' : datetime.strptime(event_plan_start_time, '%H:%M').strftime('%I:%M %p'),
                'event_end_time' : datetime.strptime(event_plan_end_time, '%H:%M').strftime('%I:%M %p'),
                'event_description' : event_plan_description,
                'event_address' : event_plan_address,
                'event_city' : event_plan_city,
                'event_state' : event_plan_state,
                'event_zipcode' : event_plan_zipcode,
                'event_planner_name' : event_existing_planner_address.first_name + " " + event_existing_planner_address.last_name,
                'event_planner_username' : event_existing_planner.username,
                'event_viewer_is_event_planner' : event_viewer_is_event_existing_planner,
                'event_planner_id' : event_exists_check.first().neighbor_id
            }
            return render(request, 'events.html', event_exists_context)
        else:
            request.session['event_id'] = Events.objects.order_by('-event_id').first().event_id+1
            Events.objects.create(
                event_id = request.session.get('event_id'),
                neighbor_id = request.session.get('neighbor_id'),
                event_description = event_plan_description,
                event_name = event_plan_name,
                event_start_date = event_plan_start_date,
                event_end_date = event_plan_end_date,
                event_start_time = event_plan_start_time,
                event_end_time = event_plan_end_time,
                event_reoccur = event_plan_reoccur,
                event_address = event_plan_address,
                event_city = event_plan_city,
                event_state = event_plan_state,
                event_zipcode = event_plan_zipcode,
                event_public = event_plan_public,
                event_invitees = 'none',
                evented_when = datetime.today()
            )
            event_query = Events.objects.get(event_id = request.session.get('event_id'))
            event_planner = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
            event_planner_address = Addresses.objects.get(neighbor_id = request.session.get('neighbor_id'))
            event_viewer_is_event_planner = event_query.neighbor_id == request.session.get('neighbor_id')
            event_planning_context = {
                'event_name' : event_query.event_name,
                'event_description' : event_query.event_description,
                'event_start_date' : event_query.event_start_date,
                'event_end_date' : event_query.event_end_date,
                'event_start_time' : event_query.event_start_time,
                'event_end_time' : event_query.event_end_time,
                'event_description' : event_query.event_description,
                'event_address' : event_query.event_address,
                'event_city' : event_query.event_city,
                'event_state' : event_query.event_state,
                'event_zipcode' : event_query.event_zipcode,
                'event_planner_name' : event_planner_address.first_name + " " + event_planner_address.last_name,
                'event_planner_username' : event_planner.username,
                'event_viewer_is_event_planner' : event_viewer_is_event_planner,
                'event_planner_id' : event_query.neighbor_id
            }
            return render(request, 'events.html', event_planning_context) # needs to redirect to the event page

def all_ad():
    if Events.objects.filter(event_start_date = date.today(),
                             event_private = False).first() == None:
        ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                            <br><br>Click here to plan an event to host.
                            <br><br>Want to host an event but not sure how? Click here!"""
        ad_name = 'No events? Create one!'
        ad_end_time = '23:59:59'
        Events.objects.create(
            event_id = Events.objects.order_by('-event_id').first().event_id+1,
            neighbor_id = 1,
            event_description = ad_description,
            event_name = ad_name,
            event_start_date = date.today(),
            event_end_date = date.today(),
            event_start_time = datetime.today().time(),
            event_end_time = ad_end_time,
            event_reoccur = 'No',
            event_address = 'Your street number and name here',
            event_city = 'City',
            event_state = 'State',
            event_zipcode = 'Zipcode',
            event_public = False,
            event_private = False,
            event_invitees = 'none',
            evented_when = datetime.today()
        )

def city_ad(request):
    location_filtering_neighbor = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
    location_filtering_neighbor_location = Zipcodes.objects.get(zipcode_id = location_filtering_neighbor.zipcode)
    if Events.objects.filter(event_start_date__gte = date.today(),
                             event_city = location_filtering_neighbor_location.city).first() == None: # separate table for addresses in vicinity...
        ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                            <br><br>Click here to plan an event to host.
                            <br><br>Want to host an event but not sure how? Click here!"""
        ad_name = 'No events? Create one!'
        ad_end_time = '23:59:59'
        Events.objects.create(
            event_id = Events.objects.order_by('-event_id').first().event_id+1,
            neighbor_id = 1,
            event_description = ad_description,
            event_name = ad_name,
            event_start_date = date.today(),
            event_end_date = date.today(),
            event_start_time = datetime.today().time(),
            event_end_time = ad_end_time,
            event_reoccur = 'No',
            event_address = 'Your street number and name here',
            event_city = location_filtering_neighbor_location.city,
            event_state = location_filtering_neighbor_location.state,
            event_zipcode = location_filtering_neighbor.zipcode,
            event_public = False,
            event_private = False,
            event_invitees = 'none',
            evented_when = datetime.today()
        )

def filter_location(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        location_filter_choice = request.POST.get('location_filter')
        request.session['location_filter_id'] = Location_filters.objects.order_by('-location_filter_id').first().location_filter_id+1
        Location_filters.objects.create(
            location_filter_id = request.session.get('location_filter_id'),
            neighbor_id = request.session.get('neighbor_id'),
            location_filter = location_filter_choice,
            location_filtered_when = datetime.today()
        )
        location_filtering_neighbor = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
        if location_filter_choice == 'All':
            if location_filtering_neighbor.neighbor_id in list(Addresses.objects.all().values_list('neighbor_id', flat=True)):
                location_filtering_neighbor_address = Addresses.objects.get(neighbor_id = location_filtering_neighbor.neighbor_id)
                if location_filtering_neighbor.neighborhood_id != 0:
                    all_ad()
                    all_events_today_n_after = []
                    for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                        event_private = False).order_by('event_start_date',
                                                                                        'event_start_time'):
                        all_events_today_n_after.append({
                            'event_id' : column.event_id,
                            'event_name' : column.event_name,
                            'event_start_date' : column.event_start_date,
                            'event_end_date' : column.event_end_date,
                            'event_start_time' : column.event_start_time,
                            'event_end_time' : column.event_end_time,
                            'event_zipcode' : column.event_zipcode,
                            'zipcode_match' : column.event_zipcode == location_filtering_neighbor.zipcode,
                            'neighborhood_match' : column.neighborhood_id == location_filtering_neighbor.neighborhood_id,
                            'city_match' : column.event_city == location_filtering_neighbor_address.city
                            })
                    location_filter_context = {
                        'events_data' : all_events_today_n_after,
                        'neighbor_username' : location_filtering_neighbor.username,
                        'neighbor_name' : location_filtering_neighbor_address.first_name,
                        'verified' : location_filtering_neighbor.verified,
                        'address' : location_filtering_neighbor_address.address,
                        'profile_picture' : location_filtering_neighbor.profile_picture,
                        'neighbor_zipcode' : location_filtering_neighbor.zipcode
                        } # events_data, variable name should be consistent across htmls with blocks
                    return render(request, 'login.html', location_filter_context)
                all_ad()
                all_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    all_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == location_filtering_neighbor.zipcode,
                        'city_match' : column.event_city == location_filtering_neighbor_address.city
                        })
                location_filter_context = {
                    'events_data' : all_events_today_n_after,
                    'neighbor_username' : location_filtering_neighbor.username,
                    'neighbor_name' : location_filtering_neighbor_address.first_name,
                    'verified' : location_filtering_neighbor.verified,
                    'address' : location_filtering_neighbor_address.address,
                    'profile_picture' : location_filtering_neighbor.profile_picture,
                    'neighbor_zipcode' : location_filtering_neighbor.zipcode
                    } # events_data, variable name should be consistent across htmls with blocks
                return render(request, 'login.html', location_filter_context)
            else:
                neighbor_location = Zipcodes.objects.get(zipcode_id = location_filtering_neighbor.zipcode)
                all_ad()
                all_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    all_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == location_filtering_neighbor.zipcode,
                        'city_match' : column.event_city == neighbor_location.city
                        })
                location_filter_context = {
                    'events_data' : all_events_today_n_after,
                    'neighbor_username' : location_filtering_neighbor.username,
                    'neighbor_name' : None,
                    'verified' : location_filtering_neighbor.verified,
                    'address' : None,
                    'profile_picture' : location_filtering_neighbor.profile_picture,
                    'neighbor_zipcode' : location_filtering_neighbor.zipcode
                    } # events_data, variable name should be consistent across htmls with blocks
                return render(request, 'login.html', location_filter_context)
        elif location_filter_choice == 'My zipcode':
            if location_filtering_neighbor.neighbor_id in list(Addresses.objects.all().values_list('neighbor_id', flat=True)):
                location_filtering_neighbor_address = Addresses.objects.get(neighbor_id = location_filtering_neighbor.neighbor_id)
                if location_filtering_neighbor.neighborhood_id != 0:
                    zipcode_ad(request)
                    zipcode_events_today_n_after = []
                    for column in Events.objects.filter(event_start_date__gte = date.today(), 
                                                        event_zipcode = location_filtering_neighbor.zipcode,
                                                        event_private = False).order_by('event_start_date',
                                                                                        'event_start_time'):
                        zipcode_events_today_n_after.append({
                            'event_id' : column.event_id,
                            'event_name' : column.event_name,
                            'event_start_date' : column.event_start_date,
                            'event_end_date' : column.event_end_date,
                            'event_start_time' : column.event_start_time,
                            'event_end_time' : column.event_end_time,
                            'event_zipcode' : column.event_zipcode,
                            'zipcode_match' : column.event_zipcode == location_filtering_neighbor.zipcode,
                            'neighborhood_match' : column.neighborhood_id == location_filtering_neighbor.neighborhood_id,
                            'city_match' : column.event_city == location_filtering_neighbor_address.city
                            })
                    location_filter_context = {
                        'events_data' : zipcode_events_today_n_after,
                        'neighbor_username' : location_filtering_neighbor.username,
                        'neighbor_name' : location_filtering_neighbor_address.first_name,
                        'verified' : location_filtering_neighbor.verified,
                        'address' : location_filtering_neighbor_address.address,
                        'profile_picture' : location_filtering_neighbor.profile_picture,
                        'neighbor_zipcode' : location_filtering_neighbor.zipcode
                        } # events_data, variable name should be consistent across htmls with blocks
                    return render(request, 'login.html', location_filter_context)
                zipcode_ad(request)
                zipcode_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(), 
                                                    event_zipcode = location_filtering_neighbor.zipcode,
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    zipcode_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == location_filtering_neighbor.zipcode,
                        'city_match' : column.event_city == location_filtering_neighbor_address.city
                        })
                location_filter_context = {
                    'events_data' : zipcode_events_today_n_after,
                    'neighbor_username' : location_filtering_neighbor.username,
                    'neighbor_name' : location_filtering_neighbor_address.first_name,
                    'verified' : location_filtering_neighbor.verified,
                    'address' : location_filtering_neighbor_address.address,
                    'profile_picture' : location_filtering_neighbor.profile_picture,
                    'neighbor_zipcode' : location_filtering_neighbor.zipcode
                    } # events_data, variable name should be consistent across htmls with blocks
                return render(request, 'login.html', location_filter_context)
            else:
                neighbor_location = Zipcodes.objects.get(zipcode_id = location_filtering_neighbor.zipcode)
                zipcode_ad(request)
                zipcode_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(), 
                                                    event_zipcode = location_filtering_neighbor.zipcode,
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    zipcode_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == location_filtering_neighbor.zipcode,
                        'city_match' : column.event_city == neighbor_location.city
                        })
                location_filter_context = {
                    'events_data' : zipcode_events_today_n_after,
                    'neighbor_username' : location_filtering_neighbor.username,
                    'neighbor_name' : None,
                    'verified' : location_filtering_neighbor.verified,
                    'address' : None,
                    'profile_picture' : location_filtering_neighbor.profile_picture,
                    'neighbor_zipcode' : location_filtering_neighbor.zipcode
                    } # events_data, variable name should be consistent across htmls with blocks
                return render(request, 'login.html', location_filter_context)
        elif location_filter_choice == 'My neighborhood':
            if location_filtering_neighbor.neighborhood_id == 0:
                if location_filtering_neighbor.neighbor_id in list(Addresses.objects.all().values_list('neighbor_id', flat=True)):
                    location_filtering_neighbor_address = Addresses.objects.get(neighbor_id = location_filtering_neighbor.neighbor_id)
                    zipcode_ad(request)
                    zipcode_events_today_n_after = []
                    for column in Events.objects.filter(event_start_date__gte = date.today(), 
                                                        event_zipcode = location_filtering_neighbor.zipcode,
                                                        event_private = False).order_by('event_start_date',
                                                                                        'event_start_time'):
                        zipcode_events_today_n_after.append({
                            'event_id' : column.event_id,
                            'event_name' : column.event_name,
                            'event_start_date' : column.event_start_date,
                            'event_end_date' : column.event_end_date,
                            'event_start_time' : column.event_start_time,
                            'event_end_time' : column.event_end_time,
                            'event_zipcode' : column.event_zipcode,
                            'zipcode_match' : column.event_zipcode == location_filtering_neighbor.zipcode,
                            'city_match' : column.event_city == location_filtering_neighbor_address.city
                            })
                    location_filter_context = {
                        'events_data' : zipcode_events_today_n_after,
                        'neighbor_username' : location_filtering_neighbor.username,
                        'neighbor_name' : location_filtering_neighbor_address.first_name,
                        'verified' : location_filtering_neighbor.verified,
                        'address' : location_filtering_neighbor_address.address,
                        'profile_picture' : location_filtering_neighbor.profile_picture,
                        'neighbor_zipcode' : location_filtering_neighbor.zipcode
                        } # events_data, variable name should be consistent across htmls with blocks
                    return render(request, 'verify.html', location_filter_context)
                else:
                    Verify_laters.objects.create(
                        later_id = Verify_laters.objects.order_by('-later_id').first().later_id+1,
                        neighbor_id = request.session.get('neighbor_id'),
                        later_when = datetime.today()
                    )
                    return render(request, 'account_verify_from_signup.html') #create a new html for account verify from login?
            else:
                location_filtering_neighbor_address = Addresses.objects.get(neighbor_id = location_filtering_neighbor.neighbor_id)
                neighborhood_ad(request)
                neighborhood_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(), 
                                                    neighborhood_id = location_filtering_neighbor.neighborhood_id,
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    neighborhood_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'neighborhood_match' : column.neighborhood_id == location_filtering_neighbor.neighborhood_id,
                        'city_match' : column.event_city == location_filtering_neighbor_address.city
                        })
                location_filter_context = {
                    'events_data' : neighborhood_events_today_n_after,
                    'neighbor_username' : location_filtering_neighbor.username,
                    'neighbor_name' : location_filtering_neighbor_address.first_name,
                    'verified' : location_filtering_neighbor.verified,
                    'address' : location_filtering_neighbor_address.address,
                    'profile_picture' : location_filtering_neighbor.profile_picture,
                    'neighbor_zipcode' : location_filtering_neighbor.zipcode
                    } # events_data, variable name should be consistent across htmls with blocks
                return render(request, 'login.html', location_filter_context)
        elif location_filter_choice == 'My city':
            if location_filtering_neighbor.neighbor_id in list(Addresses.objects.all().values_list('neighbor_id', flat=True)):
                location_filtering_neighbor_address = Addresses.objects.get(neighbor_id = location_filtering_neighbor.neighbor_id)
                if location_filtering_neighbor.neighborhood_id != 0:
                    city_ad(request)
                    city_events_today_n_after = []
                    for column in Events.objects.filter(event_start_date__gte = date.today(), 
                                                        event_city = location_filtering_neighbor_address.city,
                                                        event_private = False).order_by('event_start_date',
                                                                                        'event_start_time'):
                        city_events_today_n_after.append({
                            'event_id' : column.event_id,
                            'event_name' : column.event_name,
                            'event_start_date' : column.event_start_date,
                            'event_end_date' : column.event_end_date,
                            'event_start_time' : column.event_start_time,
                            'event_end_time' : column.event_end_time,
                            'event_zipcode' : column.event_zipcode,
                            'zipcode_match' : column.event_zipcode == location_filtering_neighbor.zipcode,
                            'neighborhood_match' : column.neighborhood_id == location_filtering_neighbor.neighborhood_id,
                            'city_match' : column.event_city == location_filtering_neighbor_address.city
                            })
                    location_filter_context = {
                        'events_data' : city_events_today_n_after,
                        'neighbor_username' : location_filtering_neighbor.username,
                        'neighbor_name' : location_filtering_neighbor_address.first_name,
                        'verified' : location_filtering_neighbor.verified,
                        'address' : location_filtering_neighbor_address.address,
                        'profile_picture' : location_filtering_neighbor.profile_picture,
                        'neighbor_zipcode' : location_filtering_neighbor.zipcode
                        } # events_data, variable name should be consistent across htmls with blocks
                    return render(request, 'login.html', location_filter_context)
                city_ad(request)
                city_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(), 
                                                    event_city = location_filtering_neighbor_address.city,
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    city_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == location_filtering_neighbor.zipcode,
                        'city_match' : column.event_city == location_filtering_neighbor_address.city
                        })
                location_filter_context = {
                    'events_data' : city_events_today_n_after,
                    'neighbor_username' : location_filtering_neighbor.username,
                    'neighbor_name' : location_filtering_neighbor_address.first_name,
                    'verified' : location_filtering_neighbor.verified,
                    'address' : location_filtering_neighbor_address.address,
                    'profile_picture' : location_filtering_neighbor.profile_picture,
                    'neighbor_zipcode' : location_filtering_neighbor.zipcode
                    } # events_data, variable name should be consistent across htmls with blocks
                return render(request, 'login.html', location_filter_context)
            else:
                neighbor_location = Zipcodes.objects.get(zipcode_id = location_filtering_neighbor.zipcode)
                city_ad(request)
                city_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(), 
                                                    event_city = neighbor_location.city,
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    city_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == location_filtering_neighbor.zipcode,
                        'city_match' : column.event_city == neighbor_location.city
                        })
                location_filter_context = {
                    'events_data' : city_events_today_n_after,
                    'neighbor_username' : location_filtering_neighbor.username,
                    'neighbor_name' : None,
                    'verified' : location_filtering_neighbor.verified,
                    'address' : None,
                    'profile_picture' : location_filtering_neighbor.profile_picture,
                    'neighbor_zipcode' : location_filtering_neighbor.zipcode
                    } # events_data, variable name should be consistent across htmls with blocks
                return render(request, 'login.html', location_filter_context)
        elif location_filter_choice == 'Other':
            return render(request, 'city_search.html')

def filter_view(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today(),
                                                event_private = False).order_by('event_start_date',
                                                                                'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        view_filter_choice = request.POST.get('view_filter')
        request.session['view_filter_id'] = View_filters.objects.order_by('-view_filter_id').first().view_filter_id+1
        View_filters.objects.create(
            view_filter_id = request.session.get('view_filter_id'),
            neighbor_id = request.session.get('neighbor_id'),
            view_filter = view_filter_choice,
            view_filtered_when = datetime.today()
        )
        view_filtering_neighbor = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
        if view_filtering_neighbor.neighbor_id in list(Addresses.objects.all().values_list('neighbor_id', flat=True)):
            view_filtering_neighbor_address = Addresses.objects.get(neighbor_id = request.session.get('neighbor_id'))
            if view_filtering_neighbor.neighborhood_id != 0:
                zipcode_ad(request)
                zipcode_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                    event_zipcode = view_filtering_neighbor.zipcode,
                                                    event_private = False).order_by('event_start_date',
                                                                                    'event_start_time'):
                    zipcode_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == view_filtering_neighbor.zipcode,
                        'neighborhood_match' : column.neighborhood_id == view_filtering_neighbor.neighborhood_id,
                        'city_match' : column.event_city == view_filtering_neighbor_address.city
                        })
                cal = HTMLCalendar(calendar.SUNDAY).formatmonth(datetime.today().year,datetime.today().month)
                view_filter_context = {
                    'events_data' : zipcode_events_today_n_after,
                    'neighbor_username' : view_filtering_neighbor.username,
                    'neighbor_name' : view_filtering_neighbor_address.first_name,
                    'verified' : view_filtering_neighbor.verified,
                    'address' : view_filtering_neighbor_address.address,
                    'profile_picture' : view_filtering_neighbor.profile_picture,
                    'neighbor_zipcode' : view_filtering_neighbor.zipcode,
                    'view_filter_choice' : view_filter_choice,
                    'cal' : cal
                    } # events_data, variable name should be consistent across htmls with blocks
                return render(request, 'login.html', view_filter_context)

            zipcode_ad(request)
            zipcode_events_today_n_after = []
            for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                event_zipcode = view_filtering_neighbor_address.zipcode).order_by('event_start_date',
                                                                                                            'event_start_time'):
                zipcode_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode,
                    'zipcode_match' : column.event_zipcode == view_filtering_neighbor_address.zipcode
                    })
            cal = HTMLCalendar(calendar.SUNDAY).formatmonth(datetime.today().year,datetime.today().month)
            view_filter_context = {
                'events_data' : zipcode_events_today_n_after,
                'neighbor_username' : view_filtering_neighbor.username,
                'neighbor_name' : view_filtering_neighbor_address.first_name,
                'verified' : view_filtering_neighbor.verified,
                'address' : view_filtering_neighbor_address.address,
                'profile_picture' : view_filtering_neighbor.profile_picture,
                'neighbor_zipcode' : view_filtering_neighbor_address.zipcode,
                'view_filter_choice' : view_filter_choice,
                'cal' : cal
                } # events_data, variable name should be consistent across htmls with blocks
            return render(request, 'login.html', view_filter_context)

def filter_calendar(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                               'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        month_choice = request.POST.get('month')
        year_choice = request.POST.get('year')
        request.session['calendar_filter_id'] = Calendar_filters.objects.order_by('-calendar_filter_id').first().calendar_filter_id+1
        Calendar_filters.objects.create(
            calendar_filter_id = request.session.get('calendar_filter_id'),
            neighbor_id = request.session.get('neighbor_id'),
            month = month_choice,
            year = year_choice,
            calendar_filtered_when = datetime.today()
        )
        calendar_filtering_neighbor = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
        calendar_filtering_neighbor_address = Addresses.objects.get(neighbor_id = request.session.get('neighbor_id'))
        if calendar_filtering_neighbor_address.zipcode == None:
            unverified_ad()
            all_events_today_n_after = []
            for column in Events.objects.filter(event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                            'event_start_time'):
                all_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode,
                    'zipcode_match' : column.event_zipcode == calendar_filtering_neighbor.zipcode
                    })
            cal = HTMLCalendar(calendar.SUNDAY).formatmonth(int(year_choice), int(month_choice))
            calendar_filtering_neighbor_context = {'events_data' : all_events_today_n_after,
                                'neighbor_name' : calendar_filtering_neighbor.first_name,
                                'neighbor_username' : calendar_filtering_neighbor.username,
                                'verified' : calendar_filtering_neighbor.verified,
                                'address' : calendar_filtering_neighbor.address,
                                'profile_picture' : calendar_filtering_neighbor.profile_picture,
                                'neighbor_zipcode' : calendar_filtering_neighbor.zipcode,
                                'view_filter_choice' : 'Calendar view',
                                'cal' : cal} # events_data, variable name should be consistent across htmls with blocks
            return render(request, 'login.html', calendar_filtering_neighbor_context)
        else:
            zipcode_ad(request)
            zipcode_events_today_n_after = []
            for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                event_zipcode = calendar_filtering_neighbor_address.zipcode).order_by('event_start_date',
                                                                                                            'event_start_time'):
                zipcode_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode,
                    'zipcode_match' : column.event_zipcode == calendar_filtering_neighbor_address.zipcode
                    })
            cal = HTMLCalendar(calendar.SUNDAY).formatmonth(int(year_choice), int(month_choice))
            calendar_filter_context = {
                'events_data' : zipcode_events_today_n_after,
                'neighbor_username' : calendar_filtering_neighbor.username,
                'neighbor_name' : calendar_filtering_neighbor_address.first_name,
                'verified' : calendar_filtering_neighbor.verified,
                'address' : calendar_filtering_neighbor_address.address,
                'profile_picture' : calendar_filtering_neighbor.profile_picture,
                'neighbor_zipcode' : calendar_filtering_neighbor_address.zipcode,
                'view_filter_choice' : 'Calendar view',
                'cal' : cal
                } # events_data, variable name should be consistent across htmls with blocks
            return render(request, 'login.html', calendar_filter_context)

def filter_date(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                               'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        request.session['date_filter_id'] = Date_filters.objects.order_by('-date_filter_id').first().date_filter_id+1
        date_by_choice = request.POST.get('date_by')
        filter_date_choice = request.POST.get('filter_date')
        date_filtering_neighbor = Neighbors.objects.get(neighbor_id = request.session.get('neighbor_id'))
        date_filtering_neighbor_address = Addresses.objects.get(neighbor_id = request.session.get('neighbor_id'))
        # need to include code where if there is no filter_date_choice, returns login with note to pick a date
        if filter_date_choice == "":
            if date_filtering_neighbor_address.zipcode == None:
                unverified_ad()
                all_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                                'event_start_time'):
                    all_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == date_filtering_neighbor_address.zipcode
                        })
                date_filtering_neighbor_context = {'events_data' : all_events_today_n_after,
                                    'neighbor_name' : date_filtering_neighbor_address.first_name,
                                    'neighbor_username' : date_filtering_neighbor.username,
                                    'verified' : date_filtering_neighbor.verified,
                                    'address' : date_filtering_neighbor_address.address,
                                    'profile_picture' : date_filtering_neighbor.profile_picture,
                                    'neighbor_zipcode' : date_filtering_neighbor_address.zipcode} # events_data, variable name should be consistent across htmls with blocks
                return render(request, 'blank_date.html', date_filtering_neighbor_context)
            else:
                zipcode_ad(request)
                zipcode_events_today_n_after = []
                for column in Events.objects.filter(event_start_date__gte = date.today(),
                                                    event_zipcode = date_filtering_neighbor_address.zipcode).order_by('event_start_date',
                                                                                                            'event_start_time'):
                    zipcode_events_today_n_after.append({
                        'event_id' : column.event_id,
                        'event_name' : column.event_name,
                        'event_start_date' : column.event_start_date,
                        'event_end_date' : column.event_end_date,
                        'event_start_time' : column.event_start_time,
                        'event_end_time' : column.event_end_time,
                        'event_zipcode' : column.event_zipcode,
                        'zipcode_match' : column.event_zipcode == date_filtering_neighbor_address.zipcode
                        })
                blank_date_context = {
                    'events_data' : zipcode_events_today_n_after,
                    'neighbor_username' : date_filtering_neighbor.username,
                    'neighbor_name' : date_filtering_neighbor_address.first_name,
                    'verified' : date_filtering_neighbor.verified,
                    'address' : date_filtering_neighbor_address.address,
                    'profile_picture' : date_filtering_neighbor.profile_picture,
                    'neighbor_zipcode' : date_filtering_neighbor_address.zipcode
                }
                return render(request, 'blank_date.html', blank_date_context)
        else:
            Date_filters.objects.create(
                date_filter_id = request.session.get('date_filter_id'),
                neighbor_id = request.session.get('neighbor_id'),
                date_by = date_by_choice,
                filter_date = filter_date_choice,
                date_filtered_when = datetime.today()
            )
            if date_by_choice == 'On':
                if datetime.strptime(filter_date_choice, '%Y-%m-%d').date() < date.today():
                    return render(request, 'past_events.html')
                else:
                    if date_filtering_neighbor_address.zipcode == None:
                        if Events.objects.filter(event_start_date = filter_date_choice).first() == None:
                            ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                                                <br><br>Click here to plan an event to host.
                                                <br><br>Want to host an event but not sure how? Click here!"""
                            ad_name = 'No events? Create one!'
                            ad_end_time = '23:59:59'
                            Events.objects.create(
                                event_id = Events.objects.order_by('-event_id').first().event_id+1,
                                neighbor_id = 1,
                                event_description = ad_description,
                                event_name = ad_name,
                                event_start_date = filter_date_choice,
                                event_end_date = filter_date_choice,
                                event_start_time = datetime.today().time(),
                                event_end_time = ad_end_time,
                                event_reoccur = 'No',
                                event_address = 'Your street number and name here',
                                event_city = 'Your city here',
                                event_state = 'Your state here',
                                event_zipcode = 'Your zipcode here',
                                event_public = False,
                                event_invitees = 'none',
                                evented_when = datetime.today()
                            )
                        all_events_on = []
                        for column in Events.objects.filter(event_start_date = filter_date_choice).order_by('event_start_date',
                                                                                                            'event_start_time'):
                            all_events_on.append({
                                'event_id' : column.event_id,
                                'event_name' : column.event_name,
                                'event_start_date' : column.event_start_date,
                                'event_end_date' : column.event_end_date,
                                'event_start_time' : column.event_start_time,
                                'event_end_time' : column.event_end_time,
                                'event_zipcode' : column.event_zipcode,
                                'zipcode_match' : column.event_zipcode == date_filtering_neighbor_address.zipcode
                                })
                        date_filtering_neighbor_context = {'events_data' : all_events_on,
                                            'neighbor_name' : date_filtering_neighbor_address.first_name,
                                            'neighbor_username' : date_filtering_neighbor.username,
                                            'verified' : date_filtering_neighbor.verified,
                                            'address' : date_filtering_neighbor_address.address,
                                            'profile_picture' : date_filtering_neighbor.profile_picture,
                                            'neighbor_zipcode' : date_filtering_neighbor_address.zipcode} # events_data, variable name should be consistent across htmls with blocks
                        return render(request, 'login.html', date_filtering_neighbor_context)
                    else:
                        if Events.objects.filter(event_start_date = filter_date_choice,
                                                event_zipcode = date_filtering_neighbor_address.zipcode).first() == None:
                            ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                                                <br><br>Click here to plan an event to host.
                                                <br><br>Want to host an event but not sure how? Click here!"""
                            ad_name = 'No events? Create one!'
                            ad_end_time = '23:59:59'
                            Events.objects.create(
                                event_id = Events.objects.order_by('-event_id').first().event_id+1,
                                neighbor_id = 1,
                                event_description = ad_description,
                                event_name = ad_name,
                                event_start_date = filter_date_choice,
                                event_end_date = filter_date_choice,
                                event_start_time = datetime.today().time(),
                                event_end_time = ad_end_time,
                                event_reoccur = 'No',
                                event_address = 'Your street number and name here',
                                event_city = date_filtering_neighbor.city,
                                event_state = date_filtering_neighbor.state,
                                event_zipcode = date_filtering_neighbor_address.zipcode, # need to put neighbor's zipcode here
                                event_public = False,
                                event_invitees = 'none',
                                evented_when = datetime.today()
                            )
                        zipcode_events_on = []
                        for column in Events.objects.filter(event_start_date = filter_date_choice,
                                                            event_zipcode = date_filtering_neighbor_address.zipcode).order_by('event_start_date', 
                                                                                                                    'event_start_time'):
                            zipcode_events_on.append({
                                'event_id' : column.event_id,
                                'event_name' : column.event_name,
                                'event_start_date' : column.event_start_date,
                                'event_end_date' : column.event_end_date,
                                'event_start_time' : column.event_start_time,
                                'event_end_time' : column.event_end_time,
                                'event_zipcode' : column.event_zipcode,
                                'zipcode_match' : column.event_zipcode == date_filtering_neighbor_address.zipcode
                                })
                        zipcode_events_on_context = {
                            'events_data' : zipcode_events_on,
                            'neighbor_username' : date_filtering_neighbor.username,
                            'neighbor_name' : date_filtering_neighbor_address.first_name,
                            'verified' : date_filtering_neighbor.verified,
                            'address' : date_filtering_neighbor_address.address,
                            'profile_picture' : date_filtering_neighbor.profile_picture,
                            'neighbor_zipcode' : date_filtering_neighbor_address.zipcode
                            } # events_data, variable name should be consistent across htmls with blocks
                        return render(request, 'login.html', zipcode_events_on_context)
            elif date_by_choice == 'Before':
                if datetime.strptime(filter_date_choice, '%Y-%m-%d').date() < date.today():
                    return render(request, 'past_events.html')
                else: # need to rewrite for before!
                    if date_filtering_neighbor_address.zipcode == None:
                        if Events.objects.filter(event_start_date__range=(date.today(),filter_date_choice)).first() == None:
                            ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                                                <br><br>Click here to plan an event to host.
                                                <br><br>Want to host an event but not sure how? Click here!"""
                            ad_name = 'No events? Create one!'
                            ad_end_time = '23:59:59'
                            Events.objects.create(
                                event_id = Events.objects.order_by('-event_id').first().event_id+1,
                                neighbor_id = 1,
                                event_description = ad_description,
                                event_name = ad_name,
                                event_start_date = filter_date_choice,
                                event_end_date = filter_date_choice,
                                event_start_time = datetime.today().time(),
                                event_end_time = ad_end_time,
                                event_reoccur = 'No',
                                event_address = 'Your street number and name here',
                                event_city = 'Your city here',
                                event_state = 'Your state here',
                                event_zipcode = 'Your zipcode here',
                                event_public = False,
                                event_invitees = 'none',
                                evented_when = datetime.today()
                            )
                        all_events_before = []
                        for column in Events.objects.filter(event_start_date__range=(date.today(),filter_date_choice)).order_by('event_start_date',
                                                                                                                                'event_start_time'):
                            all_events_before.append({
                                'event_id' : column.event_id,
                                'event_name' : column.event_name,
                                'event_start_date' : column.event_start_date,
                                'event_end_date' : column.event_end_date,
                                'event_start_time' : column.event_start_time,
                                'event_end_time' : column.event_end_time,
                                'event_zipcode' : column.event_zipcode,
                                'zipcode_match' : column.event_zipcode == date_filtering_neighbor_address.zipcode
                                })
                        date_filtering_neighbor_context = {'events_data' : all_events_before,
                                            'neighbor_name' : date_filtering_neighbor_address.first_name,
                                            'neighbor_username' : date_filtering_neighbor.username,
                                            'verified' : date_filtering_neighbor.verified,
                                            'address' : date_filtering_neighbor_address.address,
                                            'profile_picture' : date_filtering_neighbor.profile_picture,
                                            'neighbor_zipcode' : date_filtering_neighbor_address.zipcode} # events_data, variable name should be consistent across htmls with blocks
                        return render(request, 'login.html', date_filtering_neighbor_context)
                    else:
                        if Events.objects.filter(event_start_date__range=(date.today(),filter_date_choice),
                                                event_zipcode = date_filtering_neighbor_address.zipcode).first() == None:
                            ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                                                <br><br>Click here to plan an event to host.
                                                <br><br>Want to host an event but not sure how? Click here!"""
                            ad_name = 'No events? Create one!'
                            ad_end_time = '23:59:59'
                            Events.objects.create(
                                event_id = Events.objects.order_by('-event_id').first().event_id+1,
                                neighbor_id = 1,
                                event_description = ad_description,
                                event_name = ad_name,
                                event_start_date = filter_date_choice,
                                event_end_date = filter_date_choice,
                                event_start_time = datetime.today().time(),
                                event_end_time = ad_end_time,
                                event_reoccur = 'No',
                                event_address = 'Your street number and name here',
                                event_city = date_filtering_neighbor.city,
                                event_state = date_filtering_neighbor.state,
                                event_zipcode = date_filtering_neighbor_address.zipcode,
                                event_public = False,
                                event_invitees = 'none',
                                evented_when = datetime.today()
                            )
                        zipcode_events_before = []
                        for column in Events.objects.filter(event_start_date__range=(date.today(),filter_date_choice),
                                                            event_zipcode = date_filtering_neighbor_address.zipcode).order_by('event_start_date', 
                                                                                                                    'event_start_time'):
                            zipcode_events_before.append({
                                'event_id' : column.event_id,
                                'event_name' : column.event_name,
                                'event_start_date' : column.event_start_date,
                                'event_end_date' : column.event_end_date,
                                'event_start_time' : column.event_start_time,
                                'event_end_time' : column.event_end_time,
                                'event_zipcode' : column.event_zipcode,
                                'zipcode_match' : column.event_zipcode == date_filtering_neighbor_address.zipcode
                                })
                        zipcode_events_before_context = {
                            'events_data' : zipcode_events_before,
                            'neighbor_username' : date_filtering_neighbor.username,
                            'neighbor_name' : date_filtering_neighbor_address.first_name,
                            'verified' : date_filtering_neighbor.verified,
                            'address' : date_filtering_neighbor_address.address,
                            'profile_picture' : date_filtering_neighbor.profile_picture,
                            'neighbor_zipcode' : date_filtering_neighbor_address.zipcode
                            } # events_data, variable name should be consistent across htmls with blocks
                        return render(request, 'login.html', zipcode_events_before_context)
            elif date_by_choice == 'After':
                if date_filtering_neighbor_address.zipcode == None:
                    if Events.objects.filter(event_start_date__gt = filter_date_choice).first() == None:
                        ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                                            <br><br>Click here to plan an event to host.
                                            <br><br>Want to host an event but not sure how? Click here!"""
                        ad_name = 'No events? Create one!'
                        ad_end_time = '23:59:59'
                        Events.objects.create(
                            event_id = Events.objects.order_by('-event_id').first().event_id+1,
                            neighbor_id = 1,
                            event_description = ad_description,
                            event_name = ad_name,
                            event_start_date = filter_date_choice,
                            event_end_date = filter_date_choice,
                            event_start_time = datetime.today().time(),
                            event_end_time = ad_end_time,
                            event_reoccur = 'No',
                            event_address = 'Your street number and name here',
                            event_city = 'Your city here',
                            event_state = 'Your state here',
                            event_zipcode = 'Your zipcode here',
                            event_public = False,
                            event_invitees = 'none',
                            evented_when = datetime.today()
                        )
                    all_events_after = []
                    for column in Events.objects.filter(event_start_date__gt = filter_date_choice).order_by('event_start_date',
                                                                                                            'event_start_time'):
                        all_events_after.append({
                            'event_id' : column.event_id,
                            'event_name' : column.event_name,
                            'event_start_date' : column.event_start_date,
                            'event_end_date' : column.event_end_date,
                            'event_start_time' : column.event_start_time,
                            'event_end_time' : column.event_end_time,
                            'event_zipcode' : column.event_zipcode,
                            'zipcode_match' : column.event_zipcode == date_filtering_neighbor_address.zipcode
                            })
                    date_filtering_neighbor_context = {'events_data' : all_events_after,
                                        'neighbor_name' : date_filtering_neighbor_address.first_name,
                                        'neighbor_username' : date_filtering_neighbor.username,
                                        'verified' : date_filtering_neighbor.verified,
                                        'address' : date_filtering_neighbor_address.address,
                                        'profile_picture' : date_filtering_neighbor.profile_picture,
                                        'neighbor_zipcode' : date_filtering_neighbor_address.zipcode} # events_data, variable name should be consistent across htmls with blocks
                    return render(request, 'login.html', date_filtering_neighbor_context)
                else:
                    if Events.objects.filter(event_start_date__gt = filter_date_choice,
                                            event_zipcode = date_filtering_neighbor_address.zipcode).first() == None:
                        ad_description = """Neighborhost relies on proactive neighbors like you to build the kinds of communities we've dreamed of.
                                            <br><br>Click here to plan an event to host.
                                            <br><br>Want to host an event but not sure how? Click here!"""
                        ad_name = 'No events? Create one!'
                        ad_end_time = '23:59:59'
                        Events.objects.create(
                            event_id = Events.objects.order_by('-event_id').first().event_id+1,
                            neighbor_id = 1,
                            event_description = ad_description,
                            event_name = ad_name,
                            event_start_date = filter_date_choice,
                            event_end_date = filter_date_choice,
                            event_start_time = datetime.today().time(),
                            event_end_time = ad_end_time,
                            event_reoccur = 'No',
                            event_address = 'Your street number and name here',
                            event_city = date_filtering_neighbor.city,
                            event_state = date_filtering_neighbor.state,
                            event_zipcode = date_filtering_neighbor_address.zipcode,
                            event_public = False,
                            event_invitees = 'none',
                            evented_when = datetime.today()
                        )
                    zipcode_events_after = []
                    for column in Events.objects.filter(event_start_date__gte = filter_date_choice,
                                                        event_zipcode = date_filtering_neighbor_address.zipcode).order_by('event_start_date', 
                                                                                                                'event_start_time'):
                        zipcode_events_after.append({
                            'event_id' : column.event_id,
                            'event_name' : column.event_name,
                            'event_start_date' : column.event_start_date,
                            'event_end_date' : column.event_end_date,
                            'event_start_time' : column.event_start_time,
                            'event_end_time' : column.event_end_time,
                            'event_zipcode' : column.event_zipcode,
                            'zipcode_match' : column.event_zipcode == date_filtering_neighbor_address.zipcode
                            })
                    zipcode_events_after_context = {
                        'events_data' : zipcode_events_after,
                        'neighbor_username' : date_filtering_neighbor.username,
                        'neighbor_name' : date_filtering_neighbor_address.first_name,
                        'verified' : date_filtering_neighbor.verified,
                        'address' : date_filtering_neighbor_address.address,
                        'profile_picture' : date_filtering_neighbor.profile_picture,
                        'neighbor_zipcode' : date_filtering_neighbor_address.zipcode
                        } # events_data, variable name should be consistent across htmls with blocks
                    return render(request, 'login.html', zipcode_events_after_context)

def view_event_from_login(request): #separate view event for signed out folks
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                               'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        request.session['event_view_id'] = Event_views.objects.order_by('-event_view_id').first().event_view_id+1
        request.session['event_id'] = request.POST.get('event_id')
        Event_views.objects.create(
            event_view_id = request.session.get('event_view_id'),
            neighbor_id = request.session.get('neighbor_id'),
            event_id = request.session.get('event_id'),
            event_viewed_when = datetime.today()
        )
        event_query = Events.objects.get(event_id = request.session.get('event_id'))
        event_planner = Neighbors.objects.get(neighbor_id = event_query.neighbor_id)
        event_planner_address = Addresses.objects.get(neighbor_id = event_query.neighbor_id)
        event_viewer_is_event_planner = event_query.neighbor_id == request.session.get('neighbor_id')
        event_planning_context = {
            'event_name' : event_query.event_name,
            'event_description' : event_query.event_description,
            'event_start_date' : event_query.event_start_date,
            'event_end_date' : event_query.event_end_date,
            'event_start_time' : event_query.event_start_time,
            'event_end_time' : event_query.event_end_time,
            'event_description' : event_query.event_description,
            'event_address' : event_query.event_address,
            'event_city' : event_query.event_city,
            'event_state' : event_query.event_state,
            'event_zipcode' : event_query.event_zipcode,
            'event_planner_name' : event_planner_address.first_name + " " + event_planner_address.last_name,
            'event_planner_username' : event_planner.username, # need to add logic where if users are not friends, can only see username
            'event_viewer_is_event_planner' : event_viewer_is_event_planner,
            'event_planner_id' : event_query.neighbor_id
        }
        return render(request, 'events.html', event_planning_context) # needs to redirect to the event page

def friend_profile(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                               'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        request.session['friend_id'] = request.POST.get('friend_id')
        Friend_views.objects.create(
            friend_view_id = Friend_views.objects.order_by('-friend_view_id').first().friend_view_id+1,
            neighbor_id = request.session.get('neighbor_id'),
            friend_id = request.session.get('friend_id'),
            friend_viewed_when = datetime.today()
        )
        friend_query = Neighbors.objects.get(neighbor_id = request.session.get('friend_id'))
        friend_query_address = Addresses.objects.get(neighbor_id = request.session.get('friend_id'))
        neighbor_query = Neighbors.objects.filter(neighbor_id = request.session.get('neighbor_id'))
        neighbor_query_address = Addresses.objects.filter(neighbor_id = request.session.get('neighbor_id'))
        friend_events = []
        for column in Events.objects.filter(neighbor_id = request.session.get('friend_id'),
                                            event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                           'event_start_time'):
            friend_events.append({
                'event_id' : column.event_id,
                'event_name' : column.event_name,
                'event_start_date' : column.event_start_date,
                'event_end_date' : column.event_end_date,
                'event_start_time' : column.event_start_time,
                'event_end_time' : column.event_end_time,
                'event_zipcode' : column.event_zipcode,
                'event_public' : column.event_public,
                'zipcode_match' : column.event_zipcode == neighbor_query_address.first().zipcode
            })
        stranger_events = []
        for column in Events.objects.filter(neighbor_id = request.session.get('friend_id'),
                                            event_start_date__gte = date.today(),
                                            event_public = True).order_by('event_start_date',
                                                                          'event_start_time'):
            stranger_events.append({
                'event_id' : column.event_id,
                'event_name' : column.event_name,
                'event_start_date' : column.event_start_date,
                'event_end_date' : column.event_end_date,
                'event_start_time' : column.event_start_time,
                'event_end_time' : column.event_end_time,
                'event_zipcode' : column.event_zipcode,
                'event_public' : column.event_public,
                'zipcode_match' : column.event_zipcode == neighbor_query_address.first().zipcode
            })
        friend_view_context = {
            'friend_events_data' : friend_events,
            'stranger_events_data' : stranger_events,
            'profile_name' : friend_query_address.first_name + " " + friend_query_address.last_name,
            'profile_username' : friend_query.username,
            'profile_id' : request.session.get('friend_id'),
            'profile_picture' : friend_query.profile_picture,
            'neighbor_id' : str(neighbor_query.first().neighbor_id),
            'neighbor_friends_list' : ",".join(str(list(Friends.objects.filter(neighbor_id = request.session.get('neighbor_id')).values_list('friend_id', flat=True)))),
            'friend_request_list' : ",".join(str(list(Friend_requests.objects.filter(neighbor_id = request.session.get('neighbor_id')).values_list('friend_id', flat=True))))
        }
        print(list(Friends.objects.filter(neighbor_id = request.session.get('neighbor_id')).values_list('friend_id', flat=True)))
        return render(request,'profile.html', friend_view_context)

def friend_request(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                               'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        request.session['friend_id'] = request.POST.get('friend_id')
        
        if request.session.get('friend_id') in list(Friends.objects.filter(neighbor_id = request.session.get('neighbor_id')).values_list('friend_id', flat=True)):
            return render(request, 'already_friends.html') # should show, already friends html
        else:
            Friend_requests.objects.create(
                friend_request_id = Friend_requests.objects.order_by('-friend_request_id').first().friend_request_id+1,
                neighbor_id = request.session.get('neighbor_id'),
                friend_id = request.session.get('friend_id'),
                friend_requested_when = datetime.today()
            )
            friend_query = Neighbors.objects.get(neighbor_id = request.session.get('friend_id'))
            friend_query_address = Addresses.objects.get(neighbor_id = request.session.get('friend_id'))
            neighbor_query = Neighbors.objects.filter(neighbor_id = request.session.get('neighbor_id'))
            neighbor_query_address = Addresses.objects.filter(neighbor_id = request.session.get('neighbor_id'))
            friend_events = []
            for column in Events.objects.filter(neighbor_id = request.session.get('friend_id'),
                                                event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                            'event_start_time'):
                friend_events.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode,
                    'event_public' : column.event_public,
                    'zipcode_match' : column.event_zipcode == neighbor_query_address.first().zipcode
                })
            stranger_events = []
            for column in Events.objects.filter(neighbor_id = request.session.get('friend_id'),
                                                event_start_date__gte = date.today(),
                                                event_public = True).order_by('event_start_date',
                                                                            'event_start_time'):
                stranger_events.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode,
                    'event_public' : column.event_public,
                    'zipcode_match' : column.event_zipcode == neighbor_query_address.first().zipcode
                })
            friend_view_context = {
                'friend_events_data' : friend_events,
                'stranger_events_data' : stranger_events,
                'profile_name' : friend_query_address.first_name + " " + friend_query_address.last_name,
                'profile_username' : friend_query.username,
                'profile_id' : request.session.get('friend_id'),
                'profile_picture' : friend_query.profile_picture,
                'neighbor_id' : str(neighbor_query.first().neighbor_id),
                'neighbor_friends_list' : ",".join(str(list(Friends.objects.filter(neighbor_id = request.session.get('neighbor_id')).values_list('friend_id', flat=True)))),
                'friend_request_list' : ",".join(str(list(Friend_requests.objects.filter(neighbor_id = request.session.get('neighbor_id')).values_list('friend_id', flat=True))))
            }
            return render(request, 'friend_requested.html', friend_view_context)

def signout(request):
    if request.method == 'POST':
        try:
            request.session['neighbor_id']
        except KeyError:
            ad()
            # >= today's date events
            public_events_today_n_after = []
            for column in Events.objects.filter(event_public = True, 
                                                event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                               'event_start_time'):
                public_events_today_n_after.append({
                    'event_id' : column.event_id,
                    'event_name' : column.event_name,
                    'event_start_date' : column.event_start_date,
                    'event_end_date' : column.event_end_date,
                    'event_start_time' : column.event_start_time,
                    'event_end_time' : column.event_end_time,
                    'event_zipcode' : column.event_zipcode
                    })
            relogin_context = {'events_data' : public_events_today_n_after,
                               'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                               'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))} # events_data, variable name should be consistent across htmls?
            return render(request, 'relogin.html', relogin_context)
        
        Signouts.objects.create(
            signout_id = Signouts.objects.order_by('-signout_id').first().signout_id+1,
            neighbor_id = request.session.get('neighbor_id'),
            signout_when = datetime.today()
        )
        ad()
        public_events_today_n_after = []
        for column in Events.objects.filter(event_public = True, 
                                            event_start_date__gte = date.today()).order_by('event_start_date',
                                                                                           'event_start_time'):
            public_events_today_n_after.append({
                'event_id' : column.event_id,
                'event_name' : column.event_name,
                'event_start_date' : column.event_start_date,
                'event_end_date' : column.event_end_date,
                'event_start_time' : column.event_start_time,
                'event_end_time' : column.event_end_time,
                'event_zipcode' : column.event_zipcode
                })
        del request.session['neighbor_id']
        signout_context = {'events_data' : public_events_today_n_after,
                           'existing_usernames' : list(Neighbors.objects.all().values_list('username',flat=True)),
                           'existing_emails' : list(Neighbors.objects.all().values_list('email',flat=True))}
        return render(request, 'signout.html', signout_context)