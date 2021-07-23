from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.hashers import PBKDF2PasswordHasher as hasher, CryptPasswordHasher as crypt
from rest_framework.authtoken.models import Token
from datetime import datetime, date, timedelta
from PIL import Image


class BaseModel(models.Model):
    class Meta:
        abstract = True
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(BaseModel):
    name = models.CharField(max_length=500,default="NO DATA")
    url = models.SlugField(max_length=500, unique=True)
    sku = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=100, default='disponible')


class ProductPrice(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    normal_price = models.FloatField(default=0.00)
    daily_price = models.FloatField(default=0.00)
    special_price = models.FloatField(default=0.00)

class Store(BaseModel):
    name = models.CharField(max_length=100)
    base_url = models.SlugField(max_length=100)

class GenericProductDetail(BaseModel):
    """
    this model should be used for generic purposes
    """
    class Meta:
        abstract = True
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    meta_details = models.TextField(default="{}")
    store = models.ForeignKey(Store, on_delete=models.CASCADE,
                              default=1)


class NeveraProductDetail(GenericProductDetail):
    brand = models.CharField(max_length=500, default="NO DATA")
    reference = models.CharField(max_length=500,default="NO DATA")
    frosting_technology = models.CharField(max_length=500,default="NO DATA")
    net_total_capacity  = models.FloatField(default=0.0)
    brute_total_capacity = models.FloatField(default=0.0)
    net_refrigerator_capacity  = models.FloatField(default=0.0)
    net_freezer_capacity  = models.FloatField(default=0.0)
    water_dispenser = models.CharField(max_length=500,default="NO DATA")
    water_dispenser_type  = models.CharField(max_length=500,default="NO DATA")
    panel_control_type = models.CharField(max_length=500,default="NO DATA")
    panel_control_localization = models.CharField(max_length=500,default="NO DATA")
    door_amount = models.CharField(max_length=500,default="NO DATA")
    trays_material = models.CharField(max_length=500,default="NO DATA")
    dimensions = models.CharField(max_length=300)
    inverter = models.CharField(max_length=500,default="NO DATA")
    compressor_type = models.CharField(max_length=500,default="NO DATA")
    ice_maker = models.CharField(max_length=500,default="NO DATA")
    ice_maker_type = models.CharField(max_length=500,default="NO DATA")
    gama_color = models.CharField(max_length=500,default="NO DATA")
    voltage = models.CharField(max_length=500,default="NO DATA")
    min_energy_consumption = models.CharField(max_length=500,default="NO DATA")
    power_efficiency = models.CharField(max_length=500,default="NO DATA")
    warranty = models.CharField(max_length=500,default="NO DATA")
    compressor_warranty = models.CharField(max_length=500,default="NO DATA")
    contact  = models.CharField(max_length=500,default="NO DATA")
    other_details = models.TextField(default="")
    tips = models.TextField(default="")
    # new fields!!
    contact_phone_installation = models.CharField(max_length=500,default="NO DATA")
    product_design = models.CharField(max_length=500,default="NO DATA")
    door_type_nevecon = models.CharField(max_length=500, default="NO DATA")
    connectivity_options = models.CharField(max_length=500, default="NO DATA")
    element_included = models.CharField(max_length=500, default="NO DATA")
    maker_warranty = models.CharField(max_length=500, default="NO DATA")
    functional_duality = models.CharField(max_length=500, default="NO DATA")
    color_tone = models.CharField(max_length=500, default="NO DATA")
    line_model_reference = models.CharField(max_length=500, default="NO DATA")
    dimension_cm_width = models.CharField(max_length=500, default="NO DATA")
    dimension_cm_height = models.CharField(max_length=500, default="NO DATA")
    dimension_cm_deepening = models.CharField(max_length=500, default="NO DATA")
    all_dimensions_cm = models.CharField(max_length=500, default="NO DATA")



class ProductImage(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    img = models.ImageField()
    img_url = models.SlugField(max_length=300)

    def save(self, *args, **kwargs):
        """
          saves the new object in the database and modifies the image options here
          it overrides some of the behaviors from the parent method.
          :param args: list
          :param kwargs: dict
          :return: None
        """
        pic_size = (800, 800)
        img = Image.open(self.img.name)
        output_size = pic_size
        img.thumbnail(output_size)
        # print(self.img.name)
        img.save(self.img.name)
        super().save()


class ProductReview(BaseModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    total_qualification = models.FloatField(default=0.00)


class ReviewDetail(BaseModel):
    review = models.ForeignKey(ProductReview,on_delete=models.CASCADE)
    qualification = models.FloatField(default=0.00)
    comment = models.TextField(default="No comment")
    review_date = models.DateField(null=True)


