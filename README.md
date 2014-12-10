# Django Facebook Graph API Ads

[![Build Status](https://travis-ci.org/ramusus/django-facebook-ads.png?branch=master)](https://travis-ci.org/ramusus/django-facebook-ads) [![Coverage Status](https://coveralls.io/repos/ramusus/django-facebook-ads/badge.png?branch=master)](https://coveralls.io/r/ramusus/django-facebook-ads)

Application for interacting with Facebook Graph API Ads objects using Django model interface

## Installation

    pip install django-facebook-ads

Add into `settings.py` lines:

    INSTALLED_APPS = (
        ...
        'oauth_tokens',
        'facebook_api',
        'facebook_ads',
    )

    # oauth-tokens settings
    OAUTH_TOKENS_HISTORY = True                                        # to keep in DB expired access tokens
    OAUTH_TOKENS_FACEBOOK_CLIENT_ID = ''                               # application ID
    OAUTH_TOKENS_FACEBOOK_CLIENT_SECRET = ''                           # application secret key
    OAUTH_TOKENS_FACEBOOK_SCOPE = ['offline_access']                   # application scopes
    OAUTH_TOKENS_FACEBOOK_USERNAME = ''                                # user login
    OAUTH_TOKENS_FACEBOOK_PASSWORD = ''                                # user password

## Usage examples

###