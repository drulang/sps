Session Status Types
====================

A session status is used to determine what actions are
allowed on a session. Here are the basic actions of each
status type:

**New**

  #. Users allowed to join? Yes
  #. Users allowed to leave? Yes
  #. Leader allowed to alter beer list? yes
  #. Leader allowed to remove people? yes
  #. Leader allowed to change session status? yes

**In Progress**

  #. Users allowed to join? Yes
       * New users will not be able to rate beer's that
         have already been rated
  #. Users allowed to leave? Yes
       * If a user leaves while a session is still in
         progress their rated beers will not be deleted
  #. Leader allowed to alter beer list? yes
       * Only beers that have not been closed yet
  #. Leader allowed to remove people? yes
  #. Leader allowed to change session status? yes,
       * Only to a seqno greater than started seqno

**Closed**
  #. Users allowed to join? No
  #. Users allowed to leave? No
  #. Leader allowed to alter beer list? No
  #. Leader allowed to remove people? No
  #. Leader allowed to change session status? No
        * A closed session is final

General Questions
-----------------
  #. What happens if a leader closes a session and not 
     all beers have been rated?
        * `Those beers will remain in the list, but unrated`

Endpoints
---------

.. http:get:: /sessionstatus

    Returns `all` valid session status types

    :query string apptoken: App token

