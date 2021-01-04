from orders.models import Order
from django.shortcuts import redirect

def user_created_order(view_func):
    def wrap(request, *args, **kwargs):

        order_id = kwargs["order_id"]

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return redirect('profile')

        return view_func(request, *args, **kwargs)

    return wrap
