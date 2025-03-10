<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path("",views.login,name="login"),
    path("delete_table1",views.delete_table1,name="delete_table1"),
    path("signup",views.signup,name="signup"),
    path("login_2",views.login_2,name="login_2"),
    path("Menu",views.Menu,name="Menu"),
    path("storage",views.storage,name="storage"),
    path("About",views.About,name="About"),
    path("Services",views.Services,name="Services"),
    path("Contact",views.Contact,name="Contact"),
    path("payment13",views.payment13,name="payment13"),
    path("Dashboard",views.Dashboard,name="Dashboard"),
    path("otp_verification",views.otp_verification,name="otp_verification"),
    path("resend_otp",views.resend_otp,name="resend_otp"),
    path("otp_expire",views.otp_expire,name="otp_expire"),
    path("paysuccess",views.paysuccess,name="paysuccess"),
    path('logout',views.logout,name='logout'),
=======
from django.urls import path
from . import views

urlpatterns = [
    path("",views.login,name="login"),
    path("delete_table1",views.delete_table1,name="delete_table1"),
    path("signup",views.signup,name="signup"),
    path("login_2",views.login_2,name="login_2"),
    path("Menu",views.Menu,name="Menu"),
    path("storage",views.storage,name="storage"),
    path("About",views.About,name="About"),
    path("Services",views.Services,name="Services"),
    path("Contact",views.Contact,name="Contact"),
    path("payment13",views.payment13,name="payment13"),
    path("Dashboard",views.Dashboard,name="Dashboard"),
    path("otp_verification",views.otp_verification,name="otp_verification"),
    path("resend_otp",views.resend_otp,name="resend_otp"),
    path("otp_expire",views.otp_expire,name="otp_expire"),
    path("paysuccess",views.paysuccess,name="paysuccess"),
    path('logout',views.logout,name='logout'),
>>>>>>> 591af9b (Initial commit)
]