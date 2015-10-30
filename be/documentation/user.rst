User
====

.. http:get:: /user/<int:userid>

    Get a user's profile

    :query string apptoken: App token
    :query string usertoken: User token

.. http:post:: /user

    Creates a new user

    :query string apptoken: App token

    :form username: Desired username
    :form email: User email
    :form password: User password
    :form firstname: User first name
    :form lastname:  User last name

.. http:put:: /user/<int:userid>

    Edit user profile

    :query string apptoken: App token
    :query string usertoken: User token

    :form password: User password
    :form firstname: User first name
    :form lastname:  User last name

.. http:delete:: /user/<int:userid>

    Inactivate user

    :query string apptoken: App token
    :query string usertoken: User token

User Token
==========

.. http:post:: /user/login

    Logs a user in and returns a token to be used
    throught the API

    :query string apptoken: App token

    :form username: Username
    :form password: User password


.. http:delete:: /user/logout

    Log a user out rendering the usertoken invalid

    :query string apptoken: App token
    :query string usertoken: App token

