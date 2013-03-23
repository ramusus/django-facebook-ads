# -*- coding: utf-8 -*-
from django.core.management.base import AppCommand, LabelCommand
from django.conf import settings
from optparse import make_option
from facebook_ads.models import AdAccount, AdGroup, AdCreative, AdCampaign, AdUser, Targeting, AdImage, AdStatistic

class Command(AppCommand):
    help = 'Fetch all ads data from facebook via API'
    requires_model_validation = True

    option_list = LabelCommand.option_list + (
        make_option('--reset', action='store_true', dest='delete', help='Delete all content data before fetching'),
    )

    def handle(self, **options):
        reset = options.get('reset')

        if reset:
            AdAccount.objects.all().delete()
            AdCampaign.objects.all().delete()
            Targeting.objects.all().delete()
            AdGroup.objects.all().delete()
            AdCreative.objects.all().delete()
            AdUser.objects.all().delete()
            AdStatistic.objects.all().delete()
            AdImage.objects.all().delete()

        for account_number in getattr(settings, 'FACEBOOK_ADS_ACCOUNTS', []):
            account = AdAccount.remote.fetch(account_number)

            account.fetch_campaigns()
            account.fetch_creatives()
            account.fetch_groups()
            account.fetch_images()
            account.fetch_stats()

            account.fetch_stats_campaigns()
            account.fetch_stats_groups()