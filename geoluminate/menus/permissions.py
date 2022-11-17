
def is_admin(request):
    return request.user.is_admin
