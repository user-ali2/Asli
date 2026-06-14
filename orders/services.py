from .models import DeliveryStaff

def assign_rider(order):

    riders = DeliveryStaff.objects.filter(
        is_available=True,
        active=True
    )

    if not riders.exists():
        return None
    
    rider = riders.first()

    rider.is_available= False
    rider.save()

    return rider