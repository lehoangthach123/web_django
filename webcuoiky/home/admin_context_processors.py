def highestAdminFunctions(request):
    isSuperUser=False
    if request.user.is_superuser:
        isSuperUser=True

    return {
        'isSuperUser': isSuperUser,
    }
