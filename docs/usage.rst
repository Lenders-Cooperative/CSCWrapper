=====
Usage
=====

To use Django CSCWrapper in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_cscwrapper.apps.DjangoCscwrapperConfig',
        ...
    )

Add Django CSCWrapper's URL patterns:

.. code-block:: python

    from django_cscwrapper import urls as django_cscwrapper_urls


    urlpatterns = [
        ...
        url(r'^', include(django_cscwrapper_urls)),
        ...
    ]
