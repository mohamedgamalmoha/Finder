

def get_model_fields_names(instance, exclude=None):
    """Get fields names from model instance."""
    if exclude is None:
        exclude = []
    return list(filter(
        lambda field_name: field_name not in exclude,
        map(lambda field: field.name, instance._meta.get_fields())
    ))
