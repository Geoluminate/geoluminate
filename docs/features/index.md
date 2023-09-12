# Core Features

As mentioned throughout this documentation, the point of Geoluminate as a framework is to make many application design decisions for you so that you can concentrate on getting your schema right! This section will highlight some of the features that Geoluminate provides out of the box.

## Django

Geoluminate is built around the [Django Web Framework](https://www.djangoproject.com). Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. It is also free and open source. Django is a great choice for building web applications because it provides a lot of the functionality that you would otherwise have to build yourself. For example, Django provides a robust [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping) that allows you to interact with your database without having to write any SQL. It also provides a [templating engine](https://docs.djangoproject.com/en/3.1/topics/templates/) that allows you to write HTML templates that can be rendered by your web application. Django also provides a [user authentication system](https://docs.djangoproject.com/en/3.1/topics/auth/) that allows you to easily manage users and permissions. These are just a few of the many features that Django provides out of the box. You can read more about the features Django provides [here](https://www.djangoproject.com/start/overview/).

Before using Geoluminate, it is not necessary, but helpful, to have a basic understand of how Django works. Take the time to check out


In saying this, one must still spend a significant amount of time designing how your application will work. Django does not do this for you. It is up to you to design your application and then use Django to implement it. This is where Geoluminate comes in. Geoluminate provides a set of tools and components that you can use to build your application. It also provides a set of best practices that you can follow to ensure that your application is built in a way that is consistent with other Geoluminate applications. This means that if you are familiar with one Geoluminate application, you will be familiar with all of them. This is a huge benefit for the Geoluminate community as it means that we can all help each other out and share our experiences. 

## Geoluminate



## Bootstrap

Geoluminate uses the [Bootstrap](https://getbootstrap.com) CSS framework to provide a consistent look and feel across all Geoluminate applications. Bootstrap is a free and open-source CSS framework directed at responsive, mobile-first front-end web development. It contains CSS- and (optionally) JavaScript-based design templates for typography, forms, buttons, navigation, and other interface components.

## jQuery

Geoluminate uses the [jQuery](https://jquery.com) JavaScript library to provide a consistent look and feel across all Geoluminate applications. jQuery is a JavaScript library designed to simplify HTML DOM tree traversal and manipulation, as well as event handling, CSS animation, and Ajax. It is free, open-source software using the permissive MIT License.

## Font Awesome

Geoluminate uses the [Font Awesome](https://fontawesome.com) icon library to provide a consistent look and feel across all Geoluminate applications. Font Awesome is a font and icon toolkit based on CSS and Less. It was made by Dave Gandy for use with Twitter Bootstrap, and later was incorporated into the BootstrapCDN.

## Datatables

Geoluminate uses the [Datatables](https://datatables.net) JavaScript library to provide a consistent look and feel across all Geoluminate applications. DataTables is a plug-in for the jQuery Javascript library. It is a highly flexible tool, based upon the foundations of progressive enhancement, and will add advanced interaction controls to any HTML table.



## Why/why not a javascript framework?

A lot of modern day web applications are built using javascript web frameworks. However, there are some pros and cons involved.

Pros:

1. They are great for creating highly interactive and dynamic user interfaces that provide a smoother and more responsive user experience.
2. They have the ability to create Single Page Applications which provide a better user experience. E.g. no page loads.
3. They follow a client-server architecture where the frontend and backend are decoupled. This separation of concerns allows for easier scalability and independent development of the frontend and backend components of your application.

Cons:

*These are written from the perspective that you are NOT an experienced web developer already and probably working on your own (not in a software dev team)*

1. You must have a working knowledge of javascript (which is not common among researchers). If not, then you will need to learn javascript on top of web development.
2. Decoupled front and back ends means that you will need to learn how to develop both independently and then learn how they interact with each other.  
3. Best practices in Javascript frameworks are frequently evolving. What works best today will not be best practice tomorrow. This means you will have to stay up-to-date with the latest trends and practices. 


Full-stack frameworks such as Django or Ruby on Rails are considered such because they handle both front-end and back-end code simultaneously. Both are [HTTP](https://en.wikipedia.org/wiki/HTTP)-based (this is literally what the web was designed for!), both provide powerful [ORM](https://en.wikipedia.org/wiki/Object–relational_mapping)s (Object-Relational Mapping) which simplifies database management and both follow a [Model-View-Controller](https://en.wikipedia.org/wiki/Model–view–controller) (MVC) architectural pattern.





Geoluminate makes some significant design decisions for you and this section is provided to try and explain what those decisions are and why we made them. We try to make decisions based on our understanding of current best practices in the Django community, the availability of open source tools and any advice we can find online from people that are really experienced in this sort of thing. If, while reading through this section you find a decision that you don't quite agree with or think something could be done better, why not {ref}`learn how to contribute to Geoluminate <CONTRIBUTING:Contributing>`?


## Features

```{toctree}
:maxdepth: 1

backend
database
adminsite
roles

```
