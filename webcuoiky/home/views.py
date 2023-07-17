from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.db.models import Q
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.core.paginator import Paginator
from datetime import datetime


# Create your views here

def closed(request):
    return render(request, 'closed.html')


class RegisterPage(View):
    def get(self, request):
        forms = Register_User()
        context = {
            'forms': forms
        }
        return render(request, 'QuanLy/login.html', context)
    
    def post(self, request):
        forms = Register_User(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('home:us-index')
        else:
            messages.error(request, 'An error occurred during registration?')
        context = {
            'forms': forms
        }
        return render(request, 'QuanLy/login.html', context)


class A_Login(View):
    def get(self, request):
        page = "login"
        if request.user.is_authenticated:
            return redirect('home:us-index')
        context = {
            'page': page
        }
        return render(request, 'QuanLy/login.html', context)
    
    def post(self, request):
        page = "login"
        if request.user.is_authenticated:
            return redirect('home:us-index')
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('home:us-index')
        
        context = {
            'page': page
        }
        return render(request, 'QuanLy/login.html', context)
    

class A_Logout(View):
    def get(self, request):
        logout(request)
        return redirect("home:login")


class U_RegisterPage(View):
    def get(self, request):
        forms = RegisterCustomerForm()
        context = {
            'forms': forms
        }
        return render(request, 'user/reg.html', context)
    
    def post(self, request):
        forms = RegisterCustomerForm(request.POST)
        if forms.is_valid():
            return redirect('home:u-login')
        else:
            messages.error(request, 'An error occurred during registration?')
        context = {
            'forms': forms
        }
        return render(request, 'user/reg.html', context)


class U_Login(View):
    def get(self, request):
        context=None
        username=request.session.get('user',None)
        if username != None:
            user = User.objects.get(username=username)
            customer=Customer.objects.get(user=user)
            order_items = OrderItem.objects.filter(order__customer=customer)


            context = {
                'customer': customer,
                'order_items': order_items,
            }
        return render(request, 'user/login.html', context)
    
    def post(self, request):
        context={}
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['user']=user.username 
            context['customer']=user
        else:
            messages.error(request, 'Email or password does not exist.')
        
        return redirect('home:u-login')


class U_Logout(View):
    def get(self, request):
        del request.session['user']
        return redirect("home:u-login")
                

class U_CustomerEdit(View):
    def get(self, request):
        username=request.session.get('user',None)
        user = User.objects.get(username=username)
        customer=Customer.objects.get(user=user)
        form = CustomerForm(instance=customer)
        context = {
            'form': form,
        }
        return render(request, 'user/edit_customer.html', context)

    def post(self, request):
        username=request.session.get('user',None)
        user = User.objects.get(username=username)
        customer=Customer.objects.get(user=user)
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            new_password = form.cleaned_data['password']
            user.set_password(new_password)
            user.save()

        context = {
            'form': form,
        }
        return render(request, 'user/edit_customer.html', context)


class U_Search(View):
    def get(self, request):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(descriptions__icontains=q)
        )
        product_count = products.count()

        sort_option = request.GET.get('sort')
        if sort_option == 'price_high':
            products = products.order_by('-price')
        elif sort_option == 'price_low':
            products = products.order_by('price')
        else:
            sort_option=None

        paginator= Paginator(products,3) #chỉnh 16 là đẹp
        page_number = request.GET.get("page")
        products_per_page=paginator.get_page(page_number)

        products_show = len(products_per_page.object_list)

        # categories = Category.objects.all()

        context = {
            'products':products_per_page,
            'product_count': product_count,
            # 'categories': categories,
            'products_show': products_show,
            'sort_option': sort_option,
        }
        return render(request, 'user/search.html', context)
    

class U_Category(View):
    def get(self, request, id):
        current_category = Category.objects.get(id=id)
        products = Product.objects.filter(
            Q(category__name__icontains=current_category.name)
        )
        product_count = products.count()

        sort_option = request.GET.get('sort')
        if sort_option == 'price_high':
            products = products.order_by('-price')
        elif sort_option == 'price_low':
            products = products.order_by('price')
        else:
            sort_option=None

        paginator= Paginator(products,3) #chỉnh 16 là đẹp
        page_number = request.GET.get("page")
        products_per_page=paginator.get_page(page_number) 

        products_show = len(products_per_page.object_list)

        # categories = Category.objects.all()
        context = {
            'current_category': current_category,
            'products':products_per_page,
            'product_count': product_count,
            # 'categories': categories,
            'products_show': products_show,
            'sort_option': sort_option,
        }
        return render(request, 'user/category.html', context)
    

class U_Index(View):
    def get(self,request):
        # categories = Category.objects.all()
        context = {
            # 'categories': categories
        }
        return render(request,"user/index.html", context)


class U_Product(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        all_products = Product.objects.filter(
            Q(category__name__icontains=product.category)
        )

        products = []
        if all_products.count()>1:
            i = 0
            is_product_exist = False
            while i < 6 and i < all_products.count():
                products.append(all_products[i])
                if product.id == all_products[i]:
                    is_product_exist=True
                i = i + 1
            if is_product_exist:
                products.remove(product)
            else:
                products.pop()

        current_category = Category.objects.get(name=product.category)

        # categories = Category.objects.all()

        context = {
            "product": product,
            "products": products,
            "current_category": current_category,
            # "categories": categories,
        }
        return render(request, "user/product.html", context)


class U_Cart(View):
    def get(self, request, id):
        orderitems = Product.objects.get(id=id)
        orderitem_products = OrderItem.objects.filter(
            Q(product__name__icontains = orderitems)
        )
        context = {
            'orderitems': orderitems,
            'orderitem_products': orderitem_products
        }
        return render(request, 'user/cart.html', context)


class A_Index(View):
    def get(self, request):
        customers = Customer.objects.all()
        customer_counts = customers.count()

        orderitems = OrderItem.objects.all()
        orderitems_counts = orderitems.count()

        products = Product.objects.all()
        products_counts = products.count()
        context = {
            'customers': customers,
            'customer_counts': customer_counts,
            'orderitems_counts': orderitems_counts,
            'products_counts': products_counts,
            'products': products
        }
        return render(request, 'QuanLy/index.html', context)

    
class A_Customer(View):
    def get(self, request):
        customers = Customer.objects.all()
        context = {
            'customers': customers
        }
        return render(request, 'QuanLy/customer.html', context)
    

class A_Product(View):
    def get(self, request):
        products = Product.objects.all()
        context = {
            'products': products,
        }
        return render(request, 'QuanLy/products.html', context)
    

class A_Order(View):
    def get(self, request):
        orders = OrderItem.objects.all()
        context = {
            'orders': orders,
        }
        return render(request, 'QuanLy/oders.html', context)


class A_Inventory(View):
    def get(self, request):
        inventorys = Category.objects.all()
        context = {
            'inventorys': inventorys
        }
        return render(request, 'QuanLy/inventory.html', context)
    

class A_Account(View):
    def get(self, request):
        users = User.objects.filter(is_staff=True)
        context = {
            'users': users
        }
        return render(request, 'QuanLy/Account.html', context)
    

class A_Tasks(View):
    def get(self, request):
        web=WebsiteState.objects.first()
        form_status = WebsiteStateStatusForm(instance=web)
        form_info = WebsiteStateInformationForm(instance=web)
        context = {
            'form_status': form_status,
            'form_info':form_info
        }
        return render(request, 'QuanLy/tasks.html', context)
    
    def post(self, request):
        web = WebsiteState.objects.first()
        action = request.POST.get('action')

        if action == 'info':
            form = WebsiteStateInformationForm(request.POST, instance=web)
        else:
            form = WebsiteStateStatusForm(request.POST, instance=web)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
            print()
            for field, error in form.errors.items():
                print(f"Field '{field}': {error}")

        return redirect('home:us-tasks')


class A_Updated_Customer(View):
    def get(self, request, id):
        customer = Customer.objects.get(id=id)
        updated = customer.user
        updated_customer = ChangeCustomerPasswordForm()
        context = {
            'updated': customer,
            'updated_customer': updated_customer
        }
        return render(request, 'QuanLy/customer/edit.html', context)
    
    def post(self, request, id):
        customer = Customer.objects.get(id=id)
        updated_user = customer.user
        updated_customer = ChangeCustomerPasswordForm(request.POST)
        if updated_customer.is_valid():
            new_password = updated_customer.cleaned_data['new_password']
            updated_user.set_password(new_password)
            updated_user.save()
            return redirect('home:us-customer')
        context = {
            'updated': customer,
            'updated_customer': updated_customer
        }
        return render(request, 'QuanLy/customer/edit.html', context)


class A_New(View):
    def get(self, request):
        productforms = ProductForm()
        context = {
            'productforms': productforms
        }
        return render(request, 'QuanLy/products/new.html', context)
    
    def post(self, request):
        productforms = ProductForm(request.POST, request.FILES)
        if productforms.is_valid():
            productforms.save()
            return redirect("home:us-products")
        context = {
            'productforms': productforms
        }
        return render(request, 'QuanLy/products/new.html', context)
    

class A_Updated_Products(View):
    def get(self, request, id):
        products = Product.objects.get(id=id)
        productforms = ProductForm(instance=products)
        context = {
            'products': products,
            'productforms': productforms
        }
        return render(request, 'QuanLy/products/edit.html', context)

    def post(self, request, id):
        products = Product.objects.get(id=id)
        productforms = ProductForm(request.POST, request.FILES, instance=products)
        if productforms.is_valid():
            productforms.save()
            return redirect('home:us-products')
        context = {
            'products': products,
            'productforms': productforms
        }
        return render(request, 'QuanLy/products/edit.html', context)
    

class A_Delete_Products(View):
    def get(self, request, id):
        products = Product.objects.get(id=id)
        context = {
            'products': products
        }
        return render(request, 'QuanLy/products/delete.html', context)
    def post(self, request, id):
        products = Product.objects.get(id=id)
        if request.method == "POST":
            products.delete()
            return redirect('home:us-products')
        context = {
            'products': products
        }
        return render(request, 'QuanLy/products/delete.html', context)
    

class A_Created_Inventory(View):
    def get(self, request):
        create_inventorys = CategoryInventoryForm()
        context = {
            'create_inventorys': create_inventorys
        }
        return render(request, 'QuanLy/inventory/new.html', context)
    
    def post(self, request):
        create_inventorys = CategoryInventoryForm(request.POST, request.FILES)
        if create_inventorys.is_valid():
            create_inventorys.save()
            return redirect('home:us-inventory')
        context = {
            'create_inventorys': create_inventorys
        }
        return render(request, 'QuanLy/inventory/new.html', context)


class A_Updated_Inventory(View):
    def get(self, request, id):
        updated = Category.objects.get(id=id)
        updated_inventorys = CategoryInventoryForm(instance=updated)
        context = {
            'updated': updated,
            'updated_inventorys': updated_inventorys
        }
        return render(request, 'QuanLy/inventory/edit.html', context)
    
    def post(self, request, id):
        updated = Category.objects.get(id=id)
        updated_inventorys = CategoryInventoryForm(request.POST, request.FILES ,instance=updated)
        if updated_inventorys.is_valid():
            updated_inventorys.save()
            return redirect('home:us-inventory')
        context = {
            'updated': updated,
            'updated_inventorys': updated_inventorys
        }
        return render(request, 'QuanLy/inventory/edit.html', context)
    

class A_Delete_Inventory(View):
    def get(self, request, id):
        inventorys = Category.objects.get(id=id)
        context = {
            'inventorys': inventorys
        }
        return render(request, 'QuanLy/inventory/delete.html', context)
    def post(self, request, id):
        inventorys = Category.objects.get(id=id)
        if request.method == "POST":
            inventorys.delete()
            return redirect('home:us-inventory')
        context = {
            'inventorys': inventorys
        }
        return render(request, 'QuanLy/inventory/delete.html', context)


class A_Create_Account(View):
    def get(self, request):
        form = AddAccountForm()
        context = {
            'create_account': form
        }
        return render(request, 'QuanLy/account/new.html', context)
    def post(self,request):
        form = AddAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            is_staff = form.cleaned_data['is_staff']
            user = User.objects.create_user(username=username, password=password, is_staff=is_staff)
            # form.save()
            return redirect('home:us-account')
        context = {
            'create_account': form
        }
        return render(request, 'QuanLy/account/new.html', context)


class A_Delete_Account(View):
    def get(self, request, id):
        account = User.objects.get(id=id)
        context = {
            'account': account
        }
        return render(request, 'QuanLy/account/delete.html', context)
    def post(self, request, id):
        account = User.objects.get(id=id)
        account.delete()
        return redirect('home:us-account')
        # context = {
        #     'inventorys': inventorys
        # }
        # return render(request, 'QuanLy/inventory/delete.html', context)


class A_Search_Products(View):
    def get(self, request):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(category__name__icontains=q) |
            Q(descriptions__icontains=q)
        )

        context = {
            'products': products,
        }
        return render(request, 'QuanLy/products.html', context)
    

def product_to_dict(product):
        product_dict = serializers.serialize('python', [product])[0]['fields']
        product_dict['id'] = product.pk
        return product_dict


class V_Cart(View):
    def get_items_price(self, items):
        price = 0
        for item in items:
            price = price + item['product']['price'] * item['quantity']
        return price
    
    def get(self, request):
        product_id = int(request.GET.get('id',-1))
        cart=request.session.get("cart",None)
        # kiểm tra xem có phải url xem cart hay không
        if product_id == -1:
            pass
        else:

            # thêm vào cart
            if request.GET.get("action") == "add-to-cart":
                product = Product.objects.get(id = product_id)
                product = product_to_dict(product)
                # chuyển đối tượng ngày thành chuỗi
                product['created_Date']=product['created_Date'].strftime("%Y-%m-%dT%H:%M:%S.%f")
                product_quantity = int(request.GET.get('quantity'))
                item={
                    'product':product,
                    'quantity':product_quantity,
                    'price':product['price']*product_quantity
                }
                
                # chưa có cart thì tạo mới
                if cart is None:
                    items = []
                    items.append(item)
                    price=self.get_items_price(items)
                    items_count=len(items)
                    cart={
                        'items': items,
                        'total_price':price,
                        'items_count':items_count
                    }

                # đã có cart thì cập nhập quantity hoặc thêm vào cart
                else:
                    items=cart['items']
                    # cập nhập quantity
                    item_found = False
                    for item_dict in items:
                        if item_dict['product']['id'] == item['product']['id']:
                            item_dict['quantity'] += item['quantity']
                            item_dict['price'] = item_dict['quantity'] * item_dict['product']['price']
                            item_found = True
                            break
                    # thêm vào cart
                    if not item_found:
                        items.append(item)
                    price=self.get_items_price(items)
                    items_count=len(items)
                    cart={
                        'items': [item_dict for item_dict in items],
                        'total_price':price,
                        'items_count':items_count
                    }
            
            # cập nhập quantitly
            if request.GET.get("action") == "update-cart":
                new_quantity = int(request.GET.get('quantity'))
                items=cart['items']
                for item_dict in items:
                        if item_dict['product']['id'] == product_id:
                            item_dict['quantity'] = new_quantity
                            item_dict['price'] = item_dict['quantity'] * item_dict['product']['price']
                            break
                cart['total_price']=self.get_items_price(items)
                
            # xóa item khỏi cart
            if request.GET.get("action") == "delete-cart":
                items = cart['items']
                for i, item_dict in enumerate(items):
                    if item_dict['product']['id'] == product_id:
                        del items[i]
                        break
                cart['items_count']=len(items)
                cart['total_price']=self.get_items_price(items)
                

            request.session['cart']=cart

        context={}
        if cart != None:
            context.update(cart)

        # categories = Category.objects.all()
        # context['categories']=categories

        money_to_free_ship=200-context.get('total_price', 0)
        if money_to_free_ship > 0:
            context['money_to_free_ship']=money_to_free_ship
        else:
            context['money_to_free_ship']=None
        
        return render(request, "user/cart.html", context)


class U_Pay(View):
    def get(self, request):
        username=request.session.get('user',None)
        if username != None:
            cart=request.session.get("cart",None)
            if cart !=None and cart['items_count'] > 0:
                user = User.objects.get(username=username)
                customer=Customer.objects.get(user=user)
                order = Order(customer=customer)
                order.save()
                items = cart['items']
                for item_dict in items:
                    product_dict = item_dict['product']
                    product_dict['created_Date']= datetime.strptime(product_dict['created_Date'], "%Y-%m-%dT%H:%M:%S.%f")
                    product_dict['category']= Category(product_dict['category'] ) 
                    product = Product(**product_dict)
                    order_item= OrderItem(product=product,order=order, quantity=item_dict['quantity'])
                    order_item.save()
                    product_in_stock = Product.objects.get(id=product.id)
                    product_in_stock.quantity=product_in_stock.quantity-item_dict['quantity']
                    product_in_stock.save()
                del request.session['cart']
            else:
                messages.error(request, 'Cart empty!')
        else:
            return redirect('home:u-login')
        return redirect('home:cart')
        



