# Polymorphism

## Solution 1 (current solution) - Relation from base Measurement model to base Sample model

Pros:

- Easy to implement
- No need to change the database schema

Cons

- Can't filter from measurement to polymorphic sample subtype.


## Solution 2 - User specifies relation from child Measurement model to child Sample model

Pros:

- Maintains polymorphism so views and uuids function the same way.
- Can filter from measurement subtype to polymorphic sample subtype (normal relationship).
- Can filter from sample instance to specific measurement subtype.

Cons:

- Measurements must have a specific sample type.
- Requires mechanism to retrieve all measurements of different types for a sample instance.


## Solution 3 - No polymorphism. Use abstract Measurement and Sample models.

Pros:

- Filtering is straightforward.
- No extra queries from polymorphism.

Cons:

- Must keep a registry of Sample and Measurement types.
- Must rewrite views to handle different model types.
- Can't look up single instance by uuid.