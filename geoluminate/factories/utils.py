import random

import factory
from factory import RelatedFactoryList


def randint(min_value, max_value):
    return lambda: random.randint(min_value, max_value)


class ReusableFactoryList(factory.RelatedFactoryList):
    def __init__(self, base_factory, model, choices: list, field="type", **kwargs):
        related_factory = factory.make_factory(model, FACTORY_CLASS=base_factory)
        size = randint(1, len(choices))
        factory_related_name = "object"

        kwargs[field] = factory.Iterator(choices)

        super().__init__(related_factory, factory_related_name, size, **kwargs)


class RelatedFactorySampler(factory.RelatedFactory):
    def __init__(self, factory, factory_related_name, max_allowed=None, max_allowed_ratio=None, **kwargs):
        # self.create = create
        if not max_allowed and not max_allowed_ratio:
            raise ValueError("Must provide either max_allowed or max_allowed_ratio")
        if max_allowed and max_allowed_ratio:
            raise ValueError("Cannot provide both max_allowed and max_allowed_ratio")
        self.max_allowed = max_allowed
        self.max_allowed_ratio = max_allowed_ratio
        self.related_name = factory_related_name
        super().__init__(factory, factory_related_name, **kwargs)

    def call(self, instance, step, context):
        # if not self.create:
        # return

        # used to set a cache on the factory class so that we don't have to query the database for related objects every time we create an instance
        current_factory = instance.__class__

        # factory class of the related objects that we will sample from
        related_factory = self.get_factory()

        # if max_allowed is set, we will use that as the maximum number of related objects to create
        cached_model_list = self.fetch_cache(current_factory, related_factory)

        setattr(instance, self.related_name, random.sample(cached_model_list, k=1))
        # Select a random subset of exhibitions
        # return random.sample(cached_model_list, k=1)

    def fetch_cache(self, factory_class, related_factory):
        """Fetches the cache of related objects stored on the current factory class. If the cache does not exist, it creates it."""
        related_model = related_factory._meta.model
        related_model_name = related_model._meta.model_name
        cache_name = f"_{related_model_name}_cache"

        if not hasattr(factory_class, cache_name):
            count = related_model.objects.count()

            # if self.max_allowed is set, make sure we don't create more than that number of related objects
            if count < self.max_allowed:
                related_factory.create_batch(self.max_allowed - count)

            # we evaluate the queryset here as a list and cache it so that we can call random.sample on it
            setattr(factory_class, cache_name, list(related_model.objects.all()))

        return getattr(factory_class, cache_name)


class RelatedFactoryListWithCreate(RelatedFactoryList):
    def __init__(self, factory, factory_related_name, size, max_allowed=None, max_allowed_ratio=None, **kwargs):
        # self.create = create
        if not max_allowed and not max_allowed_ratio:
            raise ValueError("Must provide either max_allowed or max_allowed_ratio")
        if max_allowed and max_allowed_ratio:
            raise ValueError("Cannot provide both max_allowed and max_allowed_ratio")
        self.max_allowed = max_allowed
        self.max_allowed_ratio = max_allowed_ratio
        super().__init__(factory, factory_related_name, size, **kwargs)

    def call(self, instance, step, context):
        if not self.create:
            return

        # used to set a cache on the factory class so that we don't have to query the database for related objects every time we create an instance
        current_factory = instance.__class__

        # factory class of the related objects that we will sample from
        related_factory = self.get_factory()

        # if max_allowed is set, we will use that as the maximum number of related objects to create
        cached_model_list = self.fetch_cache(current_factory, related_factory)

        # Select a random subset of exhibitions
        random_selection = random.sample(cached_model_list, k=self.size if isinstance(self.size, int) else self.size())

        # add the randomly selected related objects to the current instance via the related_name
        getattr(instance, self.related_name).set(random_selection)

    def fetch_cache(self, factory_class, related_factory):
        """Fetches the cache of related objects stored on the current factory class. If the cache does not exist, it creates it."""
        related_model = related_factory._meta.model
        related_model_name = related_model._meta.model_name
        cache_name = f"_{related_model_name}_cache"

        if not hasattr(factory_class, cache_name):
            count = related_model.objects.count()

            # if self.max_allowed is set, make sure we don't create more than that number of related objects
            if count < self.max_allowed:
                related_factory.create_batch(self.max_allowed - count)

            # we evaluate the queryset here as a list and cache it so that we can call random.sample on it
            setattr(factory_class, cache_name, list(related_model.objects.all()))

        return getattr(factory_class, cache_name)
