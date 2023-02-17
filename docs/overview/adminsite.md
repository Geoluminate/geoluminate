# The Administration Site

One of the standout features of developing with Django is the automatic creation of a fully functioning administration site that allows database administrators to create, read, update and delete basically anything contained within the database. The current version of Django ships with a reasonable default admin theme which is fine for smaller projects, however, we have found the lack of customization options to be frustrating as the number of external applications added to a project increases.

## Existing 3rd Party Admin Themes

Initially, we decided to use the open-source Django Grappelli admin theme because it is very highly rated within the Django community and provides some excellent out-of-the-box functionality. However, it has some shortcomings including a non-responsive design (i.e. doesn't look good on mobile) and a custom, non-familiar theme that we found difficult to override on occasions. For this reason, we ended up switching to a different admin theme provided by Django Jazzmin which is built on the ever-popular Bootstrap CSS framework.

Some features of Django Jazzmin include:

- Based on [AdminLTE](https://adminlte.io) and [Bootstrap 4](https://getbootstrap.com/docs/4.0/)
- Easily customisable\*
- Modals instead of popup windows
- Responsive design

:::{note}
While Jazzmin is indeed easily customisable, Geoluminate already provides customizations that are designed to benefit administrators of Geoluminate powered database applications. Therefore we suggest only toying with further Jazzmin configurations if you are very comfortable with Django and understand the modifications already made by Geoluminate.
:::

## Geoluminate Customizations

Further customizations made specifically for Geoluminate applications are provided in the builtin {doc}`geoluminate.contrib.admin` application.

% * CRUD style admin interface

% * Object level user permissions

% * Import/export capable

% * Invitation system

% * Object history tracking

% * Newsletters

% * Literature management

% * ORCID based user authentication

% * Site lockdown capabilities

% * User organisations
