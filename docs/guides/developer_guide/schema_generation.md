# Defining your schemas

Declare fields and validators for your database tables in a familiar, easy-to-understand syntax according to the exact specifications required by your research community. With Geoluminate, the most important data structures are defined by you so there is no need to adapt your requirements to fit a structure defined by somebody else. Geoluminate provides a base `Measurement` class that you can extend to define your own data structures. This class allows you to leverage the full power of Django's model layer while also providing necessary metadata to properly describe your measuremenet. 

Unlike text-based, NoSQL alternatives, all fields listed in your measurement classes will directly alter your database schema, allowing you to harness the full capabilities of your underlying PostgreSQL database. Additionally, you can use Django's built-in ORM to interact with your database tables, making it easy to query, filter, and manipulate your data.


## Additional Fields

In addition to Django's standard database fields, Geoluminate provides custom fields that are particularly useful for reasearch data:

- `QuantityField`: A numeric field that also stores basic units of measurement (e.g. meters, seconds, etc.) alongside the value and allows you to perform unit conversions.
- `ConceptField`: A field that stores a concept from a controlled vocabulary.
- `TaggableConcepts`: A generic relationship that allows you to tag any model with concepts from a controlled vocabulary. Great for keyword tagging.
- `FuzzyDateField`: A field that stores a date with an associated level of uncertainty.