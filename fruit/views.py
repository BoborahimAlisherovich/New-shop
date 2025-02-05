
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from .bot import send_message
from .models import Contact,Product,Category,Comment,Cart,CartItem
from django.views.generic import View,TemplateView,DetailView,ListView
from .forms import LoginForm, UserRegistrationForm


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self,*args, **kwargs):
        context = super(HomeView, self).get_context_data(*args,**kwargs)
        context['products'] = Product.objects.all()
        context['besteller_products'] = Product.objects.all().order_by('-rating')[:6]  #new
        context
        context['categories'] = Category.objects.all()
        context["reyting"] = [1,2,3,4,5]
        query = self.request.GET.get('q')
        if query:
            context['products'] = Product.objects.filter(title__icontains=query)

        return context

class ShopDetailView(DetailView):
    model = Product
    template_name = "shop-detail.html"
    context_object_name = "product"
    form_class = CommentForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["comments"] = Comment.objects.filter(product=self.object).order_by("-created_date")
        context["form"] = self.form_class()
        context["reyting"] = [1,2,3,4,5]
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)

        if form.is_valid():
            # Process form data
            full_name = form.cleaned_data['full_name']
            description = form.cleaned_data['description']
            rating = form.cleaned_data['rating']
            email = form.cleaned_data['email']
            comment = Comment()
            comment.full_name = full_name
            comment.product = self.object
            comment.description = description
            comment.rating = rating
            comment.email = email
            comment.save()
            return redirect(self.object.get_absolute_url())
        else:
            print(form.errors)  # Xatolikni chop etish
        return self.render_to_response(self.get_context_data(form=form))
    

from django.db.models import Case, When
from django.views.generic import ListView
from django.db.models import Case, When, Value, CharField

class ShopView(ListView):
    model = Product
    paginate_by = 3
    template_name = "shop.html"
    context_object_name = "Products"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["checked"] = Category.objects.all().order_by('title')  # checked ko'rsatkichlarni olish
        return context

    def get_queryset(self):
            queryset = super().get_queryset()
            min_price = self.request.GET.get('price')
            name = self.request.GET.get('q')
            quality = self.request.GET.get('quality')
            if min_price:
                queryset = queryset.filter(price__lte=min_price)
            if name:
                queryset = queryset.filter(title__icontains=name)
            if quality:
                queryset = queryset.filter(quality__icontains=quality)
            return queryset


    def my_view(request):
        Products = [
            {'id': 1, 'checked': 'Quality A', 'name': 'Product A'},
            {'id': 2, 'checked': 'Quality B', 'name': 'Product B'},
            {'id': 3, 'checked': 'Quality C', 'name': 'Product C'},
            # Add more products as needed
        ]
        
        # Duplicate each product in the list with a different 'checked' value
        duplicated_products = []
        for product in Products:
            duplicated_products.append(product)
            duplicated_products.append({'id': product['id'], 'checked': 'Second ' + product['checked'], 'name': product['name']})
        
        return render(request, 'your_template.html', {'Products': duplicated_products})


    
class ContactView(View):
    template_name = "contact.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs): 
        name = request.POST.get('first_name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('description', '')
        contact = Contact(first_name=name,email=email,description=message)
        contact.save()
        
        send_message(f"Ism: {name}\nEmail: {email}\nText:{message}")

        return HttpResponseRedirect(reverse('home-page'))  

def page_turt_view(request,path):
    return render(request, "page-404.html")
 



from .forms import LoginForm, UserRegistrationForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})





def cart(request):
    try:
        cart= Cart.objects.get(session_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.quantity*cart_item.product.price
        shipping = 10
        context = {
        'cart_items': cart_items,
        'shipping': shipping,
        'get_total': total+shipping
    }
    
    except ObjectDoesNotExist:
        context={}
    
    return render(request, 'cart.html', context)
    
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):        
    product = Product.objects.get(id=product_id)
    
    try:
        cart = Cart.objects.get(session_id=_cart_id(request))      
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_id=_cart_id(request))
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        cart_item.save()
    return redirect('cart')

def sub_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(session_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(session_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')