from polymorphic.models import PolymorphicModel


class Sample(PolymorphicModel):
    ...
    pass


class Dirt(Sample):
    ...
    pass


class Rock(Sample):
    ...
    pass
