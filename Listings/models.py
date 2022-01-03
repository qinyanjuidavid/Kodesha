from django.db import models
from django.db.models.fields import PositiveIntegerField
from accounts.models import User, TrackingModel, Administrator
from django.utils.translation import gettext as _


class Property_Type(TrackingModel):
    type = models.CharField(_("Property Type"), max_length=89, unique=True)
    added_by = models.ForeignKey(Administrator, on_delete=models.CASCADE)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = "Property Type"


class Property(TrackingModel):
    property_status_choice = (
        ("For Rent", "For Rent"),
        ("For Sale", "For Sale")
    )
    building_age_choice = (
        ("0-1 Years", "0-1 Years"),
        ("2-5 Years", "2-5 Years"),
        ("6-10 Years", "6-10 Years"),
        ("11-15 Years", "11-15 Years"),
        ("16+ Years", "16+ Years")
    )
    property_title = models.CharField(_("Property title"), max_length=90)
    status = models.CharField(_("Property status"),
                              max_length=20, choices=property_status_choice)
    property_type = models.ForeignKey(
        Property_Type, related_name="types", on_delete=models.CASCADE)
    price = models.FloatField(_("price"), default=0.00)
    rooms = models.PositiveIntegerField(_("rooms"), default=1)
    bathrooms = models.PositiveIntegerField(_("bathrooms"), default=1)
    balcony = models.PositiveIntegerField(_("balcony"), blank=True, null=True)
    bed_rooms = models.PositiveIntegerField(_("bedrooms"), default=1)
    garage = models.PositiveIntegerField(_("garage"), blank=True, null=True)
    area = models.CharField(_("Area"), max_length=18, help_text="SqFt")
    property_gallery = models.ImageField(
        _("property gallery"), upload_to="property/")
    rented = models.BooleanField(_("rented"), default=False)
    sold = models.BooleanField(_("sold"), default=False)
    like = models.ManyToManyField(User, related_name="likes", blank=True)
    video = models.FileField(upload_to="video/", blank=True, null=True)
    address = models.CharField(_("address"), max_length=56)
    city = models.CharField(_("City/Town"), max_length=57)
    postal_code = models.CharField(_("Postal code"), max_length=15)
    longitude = models.FloatField(_("longitude"), default=31.67)
    latitude = models.FloatField(_("latitude"), default=0.00)
    description = models.TextField(
        _("Detailed Information"), blank=True, null=True)
    building_age = models.CharField(
        _("Building age"), choices=building_age_choice, max_length=56)
    floor_plan = models.ImageField(
        _("floor plan"), upload_to="building plan", blank=True, null=True)
    parking = models.BooleanField(_("parking"), default=False)
    air_conditioning = models.BooleanField(_("air Condition"), default=False)
    swimming_pool = models.BooleanField(_("swimming pool"), default=False)
    laundry_room = models.BooleanField(_("laundry room"), default=False)
    window_covering = models.BooleanField(_("window covering"), default=False)
    central_heating = models.BooleanField(_("central heating"), default=False)
    alarm = models.BooleanField(_("alarm"), default=False)
    wifi = models.BooleanField(_("wifi"), default=False)
    gym = models.BooleanField(_("gym"), default=False)
    dining_room = models.BooleanField(_("dining_room"), default=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.property_title
