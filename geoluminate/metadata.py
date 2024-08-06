class MetadataOptions:
    model = ""
    """The model class to use for this metadata class. This is required."""

    def __new__(cls, name, bases, attrs):
        for k, v in attrs.items():
            if k.startswith("_"):
                continue
            elif getattr(cls, k, None) is None:
                msg = f"Invalid metadata option '{k}' specified on class '{cls.__name__}'"
                raise AttributeError(msg)
            else:
                setattr(cls, k, v)


class Metadata(metaclass=MetadataOptions):
    pass
