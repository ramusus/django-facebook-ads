# -*- coding: utf-8 -*-
import csv
from datetime import timedelta, datetime
import logging
import time

from dateutil import parser, relativedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _
from facebook_api import fields
from facebook_api.api import api_call
from facebook_api.models import FacebookGraphModel, FacebookGraphManager


class CSVFormatError(ValueError):
    pass

log = logging.getLogger('facebook_ads.models')

CAMPAIGN_STATUS_CHOICES = (
    (1, _('active')),
    (2, _('paused')),
    (3, _('deleted')),
)

ACCOUNT_STATUS_CHOICES = (
    (1, _('active')),
    (2, _('disabled')),
    (3, _('unsettled')),
)

ADGROUP_STATUS_CHOICES = (
    (1, _('active')),
    (3, _('deleted')),
    (4, _('pending review')),
    (5, _('dissaproved')),
    (8, _('campaign paused')),
    (9, _('adgroup paused')),
)

BID_TYPE_CHOICES = (
    (1, _('CPC')),
    (2, _('CPM')),
)

ADCREATIVE_TYPE_CHOICES = (
    (1, _('Basic ad for an external website')),
    (2, _('Social ad for a Facebook Page/Place')),
    (3, _('Social ad for an event RSVP')),
    (4, _('Social ad for a Facebook application')),
    (8, _('Sponsored stories for stories created by a Facebook application')),
    (9, _('Sponsored stories about a Page/Place like event')),
    (10, _('Sponsored stories about a Place check-in event')),
    (16, _('Sponsored stories about people using a Facebook application or playing a game')),
    (17, _('Sponsored stories about a Page/Place\'s posts like event')),
    (19, _('Sponsored stories about liking or sharing something from an external domain')),
    (25, _(
        'Sponsored stories about likes for a specific page post, comments for a specific page post, and RSVPs for a specific event')),
    (27, _('Sponsored stories for a Page post')),
)

ADCREATIVE_RUN_STATUS_CHOICES = (
    (1, _('active')),
    (3, _('deleted')),
)

TARGETING_GENDER_CHOICES = (
    ('', _('all')),
    (1, _('male')),
    (2, _('female')),
)

TARGETING_BROAD_AGE_CHOICES = (
    (0, _('disabled')),
    (1, _('enabled')),
)

ADUSER_ROLE_CHOICES = (
    (1001, _('administrator access')),
    (1002, _('general-user (ad manager) access')),
    (1003, _('reports-only access')),
)

ADUSER_PERMISSIONS_CHOICES = (
    (1, _('ACCOUNT_ADMIN: modify the set of users associated with the given account.')),
    (2, _('ADMANAGER_READ: view campaigns and ads')),
    (3, _('ADMANAGER_WRITE: manage campaigns and ads')),
    (4, _('BILLING_READ: view account billing information')),
    (5, _('BILLING_WRITE: modify the account billing information')),
    (7, _('REPORTS: run reports')),
)


class AdUser(FacebookGraphModel):

    class Meta:
        verbose_name = 'Facebook ad user permissions'
        verbose_name_plural = 'Facebook ad users permissions'
        unique_together = ('account', 'uid')

    account = models.ForeignKey('AdAccount', related_name='users')
    uid = models.BigIntegerField(help_text='The User ID of the user')
    permissions = models.CommaSeparatedIntegerField(
        max_length=20, choices=ADUSER_PERMISSIONS_CHOICES, help_text='An array of the permissions that user has.')
    role = models.IntegerField(choices=ADUSER_ROLE_CHOICES, help_text='The role of the user')

    objects = models.Manager()  # because we need it as a default manager for AdAccount many-to-many relations
    remote = FacebookGraphManager(('account', 'uid'))

    def __unicode__(self):
        return 'User #%s' % self.uid


class AdAccount(FacebookGraphModel):

    class Meta:
        verbose_name = 'Facebook account'
        verbose_name_plural = 'Facebook accounts'

    account_id = models.BigIntegerField(help_text='The ID of the ads account', unique=True)
    name = models.CharField(
        max_length=100, blank=True, help_text='Name of the account; note that many accounts are unnamed, so this field may be empty')
    account_status = models.SmallIntegerField(
        choices=ACCOUNT_STATUS_CHOICES, null=True, blank=True, help_text='Status of the account (1 for active, 2 for disabled, or 3 for unsettled)')
    daily_spend_limit = models.IntegerField(
        null=True, blank=True, help_text='The account\'s limit for daily spend, based on the corresponding value in the account settings')
    currency = models.CharField(
        max_length=100, blank=True, help_text='The currency used for the account, based on the corresponding value in the account settings')
    timezone_id = models.IntegerField(null=True, blank=True, help_text='ID for the timezone')
    timezone_name = models.CharField(max_length=100, blank=True, help_text='Name for the time zone')
#    capabilities = models._Field(help_text='Reserved for future use')    ads_management    array
# account_groups = models._Field(help_text='Container for the ID, name,
# and status of the account\'s account groups')    ads_management    array
    is_personal = models.IntegerField(null=True, blank=True, help_text='If this is a personal or business account')
    business_name = models.CharField(max_length=100, blank=True, help_text='The business name for the account')
    business_street = models.CharField(
        max_length=100, blank=True, help_text='First line of the business street address for the account')
    business_street2 = models.CharField(
        max_length=100, blank=True, help_text='Second line of the business street address for the account')
    business_city = models.CharField(max_length=100, blank=True, help_text='City for business address')
    business_state = models.CharField(max_length=100, blank=True, help_text='State abbreviation for business address')
    business_zip = models.CharField(max_length=100, blank=True, help_text='Zip code for business address')
    business_country_code = models.CharField(
        max_length=100, blank=True, help_text='Country code for the business address')
    vat_status = models.IntegerField(
        null=True, blank=True, help_text='Vat status code for the account. Here are the values for VAT Status: 0: Unknown, 1: VAT not required- US/CA, 2: VAT information required, 3: VAT information submitted, 4: Offline VAT validation failed, 5: Account is a personal account')
# agency_client_declaration = models._Field(help_text='Whether this
# account is an agency advertising on behalf of the client')
# ads_management    array

    remote = FacebookGraphManager('account_id', 'act_%s')

    def __unicode__(self):
        return '%s #%s' % (self.name or 'Account', self.account_id)

    def fetch_campaigns(self):
        '''
        Retrieve and save all campaigns for account
        '''
        if not self.id:
            log.error('It is neccesary to save account before saving campaigns')

        response = api_call('act_%s/adcampaigns' % self.account_id)

        instances = []
        for resource in response.data:
            instance = AdCampaign.remote.get_or_create_from_resource(resource)
            instances += [instance]

        return instances

    def fetch_creatives(self):
        '''
        Retrieve and save all creatives for account
        '''
        response = api_call('act_%s/adcreatives' % self.account_id)

        instances = []
        for resource in response.data:
            instance = AdCreative.remote.get_or_create_from_resource(resource)
            instances += [instance]

        return instances

    def fetch_groups(self):
        '''
        Retrieve and save all groups for account
        '''
        response = api_call('act_%s/adgroups' % self.account_id)

        instances = []
        for resource in response.data:
            instance = AdGroup.remote.get_or_create_from_resource(resource)
            instances += [instance]

        return instances

    def fetch_images(self):
        '''
        Retrieve and save images for account
        '''
        response = api_call('act_%s/adimages' % self.account_id)

        instances = []
        for resource in response.data.values():
            instance = AdImage.remote.get_or_create_from_resource(resource)
            instances += [instance]

        return instances

    def fetch_stats(self):
        '''
        Retrieve and save statistic for account
        '''
        response = api_call('act_%s/stats' % self.account_id)
        instance = AdStatistic.remote.get_or_create_from_resource(response)
        return instance

    def fetch_stats_campaigns(self):
        '''
        Retrieve and save statistic for campaigns of account
        TODO: act_AccountID/adcampaignstats?campaign_ids=[JSON-encoded array of campaign IDs]
        '''
        response = api_call('act_%s/adcampaignstats' % self.account_id)

        instances = []
        for resource in response.data:
            instance = AdStatistic.remote.get_or_create_from_resource(resource)
            instances += [instance]

        return instances

    def fetch_stats_groups(self):
        '''
        Retrieve and save statistic for groups of accout
        TODO: act_AccountID/adgroupstats?adgroup_ids=[JSON-encoded array of ad group IDs]
        '''
        response = api_call('act_%s/adgroupstats' % self.account_id)

        instances = []
        for resource in response.data:
            instance = AdStatistic.remote.get_or_create_from_resource(resource)
            instances += [instance]

        return instances


class AdCampaign(FacebookGraphModel):

    class Meta:
        verbose_name = 'Facebook ad campaign'
        verbose_name_plural = 'Facebook ad campaigns'

    campaign_id = models.BigIntegerField(help_text='The campaign ID', unique=True)
    account = models.ForeignKey(
        AdAccount, related_name='campaigns', help_text='Used to create another campaign with the same account ID')
    name = models.CharField(
        max_length=100, help_text='Campaign name of 100 characters or less; required to create a new campaign')
    start_time = models.DateTimeField(
        null=True, blank=True, help_text='A unix timestamp; optional when creating and updating campaigns')
    end_time = models.DateTimeField(
        null=True, blank=True, help_text='A unix timestamp; optional when creating and updating campaigns')
    daily_budget = models.IntegerField(
        null=True, blank=True, help_text='Defined in cents, minimum 100; daily or lifetime budget must be set when creating a a campaign; can be updated')
    campaign_status = models.SmallIntegerField(choices=CAMPAIGN_STATUS_CHOICES, null=True, blank=True,
                                               help_text='A campaign status is active (status 1), paused (status 2), or deleted (status 3)')
    lifetime_budget = models.IntegerField(
        null=True, blank=True, help_text='Defined in cents, minimum 100; can be updated; either a lifetime_budget or a daily_budget can be set (not both), and an updated budget begins spending from zero (if there\'s a switch in budget types, the entire campaign-spend, to date, is set to zero); if money already was spent on the campaign today, that money is not counted towards the new budget; an advertiser may be charged up to the sum of the old spend, plus any new spend that occurs in the campaign; for more information, see the Facebook Help')

    # not exist in API docs
    daily_imps = models.IntegerField(null=True, blank=True)
    updated_time = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    remote = FacebookGraphManager('campaign_id')

    def __unicode__(self):
        return self.name

    def parse(self, response):
        super(AdCampaign, self).parse(response)
        try:
            self.account = AdAccount.objects.get(account_id=response['account_id'])
        except AdAccount.DoesNotExist:
            raise Exception('Impossible to save campaign "%s" (%d) for unexisted account %s' %
                            (self.name, self.campaign_id, response['account_id']))

    def fetch_groups(self):
        '''
        Retrieve and save all groups for campaign
        '''
        response = api_call('%s/adgroups' % self.campaign_id)

        instances = []
        for resource in response.data:
            instance = AdGroup.remote.get_or_create_from_resource(resource)
            instances += [instance]

        return instances

    def fetch_stats(self):
        '''
        Retrieve and save statistic for campaign
        '''
        response = api_call('%s/stats' % self.campaign_id)
        instance = AdStatistic.remote.get_or_create_from_resource(response)
        return instance


class AdCreative(FacebookGraphModel):

    class Meta:
        verbose_name = 'Facebook ad creative'
        verbose_name_plural = 'Facebook ad creatives'

    creative_id = models.BigIntegerField(
        help_text='Required in order to use an existing creative from the creative library', unique=True)
    name = models.CharField(max_length=100, help_text='The name of the creative in the creative library')
    type = models.IntegerField(choices=ADCREATIVE_TYPE_CHOICES, null=True,
                               help_text='The number of the ad type, which identifies the type of sponsored story or ad')
    object_id = models.BigIntegerField(
        null=True, blank=True, help_text='The Facebook object ID that is relevant to the ad and ad type')
    body = models.CharField(max_length=135, help_text='The body of the ad, not applicable to sponsored stories')
    image_hash = models.CharField(
        max_length=32, help_text='Image ID for an image you can use in creatives and thus in ads')
    image_url = models.URLField(max_length=100, help_text='A URL for the image for this creative')
    count_current_adgroups = models.CharField(
        max_length=100, help_text='Indicates the number of ad groups in which the creative is used')
    title = models.CharField(max_length=25, help_text='Title for a default ad')
    run_status = models.SmallIntegerField(
        choices=ADCREATIVE_RUN_STATUS_CHOICES, null=True, help_text='Indicates whether the creative is available or deleted')
    link_url = models.URLField(max_length=1024, help_text='A URL for the ad')
    preview_url = models.URLField(
        max_length=100, help_text='The URL to preview the ad, only for the current session user')
    related_fan_page = models.CharField(max_length=100, help_text='Provides social context to a type 1 ad')
    auto_update = models.BooleanField(
        help_text='Boolean true to constantly promote the latest page post and ignore story_id parameter. Boolean false to promote a specific page post by story_id. Required for type 27 ads only.')
    story_id = models.BigIntegerField(
        null=True, blank=True, help_text='The fbid of a page post to use in a type 25 or type 27 ad. This ID can be retrieved by using the graph API to query the posts of the page.')
# query_templates = models._Field(help_text='An array of numbers
# corresponding to the type of sponsored story for a type 25 ad
# (query-based sponsored stories). Current valid values are 6 (likes for a
# specific page post), 7 (comments for a specific page post), and 8 (RSVPs
# for a specific page event).') ads_management    array of int

    # not exist in API docs
    view_tag = models.CharField(max_length=100)

    remote = FacebookGraphManager('creative_id')

    def parse(self, response):
        super(AdCreative, self).parse(response)
        if not self.creative_id and response['id']:
            self.creative_id = response['id']

        # integerify fields
        for field_name in ['type', 'story_id', 'object_id', 'creative_id']:
            try:
                setattr(self, field_name, int(getattr(self, field_name)))
            except:
                pass

    def clean(self):
        '''
        Validate the maximum allowable length of an individual word in an ad’s body or title
        '''
        super(AdCreative, self).clean()

        words = self.body.split()
        for word in words:
            if len(word) > 20:
                raise ValidationError(
                    'The maximum allowable length of an individual word in an ad’s body : 20 characters')
        words = self.title.split()
        for word in words:
            if len(word) > 20:
                raise ValidationError(
                    'The maximum allowable length of an individual word in an ad’s title : 20 characters')


class Targeting(FacebookGraphModel):

    '''
    Targeting model connected OneToOne to AdGroup model
    '''
    class Meta:
        verbose_name = 'Facebook ad targeting'
        verbose_name_plural = 'Facebook ad targetings'

    # Location
    countries = fields.CommaSeparatedCharField(
        max_length=100, blank=True, help_text='Values for country targeting. The countries parameter is the only required targeting parameter. It must be an array of country codes. See Retrieving Autocomplete Data. Limit: 25 countries.')
    cities = fields.JSONField(
        null=True, blank=True, help_text='Values for city targeting. For the values you can use, see Retrieving Autocomplete Data. For cities in the US or Canada, specify the two letter state or province code, e.g. "name":"New York,NY" (or for international cities, the country name, e.g. "name":"Paris,France"). Alternatively, specify "id":"2421215","name":"Palo Alto, CA". Limit: 200 cities.')
    zips = models.CharField(
        max_length=100, help_text='String array of 5-digit ZIP codes (postal codes) specified by the United States Postal Service. For example: \'94304\'. Currently, the zips parameter does not support international postal codes, autocomplete, the radius parameter, or a countries parameter specification outside of \'US\'. See Zip Code Targeting. Limit: 2500 zip codes.')
    regions = models.CharField(
        max_length=100, help_text='State, province, or region. To get the available values, see Retrieving Autocomplete Data. Limit: 200 regions.')
    radius = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text='Must be used in conjunction with cities. Specifies a radius around cities.')
    locales = models.CharField(
        max_length=100, help_text='Locales. To get the available values, see Retrieving Autocomplete Data. Alternatively, if you use the Autocomplete file (referenced above), the values are specified as indices; the indices are in a sub-array called \'locales\'. Uses of this parameter include for targeting users with a different language than the common language for the specified location parameter; you specify an ID for the language, e.g. 5 for German. Limit: 50 locales.')

    # Likes and interests
    keywords = fields.CommaSeparatedCharField(
        max_length=4000, help_text='Array of keyword strings for precise interest targeting. The keywords parameter applies only to precise interest targeting. See topic targeting. Keywords (either topic keywords or non-topic keywords) are matched to data from users profiles. For example, if an advertiser sells cameras, targeting parameters could specify users who are interested in photography. You can POST targeting data to /act_{account-id}/reachestimate to determine if proposed keywords match any profiles. Limit: 200 keywords.')
    user_adclusters = fields.JSONField(
        null=True, blank=True, help_text='Array of ID-name pairs for broad-category targeting (BCT). The user_adclusters parameter applies only for BCT, which cannot be used with precise interest targeting. To include BCT in an ad, use act_{account-id}/broadtargetingcategories. For an example of how to use this parameter, see broad category targeting, above. Limit: 50 ID-name pairs.')
    interested_in = models.CharField(
        max_length=100, help_text='Indicates targeting based on the "interested in" field of the user profile. You can specify an integer of 1 to indicate MALE (for example, if you specify "interested_in":[1]). An integer of 2 indicates FEMALE. The default of ALL is used if you specify Null. The default of ALL is also used if you do not specify the field. Do not specify zero. Please note "interested in" targeting is not available in France due to local laws.')

    # Demographics and events
    genders = fields.CommaSeparatedCharField(choices=TARGETING_GENDER_CHOICES, max_length=5, null=True, blank=True,
                                             help_text='Indicates gender-based targeting. You can specify an integer of 1 to indicate MALE (for example, if you specify "genders":[1]). An integer of 2 indicates FEMALE. The default of ALL is used if you specify Null. The default of ALL is also used if you do not specify the field. Do not specify zero.')
    age_min = fields.PositiveSmallIntegerRangeField(
        min_value=13, max_value=65, null=True, blank=True, help_text='Minimum age. If used, must be 13 or higher.')
    age_max = fields.PositiveSmallIntegerRangeField(
        min_value=13, max_value=65, null=True, blank=True, help_text='Maximum age. If used, must be 65 or lower.')
    broad_age = models.SmallIntegerField(choices=TARGETING_BROAD_AGE_CHOICES, default=0,
                                         help_text='Whether or not to enable "broad-age-match" targeting. The default is 0 (disabled). Set to 1 to enable broad-age-match targeting.')
    relationship_statuses = models.CommaSeparatedIntegerField(
        null=True, blank=True, max_length=100, help_text='Array of integers for targeting based on relationship status. Use 1 for SINGLE, 2 for IN_RELATIONSHIP, 3 for MARRIED, and 4 for ENGAGED. The default of ALL is used if you specify Null. The default of ALL is also used if you do not specify the field. Do not specify zero.')
    user_event = models.CommaSeparatedIntegerField(
        max_length=100, help_text='Array of integers corresponding to user-relevant events. Currently only supports birthday. To use birthday, pass a one-member array with a value of 1, e.g. "user_event":[1].')

    # Facebook connections
    connections = models.CommaSeparatedIntegerField(
        max_length=100, help_text='An array of Facebook IDs. Connections allows you to target your ads to users who have become a fan of your Page, a member of your Group, RSVP’d to your Event or authorized your Application. The session user has to be an admin of the page, group or event, or developer of the application that is being targeted against. Limit: 50 connections.')
    excluded_connections = fields.JSONField(
        null=True, blank=True, help_text='An array of Facebook IDs. Excluded connections allows you to target your ads to users who have not become fans of your Page, members of your Group, RSVP\'d to your Event or authorized your Application. The session user has to be an admin of the page, group or event, or developer of the application that is being targeted against.')
    friends_of_connections = fields.JSONField(
        null=True, blank=True, help_text='An array of Facebook IDs. "Friends of connections" allows you to target friends of your connections. Connections are fans of your Page, users who have RSVP’d Yes or Maybe to your Event, members of your Group, and users who have interacted with your app. The session user has to be an admin of the page, group or event, or a developer of the application that is being targeted against.')

    # Education and workplace
    college_networks = models.CharField(
        max_length=100, help_text='Colleges, for college graduates. Limit: 200 college networks.')
    work_networks = models.CharField(
        max_length=100, help_text='Company, organization, or other workplace. Limit: 200 work networks.')
    education_statuses = fields.CommaSeparatedCharField(
        max_length=100, help_text='Array of integers for targeting based on education level. Use 1 for HIGH_SCHOOL, 2 for UNDERGRAD, and 3 for ALUM. For one ad group, you can specify only one value. The education_statuses parameter is required if you specify the college_majors parameter.')
    college_years = models.CommaSeparatedIntegerField(
        max_length=100, help_text='Array of integers for graduation year from college.')
    college_majors = fields.CommaSeparatedCharField(
        max_length=100, help_text='Array of strings for specific college majors. Requires that you also specify a value for the education_statuses parameter. Limit: 200 college majors.')

    def parse(self, response):
        super(Targeting, self).parse(response)
        # integerify fields
        for field_name in ['radius']:
            try:
                setattr(self, field_name, int(getattr(self, field_name)))
            except:
                pass


class AdGroup(FacebookGraphModel):

    class Meta:
        verbose_name = 'Facebook ad group'
        verbose_name_plural = 'Facebook ad groups'

    adgroup_id = models.BigIntegerField(help_text='The ID of the ad group', unique=True)
    ad_id = models.BigIntegerField(null=True, help_text='ID of the ad group, required for updating ad groups')
    campaign = models.ForeignKey(
        AdCampaign, related_name='adgroups', help_text='ID of the campaign, required for creating ad groups')
    # in API docs max_length=25, but there is bigger values in the real
    name = models.CharField(
        max_length=100, help_text='The name of the ad group, not longer than 25 characters, required for creating ad groups and can be updated')
    adgroup_status = models.IntegerField(choices=ADGROUP_STATUS_CHOICES, null=True,
                                         help_text='1 indicates ACTIVE, 3 indicates DELETED, 4 indicates PENDING_REVIEW, 5 indicates DISAPPROVED, 8 indicates CAMPAIGN_PAUSED (resuming the Campaign resumes the ad group) and 9 indicates ADGROUP_PAUSED, and if the status is ADGROUP_PAUSED the ad group stays in that state regardless of the campaign being PAUSED or ACTIVE because you would have to resume that ad group specifically')
    bid_type = models.IntegerField(
        choices=BID_TYPE_CHOICES, null=True, help_text='Use 1 for CPC and 2 for CPM; required when creating ad groups;')
    max_bid = models.IntegerField(
        null=True, help_text='The highest bid, defined in cents; required when creating ad groups; can be updated')
    targeting = models.OneToOneField(
        Targeting, null=True, related_name='adgroup', help_text='The ad\'s targeting elements')
    # in API docs `creative` atribute, but `creative_ids` in ther real
    creative = models.ForeignKey(
        AdCreative, null=True, related_name='adgroups', help_text='The ad\'s creative elements')
    start_time = models.DateTimeField(null=True, blank=True, help_text='A unix timestamp for the start time of the ad')
    end_time = models.DateTimeField(null=True, blank=True, help_text='A unix timestamp for the stop time of the ad')
    updated_time = models.DateTimeField(null=True, help_text='A unix timestamp for when the ad was updated')
#    bid_info = models._Field(help_text='The ad\'s bid information') ads_management    array
#    disapprove_reason_descriptions = models._Field(help_text='Reason ad was not approved') ads_management    array

    # not exist in API docs
    ad_status = models.IntegerField(null=True)
    account = models.ForeignKey(AdAccount, related_name='adgroups')

    objects = models.Manager()
    remote = FacebookGraphManager('adgroup_id')

    def __unicode__(self):
        return self.name

    def parse(self, response):
        '''
        Additionally parse `campaign_id`, `account_id`, `creative_ids` fields
        '''
        super(AdGroup, self).parse(response)
        try:
            self.campaign = AdCampaign.objects.get(campaign_id=response['campaign_id'])
        except AdCampaign.DoesNotExist:
            raise Exception('Impossible to save adgroup "%s" (%d) for unexisted campaign %s' %
                            (self.name, self.adgroup_id, response['campaign_id']))

        try:
            self.account = AdAccount.objects.get(account_id=response['account_id'])
        except AdAccount.DoesNotExist:
            raise Exception('Impossible to save adgroup "%s" (%d) for unexisted account %s' %
                            (self.name, self.adgroup_id, response['account_id']))

        creative_id = response['creative_ids'][0]
        if creative_id:
            try:
                self.creative = AdCreative.objects.get(creative_id=creative_id)
            except AdCreative.DoesNotExist:
                self.creative = AdCreative(creative_id=creative_id)

        # integerify fields
        for field_name in ['max_bid']:
            try:
                setattr(self, field_name, int(getattr(self, field_name)))
            except:
                pass

    def save(self, *args, **kwargs):
        '''
        Create targeting and creative before saving AdGroup
        '''
        try:
            # because of strange error while saving adgroup.save() - IntegrityError:
            # null value in column "targeting_id" violates not-null constraint
            if not self.targeting_id and self.targeting:
                self.targeting.save()
                self.targeting_id = self.targeting.id
        except Targeting.DoesNotExist:
            pass

        try:
            # because of strange error while saving adgroup.save() - IntegrityError:
            # null value in column "creative_id" violates not-null constraint
            if not self.creative_id and self.creative:
                self.creative.save()
                self.creative_id = self.creative.id
        except AdCreative.DoesNotExist:
            pass

        super(AdGroup, self).save(*args, **kwargs)

    def fetch_stats(self):
        '''
        Retrieve and save statistic for group
        '''
        response = api_call('%s/stats' % self.adgroup_id)
        instance = AdStatistic.remote.get_or_create_from_resource(response)
        return instance


class StatisticManager(models.Manager):

    def import_from_csv(self, csv_file, account_id):

        data_file = csv.DictReader(csv_file)

        fields_map = {
            'Date Range': None,  # '02/11/2012-02/18/2012'

            'Ad ID': None,
            'Ad Name': None,
            'Campaign': None,
            'Campaign ID': None,

            'Impressions': 'impressions',
            'Clicks': 'clicks',
            'Connections': 'connections',
            'Spent': 'spent',
            'Social Clicks': 'social_clicks',
            'Social Impressions': 'social_impressions',
            'Social Reach': 'social_reach',
            'Social %': 'social',
            'Social CTR': 'social_ctr',
            'CPC': 'cpc',
            'CTR': 'ctr',
            'CPM': 'cpm',
            'Reach': 'reach',
            'Frequency': 'frequency',
            'Unique Clicks': 'unique_clicks',
            'Unique CTR': 'unique_ctr',

            'Actions': 'actions',
            'Page Likes': 'page_likes',
            'App Installs': 'app_installs',
            'Event Responses': 'event_responses',
        }

        stats = []
        for row in data_file:
#            print row
            # {'Social Impressions': '421', 'Ad ID': '6003513604333', 'CTR': '0.482%', 'Campaign': 'Paulig', 'Social Reach': '257', 'Campaign ID': '6003513603333', 'CPC': '5.42', 'Spent': '32.53', 'Social Clicks': '0', 'Connections': '3', 'Date Range': '02/11/2012-02/18/2012', 'Ad Name': '\xd0\x9f\xd0\xb0\xd1\x88\xd0\xb0. \xd0\x9a\xd0\xbe\xd1\x84\xd0\xb5\xd0\xb9\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xb7\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x81\xd0\xb8\xd0\xbc\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c \xd0\xb2\xd0\xb4\xd0\xbe\xd1\x85\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbb\xd1\x8f\xd0\xb5\xd1\x82', 'Social %': '33.84%', 'Social CTR': '0.000%', 'Impressions': '1244', 'Clicks': '6', 'CPM': '26.15'}
            stat = AdStatistic()

            # get or create campaigns and adgroups for statistic
            account = AdAccount.objects.get(account_id=account_id)
            campaign = None
            adgroup = None
            if 'Campaign ID' in row:
                campaign, created = AdCampaign.objects.get_or_create(
                    campaign_id=row['Campaign ID'], defaults={'account': account, 'name': row['Campaign']})
                if not created:
                    campaign.name = row['Campaign']
                    campaign.save()
            if 'Ad ID' in row:
                adgroup, created = AdGroup.objects.get_or_create(
                    adgroup_id=row['Ad ID'], defaults={'campaign': campaign, 'account': account, 'name': row['Ad Name']})
                if not created:
                    adgroup.name = row['Ad Name']
                    adgroup.save()

            if adgroup:
                stat.adgroup = adgroup
            elif campaign:
                stat.campaign = campaign
            else:
                stat.account = account

            if 'Date Range' in row:
                start, end = row['Date Range'].split('-')
                stat.start_time = parser.parse(start)
                stat.end_time = parser.parse(end)
            elif 'Date' in row:
                if 'Week of' in row['Date']:
                    stat.start_time = parser.parse(row['Date'][8:])
                    stat.end_time = stat.start_time + timedelta(days=7)
                elif len(row['Date']) == 8 and row['Date'][3:4] == ' ':
                    month = parser.parse(row['Date'])
                    stat.start_time = datetime(month.year, month.month, 1, 0, 0)
                    stat.end_time = stat.start_time + relativedelta.relativedelta(months=1)
                else:
                    stat.start_time = parser.parse(row['Date'])
                    stat.end_time = stat.start_time + timedelta(days=1)
            else:
                raise CSVFormatError(
                    "Are you sure language of export file is English? Could not find start_time/end_time fields in csv row: %s" % row)

            # don't add stat if it before or after campaign or adgroup time limits
            object_limit = None
            if stat.adgroup:
                object_limit = stat.adgroup
            elif stat.campaign:
                object_limit = stat.campaign

            # check if date ranges of stat and life of object_limit is intersects. if not => continue
            if object_limit and \
                (object_limit.start_time and object_limit.end_time and stat.start_time and stat.end_time
                    and not ((object_limit.start_time <= stat.start_time <= object_limit.end_time)
                             or (stat.start_time <= object_limit.start_time <= stat.end_time)) or
                 (object_limit.start_time and not object_limit.end_time and stat.end_time
                    and stat.end_time < object_limit.start_time)):
                continue
#            else:
#                print object_limit.start_time, object_limit.end_time
#                print stat.start_time, stat.end_time

            # set stat.start_time == None if it less then start_time of adgroup of adcampaign
            if stat.adgroup and stat.adgroup.start_time and stat.start_time <= stat.adgroup.start_time or \
                    stat.campaign and stat.campaign.start_time and stat.start_time <= stat.campaign.start_time:
                stat.start_time = None

            for key, field in fields_map.items():

                try:
                    value = row[key]
                    assert value and field
                except (KeyError, AssertionError):
                    continue

                if isinstance(stat._meta.get_field(field), models.IntegerField):
                    try:
                        setattr(stat, field, int(value))
                    except ValueError:
                        raise CSVFormatError("Wrong value %s for integer field '%s'" % (row[key], field))
                elif isinstance(stat._meta.get_field(field), models.FloatField):
                    try:
                        setattr(stat, field, float(value.replace('%', '')))
                    except ValueError:
                        raise CSVFormatError("Wrong value %s for float field '%s'" % (row[key], field))
                else:
                    setattr(stat, field, value)

            stat.set_statistic_id()
            AdStatistic.remote.get_or_create_from_instance(stat)
            stats += [stat]

        return stats


class AdStatistic(FacebookGraphModel):

    class Meta:
        verbose_name = 'Facebook ad statistic report'
        verbose_name_plural = 'Facebook ad statistic reports'

    statistic_id = models.CharField(max_length="100", unique=True, help_text='The statistic ID')

    account = models.ForeignKey(AdAccount, null=True, related_name='adstatistics',
                                help_text='The ID of the object the statistics refer to, this may also be adcampaign_id or adgroup_id')
    campaign = models.ForeignKey(AdCampaign, null=True, related_name='adstatistics',
                                 help_text='The ID of the object the statistics refer to, this may also be adcampaign_id or adgroup_id')
    adgroup = models.ForeignKey(AdGroup, null=True, related_name='adstatistics',
                                help_text='The ID of the object the statistics refer to, this may also be adcampaign_id or adgroup_id')

    start_time = models.DateTimeField(
        null=True, blank=True, help_text='A unix timestamp of the stats of the statistics period')
    end_time = models.DateTimeField(
        null=True, blank=True, help_text='A unix timestamp of the stats of the statistics period')

    impressions = models.IntegerField(
        null=True, help_text='The total number of times your adverts have been shown on the site.')
    clicks = models.IntegerField(
        null=True, help_text='The number of clicks the Sponsored Story or advert has received. If you\'re promoting a Page, event or application, clicks will also include Page likes, event RSVPs or installation of applications directly from the Sponsored Story or advert.')
    # integer in API docs but float here, because of csv reports
    spent = models.FloatField(null=True, help_text='The amount spent during the selected time period.')
    social_impressions = models.IntegerField(null=True, help_text='Impressions that were shown social context.')
    social_clicks = models.IntegerField(null=True, help_text='Clicks on adverts that were shown with social context.')
    social_spent = models.IntegerField(
        null=True, help_text='The amount spent during the selected time period on ads with social context.')
    actions = models.IntegerField(null=True, help_text='The number of action performed on this ad')
    unique_impressions = models.IntegerField(
        null=True, help_text='The number of individuals this ad was shown to on the site')
    unique_clicks = models.IntegerField(null=True, help_text='The number of individuals who clicked this ad.')
    social_unique_impressions = models.IntegerField(
        null=True, help_text='The number of individuals this ad was shown to with social context')
    social_unique_clicks = models.IntegerField(
        null=True, help_text='The number of individuals who clicked this ad while it had social context')
    connections = models.IntegerField(
        null=True, help_text='The number of events (likes, RSVPs, app installs, joins to a group) attributed to an ad or campaign within 24 hours of the user viewing or clicking an ad. The Connections stat is incremented by one of the following: For a given 24-hour period, if no click has occurred but an impression has occurred, the ad with the latest impression has the Connection stat incremented by one. For a given 24-hour period, if a click has occurred, the ad with the latest click has the Connection stat incremented by one.')

    # only in csv reports
    social_reach = models.IntegerField(
        null=True, help_text='How many people saw your ad or Sponsored Story with the names of their friends who had already liked your Page, RSVPed to your event, or used your app.')
    # TODO: ensure this is the same field that in API before, otherwise rename it
    # actions = models.IntegerField(null=True, help_text='This data includes all actions taken by people within 24 hours after viewing an ad or Sponsored Story, or within 28 days after clicking on it. You\'ll only see data here if you\'re promoting a Page, event or app.')
    page_likes = models.IntegerField(
        null=True, help_text='The number of people who like your Page within 24 hours of viewing an ad or sponsored story, or within 28 days after clicking on it.')
    app_installs = models.IntegerField(null=True, help_text='')
    event_responses = models.IntegerField(null=True, help_text='')

    # fields from week reports
    reach = models.IntegerField(null=True, help_text='')
    frequency = models.FloatField(null=True, help_text='')

    # auto-estimated values
    ctr = models.FloatField(
        help_text='Click-through rate, or the number of clicks your Sponsored Story or ad received divided by the number of times it was shown on the site.')
    social = models.FloatField(
        help_text='The percentage of impressions where your ad was shown with the names of viewers\' friends who liked your Page, RSVPed to your event, or used your app.')
    social_ctr = models.FloatField(
        help_text='The number of social clicks received divided by the number of social impressions.')
    cpc = models.FloatField(
        help_text='The average cost per click for these ads, calculated as the amount spent divided by the number of clicks received.')
    cpm = models.FloatField(
        help_text='The average cost per thousand impressions on these ads, calculated as the amount spent divided by the the number of impressions received.')
    unique_ctr = models.FloatField(
        help_text='The unique click through rate. The unique CTR is calculated as the number of unique clicks the ad(s) received divided by the number of unique ad impressions.')

    objects = StatisticManager()
    remote = FacebookGraphManager('statistic_id')

    def parse(self, response):
        '''
        Additionally parse `id`, `account_id`, `campaign_id`, `adgroup_id` fields
        '''
        super(AdStatistic, self).parse(response)

        self.statistic_id = response['id']
        try:
            self.campaign = AdCampaign.objects.get(campaign_id=response['campaign_id'])
        except AdCampaign.DoesNotExist:
            raise Exception('Impossible to save statistic "%s" for unexisted campaign %s' %
                            (self.statistic_id, response['campaign_id']))
        except KeyError:
            pass
        try:
            self.adgroup = AdGroup.objects.get(adgroup_id=response['adgroup_id'])
        except AdGroup.DoesNotExist:
            raise Exception('Impossible to save statistic "%s" for unexisted adgroup %s' %
                            (self.statistic_id, response['adgroup_id']))
        except KeyError:
            pass
        try:
            self.account = AdAccount.objects.get(account_id=response['account_id'])
        except AdAccount.DoesNotExist:
            raise Exception('Impossible to save statistic "%s" for unexisted account %s' %
                            (self.statistic_id, response['account_id']))
        except KeyError:
            pass

    def set_statistic_id(self):
        if not self.statistic_id:

            if self.account:
                ids = ["act_%d" % self.account.account_id]
            if self.campaign:
                ids = [self.campaign.campaign_id]
            if self.adgroup:
                ids = [self.adgroup.adgroup_id]

            ids += ['stats']
            # TODO: make sure that if self.start_time is None value must be 0
            if self.start_time:
                ids += [int(time.mktime(self.start_time.timetuple()))]
            else:
                ids += [0]
            ids += [int(time.mktime(self.end_time.timetuple()))]

            self.statistic_id = '/'.join([str(id) for id in ids])

    def set_auto_values(self):
        # estimate auto values
        if not self.ctr:
            self.ctr = float('%.3f' % (100 * float(self.clicks) / self.impressions) if self.impressions else 0)
        if not self.unique_ctr:
            self.unique_ctr = float(
                '%.3f' % (100 * float(self.unique_clicks) / self.unique_impressions) if self.unique_impressions else 0)
        if not self.social_ctr:
            self.social_ctr = float(
                '%.3f' % (100 * float(self.social_clicks) / self.social_impressions) if self.social_impressions else 0)
        if not self.social:
            self.social = float(
                '%.2f' % (100 * float(self.social_impressions) / self.impressions) if self.impressions else 0)
        if not self.cpc:
            self.cpc = float('%.2f' % (self.spent / self.clicks) if self.clicks else 0)
        if not self.cpm:
            self.cpm = float('%.2f' % (1000 * self.spent / self.impressions) if self.impressions else 0)

    def save(self, *args, **kwargs):
        self.set_auto_values()
        self.set_statistic_id()
        return super(AdStatistic, self).save(*args, **kwargs)


class AdImage(FacebookGraphModel):

    class Meta:
        verbose_name = 'Facebook ad image'
        verbose_name_plural = 'Facebook ad images'

    hash = models.CharField(max_length="32", unique=True, help_text='The hash which uniquely identifies the image.')
    url = models.URLField(
        max_length="100", unique=True, help_text='A temporary URL which the image can be retrieved at.')

    remote = FacebookGraphManager('hash')
