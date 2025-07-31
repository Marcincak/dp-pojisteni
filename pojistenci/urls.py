from django.urls import path
from . import views
from . import url_handlers

urlpatterns = [
    path("pojistenec_index/", views.PojistenecIndex.as_view(), name="pojistenec_index"),
    path("pojistenec_search/", views.PojistenecSearch.as_view(), name="pojistenec_search"),
    path("<int:pk>/pojistenec_detail/", views.CurrentPojistenec.as_view(), name="pojistenec_detail"),
    path("vytvor_pojistenec/", views.CreatePojistenec.as_view(), name="vytvor_pojistenec"),
    path("pojisteni_index/", views.PojisteniIndex.as_view(), name="pojisteni_index"),
    path("<int:pk>/pojisteni_detail/", views.CurrentPojisteni.as_view(), name="pojisteni_detail"),
    path("vytvor_pojisteni/", views.CreatePojisteni.as_view(), name="vytvor_pojisteni"),
    path("<int:pk>/edit/", views.EditPojistenec.as_view(), name="edit_pojistenec"),
    path("<int:pk>/edit_pojisteni/", views.EditPojisteni.as_view(), name="edit_pojisteni"),
    path("register/", views.UzivatelViewRegister.as_view(), name="registrace"),
    path("login/", views.UzivatelViewLogin.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("", url_handlers.index_handler),
]

