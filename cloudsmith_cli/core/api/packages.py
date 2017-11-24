"""API - Packages endpoints."""
from __future__ import absolute_import, print_function, unicode_literals
import inspect

import cloudsmith_api
import six
from .exceptions import catch_raise_api_exception


def get_packages_api():
    """Get the packages API client."""
    config = cloudsmith_api.Configuration()
    client = cloudsmith_api.PackagesApi()
    if config.user_agent:
        client.api_client.user_agent = config.user_agent
    return client


def create_package(package_format, owner, repo, payload):
    """Create a new package in a repository."""
    client = get_packages_api()

    with catch_raise_api_exception():
        upload = getattr(client, 'packages_upload_%s' % package_format)
        data = upload(
            owner=owner,
            repo=repo,
            data=payload
        )

    return data.slug_perm, data.slug


def delete_package(owner, repo, slug):
    """Delete a package in a repository."""
    client = get_packages_api()

    with catch_raise_api_exception():
        client.packages_delete(
            owner=owner,
            repo=repo,
            slug=slug
        )


def get_package_status(owner, repo, slug):
    """Get the status for a package in a repository."""
    client = get_packages_api()

    with catch_raise_api_exception():
        data = client.packages_status(
            owner=owner,
            repo=repo,
            slug=slug
        )

    return (
        data.is_sync_completed, data.is_sync_failed, data.sync_progress,
        data.status_str, data.stage_str
    )


def get_package_formats():
    """Get the list of available package formats and parameters."""
    # HACK: This obviously isn't great, and it is subject to change as
    # the API changes, but it'll do for now as a interim method of
    # introspection to get the parameters we need.
    def get_parameters(cls):
        params = {}

        # Create a dummy instance so we can check if a parameter is required.
        # As with the rest of this function, this is obviously hacky. We'll
        # figure out a way to pull this information in from the API later.
        dummy_kwargs = {
            k: 'dummy'
            for k in cls.swagger_types
        }
        instance = cls(**dummy_kwargs)

        for k, v in six.iteritems(cls.swagger_types):
            attr = getattr(cls, k)
            docs = attr.__doc__.strip().split("\n")
            doc = (docs[1] if docs[1] else docs[0]).strip()

            try:
                setattr(instance, k, None)
                required = False
            except ValueError:
                required = True

            params[cls.attribute_map.get(k)] = {
                'type': v,
                'help': doc,
                'required': required
            }

        return params

    return {
        key.replace('PackagesUpload', '').lower(): get_parameters(cls)
        for key, cls in inspect.getmembers(cloudsmith_api.models)
        if key.startswith('PackagesUpload')
    }