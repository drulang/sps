Session
====================

The session is the primary entity for SixpackSinday. 

General Questions
-----------------
  #. What happens if a leader closes a session and not 
     all beers have been rated?
     * `Those beers will remain in the list, but unrated`

Endpoints
---------

.. http:get:: /session

    Return all non closed sessions
    
    :query string apptoken: App token
    :query string usertoken: User token
    :query string sessionstatustypcd: Session Status Type Code

.. http:get:: /session/<int:sessionid>

    Returns session profile

    :query string apptoken: App token
    :query string usertoken: User token


.. http:post:: /session

    Create a new session

    :query string apptoken: App token
    :query string usertoken: User token

    :form userid: User who is creating the session and
                  will be marked as the leader

    :form name: Session name
    :form theme: Theme of the session. (i.e. RennFest)
    :form location: Location of sssion which is up to the
                    user. Could be specific like an
                    address or general like Bob's kitchen
                    table
    :form dateopen: Date session is open (YYYY-MM-DD HH:MM:SS)

.. http:put:: /session/<int:sessionid>

    Edit Session profile

    :query string apptoken: App token
    :query string usertoken: User token

    :form name: Session name
    :form sessionstatustypcd: Session status code
    :form theme: Theme of the session. (i.e. RennFest)
    :form location: Location of sssion which is up to the
                    user. Could be specific like an
                    address or general like Bob's kitchen
                    table
    :form dateopen: Date session is open (YYYY-MM-DD HH:MM:SS)
    :form sessionjoincd: Bool indicator of whether to update
                         the session join code. If value is 
                         true then a new code will be generated,
                         anything else will not.

Session Users
-------------

.. http:get:: /session/<int:sessionid>/user

    Returns a list of all users in the session

    :query string apptoken: App token
    :query string usertoken: User token

.. http:get:: /session/<int:sessionid>/user/<int:userid>

    Returns list of information about user as it pertains
    to the session

    :query string apptoken: App token
    :query string usertoken: User token

.. http:post:: /session/<int:sessionid>/user

    Add a user to the session

    :query string apptoken: App token
    :query string usertoken: User token

    :form userid: Userid
    :form userroletypcd: User's role in the group
    :form userjoincd: The code to join the session


.. http:put:: /session/<int:sessionid>/user/<int:userid>

    Update user as far in the session

    :query string apptoken: App token
    :query string usertoken: User token

    :form userroletypcd: User's role in the group. Only leader is
                         allowed to change this

.. http:delete:: /session/<int:sessionid>/user/<int:userid>

    Remove user from session

    :query string apptoken: App token
    :query string usertoken: User token

Session Beer
------------

A session beer can only be added/deleted while the session is in the new phase.

.. http:get:: /session/<int:sessionid>/beer

    Get all beers registered for the session
    
    :query string apptoken: App token
    :query string usertoken: User token
    :query string beersessionstatustypcd: Filter by Beer Session Status

.. http:get:: /session/<int:sessionid>/beer/<int:sessionbeerid>

    Return beer profile for the session. Includes the 
    session beer status
    
    :query string apptoken: App token
    :query string usertoken: User token

.. http:post:: /session/<int:sessionid>/beer

    Add a beer to the session. Only leader of session can do this
    
    :query string apptoken: App token
    :query string usertoken: User token

    :form beerid: One beer id or a CSV list of beer ids.
                  Ex: sj327,97wj2,923jl

.. http:put:: /session/<int:sessionid>/beer

    Update session's beers as a group

    :query string apptoken: App token
    :query string usertoken: User token

    :form sequence: CSV list of **sessionbeerids** where the sequence of the list maps to the sequence of the session

.. http:put:: /session/<int:sessionid>/beer/<int:sessionbeerid>
    
    Update beer in session

    :query string apptoken: App token
    :query string usertoken: User token

    :form beersessionstatustypcd: The status of the beer in the session
    :form seqno: The sequence number of the beer in the session

.. http:delete:: /session/<int:sessionid>/beer/<int:sessionbeerid>

    Remove beer from session. Cannot be remove if session is closed or if beer is in a state other than new
    
    :query string apptoken: App token
    :query string usertoken: User token

Session Ratings
---------------


.. http:get:: /session/<int:sessionid>/beer/<int:sessionbeerid>/rating

    Return `all` session beer ratings for this beer
    
    :query string apptoken: App token
    :query string usertoken: User token
    :query int userid: Filter by userid
    :query string ratingtypcd: Filter by rating type

.. http:get:: /session/<int:sessionid>/beer/<int:sessionbeerid>/rating/<int:ratingid>

    Retrieve rating information

    :query string apptoken: App token
    :query string usertoken: User token


.. http:post:: /session/<int:sessionid>/beer/<int:sessionbeerid>/rating

    Create a new rating for the the session beer

    :query string apptoken: App token
    :query string usertoken: User token

    :form userid: User ID
    :form ratingval:  Rating Value
    :form ratingtypcd:  Rating Type (i.e Hoppy)
    :form comment:  User's comment. (Limit: 500 chars)

.. http:put:: /session/<int:sessionid>/beer/<int:sessionbeerid>/rating/<int:beerratingid>

    Update rating. `Only author of rating can change it. Also a beer can not be changed once it's closed``

    :query string apptoken: App token
    :query string usertoken: User token

    :form ratingval:  Rating Value
    :form comment: User comment(limit 500 chars)

.. http:delete:: /session/<int:sessionid>/beer/<int:sessionbeerid>/rating/<int:beerratingid>

    Delete rating. `Only author of rating can change it. Cannot be deleted once beer is closed.`

    :query string apptoken: App token
    :query string usertoken: User token

Session Events
---------------

.. http:get:: /session/<int:sessionid>/event

    Retrive events for a session

    :query string apptoken: App token
    :query string usertoken: User token
    :query int n: Number of events to return
    :query int startindex: Subscript index start
    :query int endindex: Subscript index end

