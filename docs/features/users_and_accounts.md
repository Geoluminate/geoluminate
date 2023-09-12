# Users & Accounts

One of the goals of Geoluminate is to streamline the process of formally publishing datasets which you can read more about [here](publishing_datasets). There are a few key players when it comes to publishing datasets, but possibly none moreso than DataCite. DataCite have defined there own schema for describing datasets which you can read more about [here](https://schema.datacite.org/meta/kernel-4.3/). There is absolutely no intent within this framework to redefine such schemas that already effectively describe datasets. Instead, the aim is to adapt our core database structure to make it as simple as possible to extract the necessary information and reformat to fit existing schemas.

With this in mind, our user accounts application is designed to reflect the contributors schema set out by DataCite. 


There are four core models in our application that handle what DataCite refer to as contributors. These are the User, Organisation, Profile, and Contributor models. The User model is the default model provided by Django and is used to handle authentication. The Organisation model is used to store information about the organisation that the user is affiliated with. The Profile model is used to store information about the user, such as their name, email address, and ORCID. The Contributor model is used to store information about the user's role in the dataset, such as their role, their ORCID, and their organisation.

## User Accounts


