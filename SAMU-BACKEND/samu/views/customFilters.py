import re
from django.db.models import Q

def filter_expiration_date_entry(queryset, query_param, suffix):
    try:
        if query_param:
            test = re.compile("\w+--[\w\W]+")
            if test.fullmatch(query_param):
                data = query_param.split('--')
                if data[0] == 'expiration_date':
                    equipment_condition = Q(item__type=3)
                    filter_medicine = {f'item__medicine__{data[0]}{suffix}': data[1]}
                    filter_material = {f'item__material__{data[0]}{suffix}': data[1]}
                    filtered_queryset = queryset.filter(
                        Q(item__type=1, **filter_medicine) |
                        Q(item__type=2, **filter_material) |
                        equipment_condition
                    )
                return filtered_queryset
            else:
                return queryset
        else:
            return queryset
    except Exception:
        return queryset