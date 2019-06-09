
def jwt_rest_payload_handler(token, user=None, request=None):
    from django.contrib.auth.models import Permission
    group_perm = [g.permissions.values_list('codename', flat=True) for g in user.groups.all()]
    perm = [a for tup in group_perm for a in tup]
    perm += user.user_permissions.values_list('codename', flat=True)
    return {
        "permissions": perm,
        "user": user.pk,
        "is_superuser": user.is_superuser
    }
