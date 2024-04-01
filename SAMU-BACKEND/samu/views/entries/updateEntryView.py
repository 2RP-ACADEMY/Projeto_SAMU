from django.db import IntegrityError
from samu.models.entryModel import Entry
from samu.serializers.entrySerializer import EntrySerializer
from rest_framework.serializers import ValidationError
from datetime import datetime

class UpdateEntryView():

    @staticmethod
    def update_quantity(quantity, item):
        if quantity:
            if quantity > 0:
                entry = Entry.objects.all().filter(item=item).filter(vehicle_id=None)[0]
                last_quantity = entry.quantity
                if quantity != last_quantity:
                    available_quantity = entry.available_quantity
                    new_available_quantity = available_quantity + (quantity - last_quantity)
                    if new_available_quantity < 0:
                        raise IntegrityError("A quantidade disponível não pode ser menor que 0.")
                    updated_entry = EntrySerializer(entry, data={"quantity": quantity, "available_quantity": new_available_quantity}, partial=True)
                    updated_entry.is_valid(raise_exception=True)
                    updated_entry.save()
            else:
                raise ValidationError("Não é possível ter uma entrada com  quantidade igual ou menor que 0.")
            
    @staticmethod
    def increase_quantity(quantity, pk):
        if quantity:
            if quantity > 0:
                entry = Entry.objects.get(pk=pk)
                last_quantity = entry.quantity
                last_available_quantity = entry.available_quantity
                new_available_quantity = last_available_quantity + quantity
                new_quantity = last_quantity + quantity 
                updated_entry = EntrySerializer(entry, 
                                                data={
                                                    "quantity": new_quantity,             
                                                    "available_quantity": new_available_quantity, 
                                                    "date": datetime.now().date()
                                                }, 
                                                partial=True)
                
                updated_entry.is_valid(raise_exception=True)
                updated_entry.save()
            else:
                raise ValidationError("Não é possível ter uma entrada com  quantidade igual ou menor que 0.")
    
    @staticmethod
    def update_available_quantity(quantity: int, entry: Entry, vehicle_entry: Entry):
        if quantity:
            if quantity > 0:
                last_available_quantity = entry.available_quantity
                if quantity + last_available_quantity <= entry.quantity and quantity <= vehicle_entry.quantity:
                    new_available_quantity = last_available_quantity + quantity 
                    updated_vehicle_entry = EntrySerializer(vehicle_entry, data={"quantity": vehicle_entry.quantity - quantity}, partial=True)
                    updated_vehicle_entry.is_valid(raise_exception=True)
                    updated_vehicle_entry.save()
                    updated_entry = EntrySerializer(entry, data={"available_quantity": new_available_quantity}, partial=True)
                    updated_entry.is_valid(raise_exception=True)
                    updated_entry.save()
                else: 
                    raise ValidationError("Não é possível deslocar esta quantidade de itens.")
            else:
                raise ValidationError("Não é possível ter uma entrada com  quantidade igual ou menor que 0.")


    @staticmethod
    def consumption(quantity, entry):
        new_available_quantity = entry.available_quantity - quantity
        if new_available_quantity >= 0:
            updated_entry = EntrySerializer(entry, data={"available_quantity": new_available_quantity}, partial=True)
            updated_entry.is_valid(raise_exception=True)
            updated_entry.save()
        else:
            raise ValidationError(f"A quantidade disponível é {entry.available_quantity}. Este valor não é sufiente para realizar esta operação!")
        
    
    @staticmethod
    def set_vehicle(vehicle_id, entry_id):
        entry = Entry.objects.get(pk=entry_id)
        updated_entry = EntrySerializer(entry, data={"vehicle_id": vehicle_id}, partial=True)
        updated_entry.is_valid(raise_exception=True)
        updated_entry.save()
        return updated_entry.data
