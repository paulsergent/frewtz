from rest_framework import serializers
from .models import Order

class OrderActionSerializer(serializers.ModelSerializer):
    action = serializers.ChoiceField(choices=[('accept', 'Accept'), ('reject', 'Reject')], write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'action']

    def update(self, instance, validated_data):
        action = validated_data.get('action')
        if action == 'accept':
            if instance.quantity > instance.product.stock:
                raise serializers.ValidationError("Not enough stock.")
            instance.status = 'accepted'
            instance.farmer_confirmed = True
            instance.product.stock -= instance.quantity
            instance.product.save()
        elif action == 'reject':
            instance.status = 'rejected'
            instance.farmer_confirmed = False
        instance.save()
        return instance