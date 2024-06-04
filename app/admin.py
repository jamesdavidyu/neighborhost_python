from django.contrib import admin

# Register your models here.
from .models import Neighbors
from .models import Logins
from .models import Events
from .models import Verification_skips
from .models import Verify_laters
from .models import Verifiers
from .models import Friend_checks
from .models import Signouts

admin.site.register(Neighbors)
admin.site.register(Logins)
admin.site.register(Events)
admin.site.register(Verification_skips)
admin.site.register(Verify_laters)
admin.site.register(Verifiers)
admin.site.register(Friend_checks)
admin.site.register(Signouts)