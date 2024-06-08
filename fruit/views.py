from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse

from .forms import ContactForm,CommentForm
from .bot import send_message
from .models import Contact,Product,Category,Comment
from django.views.generic import View,TemplateView,DetailView,ListView


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


class ShopView(ListView):
    model = Product
    paginate_by = 2
    template_name = "shop.html"
    context_object_name ="Products"
    context = {}
    context["categories"] = Category.objects.all()
    
    def get_queryset(self):
            queryset = super().get_queryset()
            min_price = self.request.GET.get('price')
            name = self.request.GET.get('q')
            if min_price:
                queryset = queryset.filter(price__lte=min_price)
            if name:
                queryset = queryset.filter(title__icontains=name)
            return queryset


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

# class ContactView(CreateView):
#     model = Contact
#     form_class = ContactForm
#     template_name = "contact.html"
#     success_url ='/'


# def contact_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('first_name', '')
#         email = request.POST.get('email', '')
#         message = request.POST.get('description', '')
#         contact = Contact(first_name=name,email=email,description=message)
#         contact.save()
        
#         send_message(f"Ism: {name}\nEmail: {email}\nText:{message}")

#         return render(request, 'contact.html')
        
#     else:
#         return render(request, "contact.html")