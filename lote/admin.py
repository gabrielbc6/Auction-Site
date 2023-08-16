from django.contrib import admin
from lote.models import Lote
from lote.models import Leilao
from lote.models import Lance
from lote.models import Pagamento

admin.site.register(Pagamento)
admin.site.register(Lote)
admin.site.register(Leilao)
admin.site.register(Lance)