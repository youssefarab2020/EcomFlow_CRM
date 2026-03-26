
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm
from .models import Client
from django.db.models import Q  



def client_list(request):
    # كنجيبو الكلمة اللي كتب المستخدم في خانة البحث (name="q")
    query = request.GET.get('q')
    
    if query:
        # البحث في الاسم أو رقم الهاتف أو المدينة
        clients = Client.objects.filter(
            Q(name__icontains=query) | 
            Q(phone__icontains=query) |
            Q(city__icontains=query)
        )
    else:
        # إذا مكانش البحث، كنعرضو كلشي مرتب بالأحدث
        clients = Client.objects.all()

    return render(request, 'clients/client_list.html', {'clients': clients})

# باقي الـ Views (Create, Update, Delete) كتبقى كيفما هي

def client_list(request):
    clients = Client.objects.all()
    # تأكد أن هاد الملف Template كاين
    return render(request, 'clients/client_list.html', {'clients': clients})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            # التعديل هنا: زدنا اسم الـ App قبل اسم الـ URL
            return redirect('clients:list') 
    else:
        form = ClientForm()
    return render(request, 'clients/create_client.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from .forms import ClientForm

def client_update(request, pk):
    # كنجيبو الكليان بـ ID ديالو، ولا كيعطي 404 إلا مكانش
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        # instance=client هي اللي كتعمر الفورم بالبيانات القديمة وكتقول لـ Django يعدلها ماشي يزيدها
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients:list')
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'clients/update_client.html', {'form': form, 'client': client})


def client_delete(request, pk):
    """
    Supprimer un client définitivement.
    """
    client = get_object_or_404(Client, pk=pk)
    
    # من الأحسن الحذف يكون بـ POST للأمان، ولكن غانديروها مباشرة للتسهيل
    client.delete()
    return redirect('clients:list')