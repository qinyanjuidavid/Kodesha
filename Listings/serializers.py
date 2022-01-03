from rest_framework.serializers import ModelSerializer
from Listings.models import Property_Type, Property


class PropertyTypeSerializer(ModelSerializer):
    class Meta:
        model = Property_Type
        fields = ('type', 'added_by')


class PropertySerializer(PropertyTypeSerializer):
    # property_type = PropertyTypeSerializer(read_only=True, many=True)

    class Meta:
        model = Property
        fields = ("id", "property_title", "status", "property_type",
                  "price", "rooms", "featured",
                  "bathrooms", "balcony", "bed_rooms", "garage", "area",
                  "property_gallery", "rented", "sold", "like", "video",
                  "address", "city", "postal_code", "longitude", "latitude",
                  "description", "building_age",
                  "floor_plan", "parking", "air_conditioning",
                  "swimming_pool", "laundry_room", "window_covering",
                  "central_heating", "alarm",
                  "wifi", "gym", "dining_room", "added_by"
                  )
        read_only_fields = ("id", "featured")
