from import_export import resources
from .models import Perusahaan

class PerusahaanResources(resources.ModelResource):
    class Meta:
        model = Perusahaan