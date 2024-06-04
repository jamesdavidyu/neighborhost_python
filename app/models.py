from django.db import models
from django.core.validators import MinLengthValidator
from datetime import datetime

# Create your models here.
# database schema
class Zipcodes(models.Model):
    zipcode_id              = models.CharField(max_length=5, primary_key=True, unique=True)
    city                    = models.CharField(max_length=27)
    state                   = models.CharField(max_length=35)

class Neighborhoods(models.Model):
    neighborhood_id         = models.IntegerField(primary_key=True, unique=True, default=0)
    neighborhood            = models.CharField(max_length=255, default='Not assigned')
    neighborhood_found_when = models.DateTimeField(default=datetime.today())

class Neighbors(models.Model):
    neighbor_id             = models.IntegerField(primary_key=True, unique=True)
    signup_datetime         = models.DateTimeField()
    username                = models.CharField(max_length=255)
    email                   = models.EmailField(max_length=255)
    password                = models.CharField(validators=[MinLengthValidator(8)])
    zipcode                 = models.CharField(max_length=17, default='Your zipcode here')
    verified                = models.BooleanField(default=False)
    profile_picture         = models.CharField(default='none') # move to separate table
    neighborhood            = models.ForeignKey(Neighborhoods, on_delete=models.CASCADE, default=0)

class Addresses(models.Model):
    address_id              = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    first_name              = models.CharField(max_length=255)
    last_name               = models.CharField(max_length=255)
    address                 = models.CharField(max_length=50)
    city                    = models.CharField(max_length=27)
    state                   = models.CharField(max_length=35)
    neighborhood            = models.ForeignKey(Neighborhoods, on_delete=models.CASCADE, default=0)
    
class Events(models.Model):
    event_id                = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    event_description       = models.CharField(max_length=1000)
    event_name              = models.CharField(max_length=50)
    event_start_date        = models.DateField()
    event_end_date          = models.DateField()
    event_start_time        = models.TimeField()
    event_end_time          = models.TimeField()
    event_reoccur           = models.CharField(max_length=14)
    event_address           = models.CharField(max_length=50)
    event_city              = models.CharField(max_length=27)
    event_state             = models.CharField(max_length=35)
    event_zipcode           = models.CharField(max_length=17)
    event_public            = models.BooleanField()
    event_private           = models.BooleanField(default=False)
    event_invitees          = models.TextField()
    evented_when            = models.DateTimeField()
    neighborhood            = models.ForeignKey(Neighborhoods, on_delete=models.CASCADE, default=0)

class Verifications(models.Model):
    verification_id         = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    verification_code       = models.CharField(max_length=6)
    code_generated_when     = models.DateTimeField()

class Friends(models.Model):
    friend_id               = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    friend_status           = models.CharField(max_length=8)
    friended_when           = models.DateTimeField()

class Friend_requests(models.Model):
    friend_request_id       = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    friend_id               = models.IntegerField()
    friend_requested_when   = models.DateTimeField()

# tracking user activity tables

class Logins(models.Model):
    login_id                = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    login_datetime          = models.DateTimeField()
    login_ip                = models.GenericIPAddressField()

class Home_clicks(models.Model):
    home_click_id           = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    home_clicked_when       = models.DateTimeField()

class Verification_skips(models.Model):
    skip_id                 = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    skipped_when            = models.DateTimeField()

class Verify_laters(models.Model):
    later_id                = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    later_when              = models.DateTimeField()

class Verifiers(models.Model):
    verifier_id             = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    verifier_when           = models.DateTimeField()

class Friend_checks(models.Model):
    friend_check_id         = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    friend_check_when       = models.DateTimeField()

class Location_filters(models.Model):
    location_filter_id      = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    location_filter         = models.CharField(max_length=15)
    location_filtered_when  = models.DateTimeField()

class View_filters(models.Model):
    view_filter_id          = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    view_filter             = models.CharField(max_length=13)
    view_filtered_when      = models.DateTimeField()

class Calendar_filters(models.Model):
    calendar_filter_id      = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    month                   = models.IntegerField()
    year                    = models.IntegerField()
    calendar_filtered_when  = models.DateTimeField()

class Date_filters(models.Model):
    date_filter_id          = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    date_by                 = models.CharField(max_length=6)
    filter_date             = models.DateField()
    date_filtered_when      = models.DateTimeField()

class Event_views(models.Model):
    event_view_id           = models.IntegerField(primary_key=True, unique=True)
    event                   = models.ForeignKey(Events, on_delete=models.CASCADE)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    event_viewed_when       = models.DateTimeField()

class Friend_views(models.Model):
    friend_view_id          = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    friend_id               = models.IntegerField()
    friend_viewed_when      = models.DateTimeField()

class Signouts(models.Model):
    signout_id              = models.IntegerField(primary_key=True, unique=True)
    neighbor                = models.ForeignKey(Neighbors, on_delete=models.CASCADE)
    signout_when            = models.DateTimeField()

class Visits(models.Model):
    visit_id                = models.IntegerField(primary_key=True, unique=True)
    visit_ip                = models.GenericIPAddressField()
    visited_when            = models.DateTimeField()