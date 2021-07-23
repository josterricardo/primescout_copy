from .models import *
from scout_monitor_fetcher.SeleniumScrapper import SeleniumScrapper
from PIL.Image import Image
import PIL
import requests as rq
from django.conf import settings
import json
from django.core.files import File as DF
import pdb
import re


class ScraperHelper:
    """
    This is a general helper used
    in order to make easier the access
    and integration with the DB
    """
    scrapper_object = SeleniumScrapper()

    def scrap_site_data(self) -> dict:
        """
        calls the service to get the data from the site
        :return: dict
        """
        return self.scrapper_object.scrape_items()

    def store_data(self, scraped_data: list) -> dict:
        """
        stores the given data in
        the existing models
        :param scraped_data: list of dict of the scraped data
        :return: dict
        """
        result ={}
        try:
            for product in scraped_data:
                prod_obj, created = Product.objects.get_or_create(url=product['product_url'],
                                                                  sku=product['sku'])
                if not created:
                    prod_obj.updated_at = datetime.now()
                prod_obj.name=product['name']
                # prod_obj.status=product['status']
                serialized_details = self.organize_detail_data(product['details'])
                print(serialized_details.keys(), product['details'].keys())
                nevera_details, nev_created = NeveraProductDetail.objects.get_or_create(
                    product=prod_obj,
                )
                for key, value in serialized_details.items():
                    nevera_details.__setattr__(key, value)

                if not nev_created:
                    nevera_details.updated_at=datetime.now()

                nevera_details.save()

                for index, image in enumerate(product['images']):
                    try:
                        imgx = self.download_image(image_url=image,
                                                  path=f"{settings.MEDIA_ROOT}/prod_{prod_obj.sku}_img_{index}.png")
                        img = DF(file=open(imgx.name, mode='rb'))
                        prod_img, img_created = ProductImage.objects.get_or_create(product=prod_obj,
                                                                                   img_url = product['images'][index],
                                                                                   img=img)
                        if not img_created:
                            prod_img.updated_at = datetime.now()
                        prod_img.save()
                    except Exception as X:
                        print(X)
                        pass

                price = prod_obj.productprice_set.create()

                if 'normal_price' in product['prices'].keys():
                    price.normal_price = self.evaluate_price(product['prices']['normal_price'])
                if 'daily_price' in product['prices'].keys():
                    price.daily_price = self.evaluate_price(product['prices']['daily_price'])
                if 'special_price' in product['prices'].keys():
                    price.special_price=self.evaluate_price(product['prices']['special_price'])

                price.save()

                # reviews are stopped for economical reasons #
                # review, re_created = ProductReview.objects.get_or_create(product=prod_obj)
                # if product['reviews']:
                #     review.total_qualification = product['reviews']['total_qualification']
                #     for rev in product['reviews']['review_list']:
                #         review_detail, detal_created = ReviewDetail.objects.get_or_create(review=review)
                #         review_detail.qualification = rev['qualification']
                #         review_detail.comment = rev['comment']
                #         review_detail.review_date = self.serialize_review_date(rev['review_date'])
                #         if not re_created:
                #             review_detail.updated_at = datetime.now()
                #         review_detail.save()

            result['message'] = "The records were successfully stored in the DB!!"
            result['status'] = True
        except Exception as X:
            result['error'] = f"{X}"
            result['status'] = False
            # pdb.set_trace()
        return result


    def evaluate_price(self, price):
        """
        serializes the price if it's not a float
        :param price: object
        :return: float
        """
        if isinstance(price,str):
            price = price[price.find('$')+1:]
            price = price.replace(' ','')
            price = price.replace('.','')
            price = float(price)

        return price

    def organize_detail_data(self, product_details:dict) -> dict:
        """
        changes the name of the fields so that
        the values of the product details
        have the same name as the rest of model's fields
        :param product_details: dict
        :return: dict

        """
        rendered_field_names = {
            'marca': "brand",
            'referencia': "reference",
            'tecnología de frío': "frosting_technology",
            # new fields start
            'capacidad neta del refrigerador': "net_refrigerator_capacity",
            'capacidad neta del congelador': "net_freezer_capacity",
            # new fields end
            'capacidad bruta total': 'brute_total_capacity',
            'capacidad neta total': 'net_total_capacity',
           'dispensador de agua': "water_dispenser",
            'tipo de dispensador de agua': "water_dispenser_type",
            'tipo de panel de control': "panel_control_type",
           'localizacion del panel de control': "panel_control_localization",
            'cantidad puertas': "door_amount",
            'material de las bandejas': "trays_material",
           'medidas (ancho x alto x fondo)': "dimensions",
            'inverter': "inverter",
            'tipo de compresor': "compressor_type",
            'tipo de fabricador de hielo': "ice_maker_type",
           'fabricador de hielo': "ice_maker",
            'gama de color': "gama_color",
            'voltaje': "voltage",
            'consumo mínimo energético(kwh/mes)': "min_energy_consumption",
           'eficiencia energética': "power_efficiency",
            'garantía': "warranty",
            'garantía en el compresor': "compressor_warranty",
           'contacto para instalaciones o servicio al cliente': "contact",
            'otros': "other_details",
            'tips neveras': "tips",
            "teléfonos de contacto para información sobre la instalación del producto": "contact_phone_installation",
            'diseño del producto': "product_design",
            'tipo de puertas del nevecon': "door_type_nevecon",
            'opciones de conectividad': "connectivity_options",
            "elementos o accesorios incluidos": "element_included",
            'garantía del fabricante': "maker_warranty",
            'el congelador tiene funcion dual (refrigeración/congelación)': "functional_duality",
            'tonalidad exacta del color': "color_tone",
            'línea/modelo/referencia': "line_model_reference",
            'ancho o frente (cm) externo del producto': "dimension_cm_width",
            'alto (cm) externo del producto':"dimension_cm_height",
            'fondo (cm) externo del producto':"dimension_cm_deepening",
            'medidas (ancho x alto x fondo) en cm': 'all_dimensions_cm',

        }
        final_dict = {}
        try:
            for key,value in product_details.items():
                if key in rendered_field_names.keys():
                    final_dict[rendered_field_names[key]] = value

                if key in ['capacidad bruta total',
                           'capacidad neta del refrigerador',
                           'capacidad neta total',
                           'capacidad neta del congelador',
                           ]:
                    final_dict[rendered_field_names[key]] = (round(float(value.split(' ')[0]), 4)
                        if re.findall(r'[0-9]+', value) else 0.00)
        except Exception:
            raise Exception
            # pdb.set_trace()
        return final_dict

    def download_image(self, image_url:str, path: str) -> Image:
        """
        downloads the image and stores it in the given path
        :param image_url:
        :param: path to store the image into.
        :return: image object: PIL
        """
        downloaded_img = rq.get(image_url, stream=True)
        file =open(path,'wb+')
        file.write(downloaded_img.content)
        file.close()
        return file


    def serialize_review_date(self, review_date:str)->date:
        """
        sets the review date in ISO format
        ready to be loaded in a date field.
        :param review_date: str
        :return: str
        """
        serialized = review_date.split("-")
        return date(year=int(serialized[-1]),
                    month=int(serialized[1]),
                    day=int(serialized[0]))


    def update_values_fridge(self):
        """
        updates the values from the
        given fridge, this is only
        related to the litres
        :return: None
        """
        k = [
            "net_refrigerator_capacity",
            "net_freezer_capacity",
            'brute_total_capacity',
            'net_total_capacity',
        ]
        for obj in NeveraProductDetail.objects.all():
            for key in k:
                value = obj.__getattribute__(key)
                final = "0.0"
                print(value)
                if re.findall(r'[0-9]+', value):
                    final = str(round(float(value.split(' ')[0]), 4))
                obj.__setattr__(key, final)
            obj.save()

    def fetch_data_for_db(self):
        """
        implements the above methods so that the functionality is completed
        most likely to be used for testing.
        :return: dict
        """
        scrapped_data = self.scrap_site_data()
        result = {}
        if scrapped_data['status']:
            result =self.store_data(scraped_data=scrapped_data['data'])
        else:
            result = scrapped_data
        return result

