from django.core.validators import DomainNameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.api.validators import URLValidator
from apps.common.models import BaseModel


class ProtocolChoices(models.TextChoices):
    HTTP = "http"
    HTTPS = "https"


class URLInfo(BaseModel):
    url = models.URLField(
        verbose_name=_("URL"),
        unique=True,
        db_index=True,
        validators=[URLValidator],
        help_text=_("The URL of the page"),
    )
    protocol = models.CharField(
        verbose_name=_("Protocol"),
        max_length=5,
        choices=ProtocolChoices.choices,
        help_text=_("The protocol of the URL"),
    )
    subdomain = models.CharField(
        verbose_name=_("Subdomain"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("The subdomain of the URL"),
    )
    domain_name = models.CharField(
        verbose_name=_("Domain name"),
        max_length=255,
        validators=[DomainNameValidator],
        help_text=_("The domain name of the URL"),
    )
    title = models.CharField(verbose_name=_("Title"), max_length=255, help_text=_("The title of the page"))
    images = models.JSONField(
        verbose_name=_("Images urls"), blank=True, null=True, help_text=_("The URLs of all the images <img>")
    )
    stylesheets_count = models.PositiveSmallIntegerField(
        verbose_name=_("Stylesheets count"),
        default=0,
        help_text=_("The number of stylesheets present in the html of the page"),
    )

    class Meta:
        db_table = "url_info"
        verbose_name = _("URL info")
        verbose_name_plural = _("URL infos")

    def __str__(self) -> str:
        return self.url
