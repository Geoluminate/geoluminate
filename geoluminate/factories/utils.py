import logging
import random

import factory
from factory import enums, utils
from factory.declarations import PostGenerationDeclaration
from factory.django import DjangoModelFactory

logger = logging.getLogger(__name__)


def randint(min_value, max_value):
    return lambda: random.randint(min_value, max_value)


class TreeGenerator(PostGenerationDeclaration):
    """Calls a given function once the object has been generated."""

    def __init__(self, function):
        super().__init__()
        self.function = function

    def call(self, instance, step, context):
        logger.debug(
            "PostGeneration: Calling %s.%s(%s)",
            self.function.__module__,
            self.function.__name__,
            utils.log_pprint(
                (instance, step),
                context._asdict(),
            ),
        )
        create = step.builder.strategy == enums.CREATE_STRATEGY
        return self.function(instance, create, context.value, **context.extra)


class TreeFactory(DjangoModelFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        parent = kwargs.pop("parent", None)
        if parent:
            return model_class.add_child(parent, *args, **kwargs)
        return model_class.add_root(*args, **kwargs)

    @factory.post_generation
    def children(instance, create, extracted, **kwargs):
        """Post-generation hook to recursively generate child nodes."""
        if not create:
            return

        max_depth = kwargs.pop("max_depth", 1)
        max_children = kwargs.pop("max_children", 1)

        if instance.depth >= max_depth:
            return

        num_children = random.randint(2, max_children)

        instance.__class__.create_batch(
            num_children,
            parent=instance,
            children__max_depth=max_depth,
            children__max_children=max_children,
        )
