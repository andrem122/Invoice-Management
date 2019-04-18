def get_succeeded(model, **kwargs):
    try:
        model.objects.get(**kwargs)
        return True
    except model.DoesNotExist:
        return False
