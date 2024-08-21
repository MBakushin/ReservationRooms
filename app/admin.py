from fastapi_admin.app import app as admin_app
from fastapi_admin.models import AbstractAdmin
from fastapi_admin.resources import ModelAdmin
from fastapi_admin import Admin

class RoomAdmin(ModelAdmin):
    model = models.Room

class PeerAdmin(ModelAdmin):
    model = models.Peer

class BookingAdmin(ModelAdmin):
    model = models.Booking

admin = Admin(app=admin_app)
admin.add_view(RoomAdmin)
admin.add_view(PeerAdmin)
admin.add_view(BookingAdmin)

# Initialize FastAPI Admin
app = FastAPI()
app.mount("/admin", admin_app)
