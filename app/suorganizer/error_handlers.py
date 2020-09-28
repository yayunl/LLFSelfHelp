from django.shortcuts import render


def bad_request_handler_400(request, exception=None):
    data = {}
    return render(request, '400.html', data)


def permission_denied_handler_403(request, exception=None):
    data = {}
    return render(request, '403.html', data)


def page_not_found_handler_404(request, exception=None):
    data = {}
    return render(request, '404.html', data)


def server_error_handler_500(request, exception=None):
    data = {}
    return render(request, '500.html', data)

