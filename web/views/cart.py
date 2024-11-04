from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


def add(request, pid):
    '''将菜品加入购物车'''
    ''' 
    In Django, session data is stored as a dictionary where keys are 
    always strings. When you access request.session['productlist'][pid], 
    pid needs to be a string because dictionary keys in Python are 
    type-sensitive. If pid were an integer, it wouldn’t match the 
    string keys in the session dictionary, leading to a KeyError.
    '''
    # Ensure pid is a string as session keys are strings
    pid = str(pid)

    # Retrieve productlist from session, or default to an empty dict
    productlist = request.session.get('productlist', {})
    selected_product = productlist.get(pid)

    if not selected_product:
        # If product not found, redirect with an error message
        messages.error(request, "Product not found.")
        return redirect(reverse("web_index"))
        
    # Retrieve or initialize cartlist as a dictionary
    cartlist = request.session.get('cartlist', {})
    if not isinstance(cartlist, dict):
        cartlist = {}

    # Add product to cart or update quantity
    if pid in cartlist:
        cartlist[pid]['quantity'] = cartlist[pid].get('quantity', 1) + 1
    else:
        selected_product['quantity'] = 1
        cartlist[pid] = selected_product

    # Save the updated cartlist to the sessions
    request.session['cartlist'] = cartlist

    # Redirect to the index page
    return redirect(reverse("web_index"))


def change(request):
    try:
        cartlist = request.session.get('cartlist', {})

        pid = request.GET.get('pid', 0)
        pid = str(pid)

        num = request.GET.get('num', 0)
        num = int(num)

        if num < 1:
            num = 1

        cartlist[pid]['quantity'] = num

        request.session['cartlist'] = cartlist
        return redirect(reverse("web_index"))

    except Exception as e:
        print(e)
        return HttpResponse(f"An error occurred: {e}")
        # return redirect(reverse("web_index"))


def delete(request, pid):
    '''执行信息删除'''
    try:
        cartlist = request.session.get('cartlist', {})
        print("cartlist (b4 delete):::::", cartlist)
        if pid in cartlist:
            del cartlist[pid]
            request.session['cartlist'] = cartlist
            return redirect(reverse("web_index"))
        else:
            return HttpResponse('Item not found in cart', status=404)
    except KeyError:
        return HttpResponse('Item not found in cart', status=404)
    except Exception as err:
        print(err)
        return HttpResponse(f'Error: {err}', status=500)
        

def clearCart(request):
    request.session['cartlist'] = {}
    return redirect(reverse("web_index"))



