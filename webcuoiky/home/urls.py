from django.urls import path
from . import views
from django.contrib.auth.decorators import user_passes_test
from .models import WebsiteState

# Hàm kiểm tra quyền is_staff
def is_staff_user(request):
    return request.is_authenticated and request.is_staff

# Hàm kiểm tra trạng thái web
def is_website_open(request):
    web_state = WebsiteState.objects.first()  # Lấy trạng thái từ database
    return not web_state.is_closed  # Trả về True nếu web đang mở, False nếu web đóng


app_name = 'home'

urlpatterns = [
    path('closed/', views.closed, name='closed'),


    path('register/', views.RegisterPage.as_view(), name='register'),
    path('login/', views.A_Login.as_view(), name='login'),
    path('logout/', views.A_Logout.as_view(), name='logout'),

    path('u-register/', user_passes_test(is_website_open, login_url='home:closed')(views.U_RegisterPage.as_view()), name='u-register'),
    path('u-login/', user_passes_test(is_website_open, login_url='home:closed')(views.U_Login.as_view()), name='u-login'),
    path('u-logout/', user_passes_test(is_website_open, login_url='home:closed')(views.U_Logout.as_view()), name='u-logout'),
    path('update-customer/', user_passes_test(is_website_open, login_url='home:closed')(views.U_CustomerEdit.as_view()), name='update-customer'),


    path('', user_passes_test(is_website_open, login_url='home:closed')(views.U_Index.as_view()), name='index'),
    path('category/<int:id>', user_passes_test(is_website_open, login_url='home:closed')(views.U_Category.as_view()), name='category'),
    path('product/<int:id>/', user_passes_test(is_website_open, login_url='home:closed')(views.U_Product.as_view()), name='product'),
    path('cart', user_passes_test(is_website_open, login_url='home:closed')(views.V_Cart.as_view()), name='cart'),
    path('cart/<int:id>/', user_passes_test(is_website_open, login_url='home:closed')(views.U_Cart.as_view()), name='cart'),
    path('search/', user_passes_test(is_website_open, login_url='home:closed')(views.U_Search.as_view()), name='search'),
    path('pay/', user_passes_test(is_website_open, login_url='home:closed')(views.U_Pay.as_view()), name='pay'),


    path('us-index/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Index.as_view()), name='us-index'),
    path('us-customer/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Customer.as_view()), name='us-customer'),
    path('us-products/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Product.as_view()), name='us-products'),
    path('us-order/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Order.as_view()), name='us-order'),
    path('us-inventory/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Inventory.as_view()), name='us-inventory'),
    path('us-account/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Account.as_view()), name='us-account'),
    path('us-tasks/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Tasks.as_view()), name='us-tasks'),

    path('a-update-customer/<int:id>', user_passes_test(is_staff_user, login_url='home:login')(views.A_Updated_Customer.as_view()), name='a-update-customer'),

    path('a-new-account/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Create_Account.as_view()), name='a-new-account'),
    path('a-delete-account/<int:id>/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Delete_Account.as_view()), name='a-delete-account'),

    
    path('a-new/', user_passes_test(is_staff_user, login_url='home:login')(views.A_New.as_view()), name='a-new'),
    path('a-update/<int:id>/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Updated_Products.as_view()), name='a-update'),
    path('a-delete/<int:id>/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Delete_Products.as_view()), name='a-delete'),

    
    path('a-inventory/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Created_Inventory.as_view()), name='a-inventory'),
    path('a-update-inventory/<int:id>/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Updated_Inventory.as_view()), name='a-update-inventory'),
    path('a-delete-inventory/<int:id>/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Delete_Inventory.as_view()), name='a-delete-inventory'),
    path('a-searchs/', user_passes_test(is_staff_user, login_url='home:login')(views.A_Search_Products.as_view()), name='a-searchs'),

]