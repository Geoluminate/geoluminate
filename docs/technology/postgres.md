# Postgres

Although you can use it without such capabilities, at its heart FairDM is designed as a geospatial application. [GeoDjango](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/), the geographic extension of Django, provides support for multiple geospatial databases. However, the two most commonly used and well-supported are  [PostgreSQL](https://www.postgresql.org) (with [PostGIS](http://postgis.net)) and [SQLite](https://www.sqlite.org/index.html) (with [Spatialite](https://www.gaia-gis.it/fossil/libspatialite/index)).

So which do we use? The answer is... well, both. FairDM ships with a few different configuration (Docker) files for building and deploying your application when the time comes. One of those configurations is designed to deploy your application to a production server and utilizes PostgreSQL for it's vastly superior performance. Another deployment configuration is designed to be more lightweight so that you can easily run the application on your personal laptop. For this, we use the lighter weight SpatiaLite database. You can [read more about deployment here](deploying).


## PostgreSQL and PostGIS

 [PostgreSQL](https://www.postgresql.org) is a powerful and versatile open-source relational database management system (RDBMS) that, when combined with the [PostGIS extension](http://postgis.net), offers several compelling reasons for its use in geospatial applications.

1. **PostGIS Extension:** PostGIS adds comprehensive geospatial capabilities for storage, management and analysis of spatial data within the database.

2. **Geospatial Functionality:** PostGIS provides a rich set of geospatial functions and operators, enabling complex spatial operations, spatial queries, and proximity analysis.

3. **Data Integration and Interoperability:** PostgreSQL with PostGIS supports various geospatial data formats, facilitating seamless integration with external sources and enabling data exchange with other geospatial tools.

4. **Scalability and Performance:** PostgreSQL handles large volumes of geospatial data efficiently, performing high-performance spatial queries and analysis, especially with proper indexing and query optimization.

5. **Reliability and Data Integrity:** PostgreSQL ensures reliability and data integrity through transactional support, crash recovery mechanisms, and data integrity constraints, vital for maintaining consistency in geospatial data.


## SQLite and SpatiaLite

SQLite and SpatiaLite are lightweight, embeddable, and cross-platform databases suitable for local or client-side use. SpatiaLite extends SQLite with robust geospatial capabilities, enabling storage, management, and analysis of spatial data. It incorporates spatial indexing, follows OGC standards, and supports spatial queries, making it suitable for geospatial applications. We use this combination in local deployment configurations.


## FAQ

**I prefer [*INSERT DB ENGINE*], can I use that instead in my FairDM-based application?**

The answer here is probably yes, but with some caveats. First, you would need to look through the FairDM code base and see what spatial functions and lookups are being utilized. Then, you would need to [check here](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/db-api/#spatial-lookup-compatibility) that your preferred database is compatible. 

Then ask yourself, is it really worth it? FairDM is updated regularly under the assumption that all projects are running PostgreSQL under the hood. For this reason, we reserve the right to make changes to the codebase that could potentially break your application should you choose to use a different database.
