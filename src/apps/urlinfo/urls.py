from django.urls import path

from apps.urlinfo.views import URLInfoApiView, URLInfoDetailByPublicIdApiView, URLInfoDetailByUrlApiView

urlpatterns = [
    path(route="", view=URLInfoApiView.as_view(), name="url_info"),
    path(
        route="detail/<uuid:public_id>",
        view=URLInfoDetailByPublicIdApiView.as_view(),
        name="url_info_detail_by_public_id",
    ),
    path(route="detail/", view=URLInfoDetailByUrlApiView.as_view(), name="url_info_detail_by_url"),
]
