from django.urls import path
#from .views import SampleAPI
from .views import Signup
from .views import Login
from .views import loginwith42
from .views import Intra42Callback
urlpatterns = [
    # path('sample/', SampleAPI.as_view(), name='sample_api'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/',Login.as_view(),name='login'),
    path('login_with_42/',loginwith42.as_view(),name='login_with_42'),
    path('intra42callback/',Intra42Callback.as_view(),name='Intra42Callback'),
]