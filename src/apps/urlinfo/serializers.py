from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.urlinfo.models import URLInfo
from apps.urlinfo.validators import UniqueValidator, URLStatusValidator


class URLInfoCreationSerializer(serializers.Serializer):
    url = serializers.CharField(
        validators=[
            URLStatusValidator(),
            UniqueValidator(queryset=URLInfo.objects.all(), message=_("This URL already exists.")),
        ]
    )


class URLInfoOutputSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id")
    domainName = serializers.CharField(source="domain_name")
    stylesheetCount = serializers.IntegerField(source="stylesheets_count")
    fullDomainName = serializers.SerializerMethodField()

    class Meta:
        model = URLInfo
        fields = (
            "publicId",
            "url",
            "protocol",
            "subdomain",
            "domainName",
            "fullDomainName",
            "title",
            "images",
            "stylesheetCount",
            "created_at",
            "updated_at",
        )

    def get_fullDomainName(self, obj: URLInfo) -> str:
        return f"{obj.subdomain + '.' if obj.subdomain else ''}{obj.domain_name}"


# class URLInfoOutputSerializer(serializers.Serializer):
#     public_id = serializers.CharField()
#     url = serializers.URLField()
#     protocol = serializers.CharField()
#     subdomain = serializers.CharField(allow_null=True)
#     domain_name = serializers.CharField()
#     title = serializers.CharField()
#     images = serializers.ListField(child=serializers.URLField())
#     stylesheets_count = serializers.IntegerField()
#     created_at = serializers.DateTimeField()
#     updated_at = serializers.DateTimeField()
