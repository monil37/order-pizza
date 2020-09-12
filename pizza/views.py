from django.shortcuts import render
from pizza.forms import PizzaForm,MultiplePizzaForm 
from django.forms import formset_factory
from .models import Pizza

# Create your views here.
def home(request):
    return render(request,'pizza/home.html')

def order(request):
    multiple_form=MultiplePizzaForm()
    if request.method == 'POST':
        filled_form=PizzaForm(request.POST)
        if filled_form.is_valid():
            created_pizza=filled_form.save()
            created_pizza_pk=created_pizza.id
            note='Your order is succesfully done! You have order topping1:{},topping2:{} with size:{}'.format(filled_form.cleaned_data['topping1'],filled_form.cleaned_data['topping2'],filled_form.cleaned_data['size'])
            filled_form=PizzaForm()
        else:
            created_pizza_pk=None
            note='Your pizzas order failed!'

        return render(request,'pizza/order.html',{'created_pizza_pk':created_pizza_pk,'pizzaform':filled_form,'note':note,'mutliple_form':multiple_form})
    else:
         form=PizzaForm()
         return render(request,'pizza/order.html',{'pizzaform':form,'multiple_form':multiple_form})

def pizzas(request):
    number_pizzas=2
    filled_mutliple_pizzas_form=MultiplePizzaForm(request.GET)

    if filled_mutliple_pizzas_form.is_valid():
        number_pizzas=filled_mutliple_pizzas_form.cleaned_data['number']

    PizzaFormSet=formset_factory(PizzaForm,extra=number_pizzas)
    formset=PizzaFormSet()

    if request.method == 'POST':
        filled_formset=PizzaFormSet(request.POST)

        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note='Pizzas have been ordered'
        else:
            note='Ordered is not created!Please try again later'
        return render(request,'pizza/pizzas.html',{'note':note,'formset':formset})

    else:
        return render(request,'pizza/pizzas.html',{'formset':formset})
    
def edit_order(request,pk):
    pizza=Pizza.objects.get(pk=pk)
    form=PizzaForm(instance=pizza)

    if request.method == 'POST':
        filled_form=PizzaForm(request.POST,instance=pizza)

        if filled_form.is_valid():
            filled_form.save()
            form=filled_form
            note='Order has been updated!'
            return render(request,'pizza/edit_order.html',{'note':note,'pizzaform':form,'pizza':pizza})
    return render(request,'pizza/edit_order.html',{'pizzaform':form,'pizza':pizza})




   