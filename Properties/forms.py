from django.forms import ModelForm
from Properties.models import Property_Type,Property



class PropertySubmissionForm(ModelForm):
    class Meta:
        model=Property
        fields=("property_title","status","property_type","price","area","rooms","bathrooms","balcony",
        "garage","address","city","postal_code","description","building_age","bed_rooms","parking","air_conditioning",
        "swimming_pool","laundry_room","window_covering","central_heating","alarm","wifi","gym","dining_room"
        )