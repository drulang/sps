Beer
=============

.. http:get:: /beer

    Return all beers in cache

    :query string apptoken: App token

.. http:get:: /beer/<string:beerid>

    Returns beer profile

    :query string apptoken: App token

.. http:get:: /beer/<string:beerid>/brewery

    Return breweries for a beer

    :query string apptoken: App token

.. http:get:: /beer/search
    Search for beers, breweries

    :query string apptoken: App token
    :query string q: Query String
    :query string p: Page number
    :query string type: Beer or Brewery


.. http:get:: /brewery

    Return all beers in cache

    :query string apptoken: App token

.. http:get:: /brewery/<string:breweryid>

    Return brewery profile

    :query string apptoken: App token

.. http:get:: /brewery/<string:breweryid>/beer

    Return beers for a brewery

    :query string apptoken: App token

