# Frontend Assets

Geoluminate has switched to a Webpack-based frontend build system allowing for a more modular and maintainable frontend codebase. The frontend codebase is located in the `assets` directory of the repository.

## Design Philosophy

1. Don't go overboard with JavaScript!

    - Geoluminate is designed to be a server-side rendered application so try to keep javascript simple and to the point (e.g. initialising components, simple event listeners).
    - Where possible, allow configuration to frontend components to be passed via html5 data-attributes or Django's [json_script](https://docs.djangoproject.com/en/5.0/ref/templates/builtins/#json-script) template tag. 

2. Use the Django templating system to generate HTML. This allows for a more maintainable and testable codebase.

    Javascript should be used to enhance the user experience, not to create it. Where possible, always use Django's template system to create components.

3. Focus on reducing file size and improving performance by including only necessary components from required libraries.

4. Limit javascript/typescript to initialising components and handling user interactions.


## Frameworks and Libraries

### Bootstrap 5

Bootstrap 5 is the latest edition of the free and open-source CSS framework directed at responsive, mobile-first front-end web development. It contains CSS- and (optionally) JavaScript-based design templates for typography, forms, buttons, navigation, and other interface components.

Geoluminate uses the [Bootstrap](https://getbootstrap.com) CSS framework to provide a consistent look and feel across all Geoluminate-powered portals. This provides consistency, reliability and enhances the user experience across all applications and reduces the amount of time required to develop new applications.

### jQuery

JQuery is a JavaScript library designed to simplify HTML DOM tree traversal and manipulation, as well as event handling, CSS animation, and Ajax. It is free, open-source software using the permissive MIT License. JQuery is the most popular JavaScript library in use today, with installation on 65% of the top 10 million highest-trafficked sites on the Web. It is also required by many of the other javascript libraries that Geoluminate relies on.

### Font Awesome

[Font Awesome](https://fontawesome.com) is a font and icon toolkit based on CSS and Less and was made by Dave Gandy for use with Twitter Bootstrap. The latest Font Awesome is used within Geoluminate to provide a consistent look and feel across all Geoluminate-powered applications. 

### Datatables

[Datatables](https://datatables.net) is a plug-in for the jQuery Javascript library. It is a highly flexible tool, based upon the foundations of progressive enhancement, and will add advanced interaction controls to any HTML table. Datatables is used within Geoluminate to provide highly-interactive tables that integrate directly with the backend framework through the API. 

