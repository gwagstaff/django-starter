from django.views.generic import TemplateView, View
from django.http import JsonResponse
from celery.result import AsyncResult
from .celery import debug_task_returning, app

class CeleryDemoView(TemplateView):
    template_name = "celery_demo.html"

class StartTaskView(View):
    def post(self, request):
        number = int(request.POST.get("number", 0))
        task = debug_task_returning.delay(number)
        return JsonResponse({"task_id": task.id})

class TaskStatusView(View):
    def get(self, request, task_id):
        result = AsyncResult(task_id, app=app)
        if result.state == "PROGRESS":
            percent = result.info.get("process_percent", 0)
            return JsonResponse({"state": result.state, "percent": percent})
        elif result.state == "SUCCESS":
            return JsonResponse({"state": result.state, "result": result.result})
        else:
            return JsonResponse({"state": result.state})