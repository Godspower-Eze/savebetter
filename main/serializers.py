from rest_framework import serializers


class SignatureGeneratorSerializer(serializers.Serializer):

    user_id = serializers.CharField(max_length=42)
    reference = serializers.CharField(max_length=500)
    amount_in_kobo = serializers.IntegerField()