"""CLI - Validators."""
from __future__ import absolute_import, print_function, unicode_literals

import base64
import sys

import click


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
BAD_API_HEADERS = ('user-agent', 'host')
API_HEADER_TRANSFORMS = {'authorization': 'transform_api_header_authorization'}


def transform_api_header_authorization(param, value):
    """Transform a username:password value into a base64 string."""
    try:
        username, password = value.split(':', 1)
    except ValueError:
        raise click.BadParameter(
            'Authorization header needs to be Authorization=username:password',
            param=param)

    value = base64.b64encode('%(username)s:%(password)s' % {
        'username': username.strip(),
        'password': password
    })

    return 'Basic %(value)s' % {'value': value}


def validate_api_headers(ctx, param, value):
    """Validate that API headers is a CSV of k=v pairs."""
    # pylint: disable=unused-argument
    if not value:
        return {}

    headers = {}
    for kv in value.split(','):
        try:
            k, v = kv.split('=', 1)
            k = k.strip().lower()

            for bad_header in BAD_API_HEADERS:
                if bad_header == k:
                    raise click.BadParameter(
                        '%(key)s is not an allowed header' % {
                            'key': bad_header
                        },
                        param=param)

            if k in API_HEADER_TRANSFORMS:
                module = sys.modules[__name__]
                transform = getattr(module, API_HEADER_TRANSFORMS[k])
                v = transform(param, v)
        except ValueError:
            raise click.BadParameter(
                'Values need to be a CSV of key=value pairs',
                param=param)

        headers[k] = v

    return headers


def validate_slashes(param, value, minimum=2, maximum=None, form=None):
    """Ensure that parameter has slashes and minimum parts."""
    try:
        value = value.split('/')
    except ValueError:
        value = None

    if value:
        if len(value) < minimum:
            value = None
        elif maximum and len(value) > maximum:
            value = None

    if not value:
        form = form or '/'.join('VALUE' for _ in range(minimum))
        raise click.BadParameter(
            'Must be in the form of %(form)s' % {'form': form},
            param=param)

    value = [v.strip() for v in value]
    if not all(value):
        raise click.BadParameter(
            'Individual values cannot be blank',
            param=param)

    return value


def validate_owner_repo(ctx, param, value):
    """Ensure that owner/repo is formatted correctly."""
    # pylint: disable=unused-argument
    form = 'OWNER/REPO'
    return validate_slashes(param, value, minimum=2, maximum=2, form=form)


def validate_owner_repo_package(ctx, param, value):
    """Ensure that owner/repo/package is formatted correctly."""
    # pylint: disable=unused-argument
    form = 'OWNER/REPO/PACKAGE'
    return validate_slashes(param, value, minimum=3, maximum=3, form=form)


def validate_owner_repo_distro(ctx, param, value):
    """Ensure that owner/repo/distro/version is formatted correctly."""
    # pylint: disable=unused-argument
    form = 'OWNER/REPO/DISTRO[/RELEASE]'
    return validate_slashes(param, value, minimum=3, maximum=4, form=form)
