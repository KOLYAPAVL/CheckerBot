from __future__ import annotations
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import PostBackEvent
from django.http import JsonResponse


@method_decorator(csrf_exempt, name='dispatch')
class PostBackView(View):

    def _dict_from_request(self) -> dict:
        if self.request.method == "GET":
            data = self.request.GET
        else:
            data = self.request.POST

        amount = data.get("amount")
        if not amount:
            try:
                amount = float(amount)
            except (TypeError, ValueError):
                amount = None

        return {
            "event_id": data.get("event_id"),
            "amount": amount,
            "country": data.get("country"),
            "user_id": data.get("user_id"),
            "sub1": data.get("sub1"),
        }

    def action(self, request, *args, **kwargs) -> JsonResponse:
        event_type = kwargs.get("event_type")
        p = PostBackEvent.objects.create(
            event_type=event_type,
            **self._dict_from_request(),
        )
        return JsonResponse({
            "success": True,
            "post_back_event_id": p.id,
        })

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return self.action(request, *args, **kwargs)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        return self.action(request, *args, **kwargs)
