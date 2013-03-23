# -*- coding: utf-8 -*-
from django.test import TestCase
from models import AdAccount, AdCampaign, AdCreative, AdGroup, AdStatistic, Targeting, AdImage
from datetime import datetime
from StringIO import StringIO
import simplejson as json

ACCOUNT_ID = 213548191
CAMPAIGN_ID = 6003399667133

class FacebookAdsTest(TestCase):

    def test_fetch_creatives_for_account(self):

        self.assertEqual(AdCreative.objects.count(), 0)
        account = AdAccount.objects.create(account_id=ACCOUNT_ID)

        instances = account.fetch_creatives()
        self.assertTrue(AdCreative.objects.count() > 0)
        self.assertEqual(AdCreative.objects.count(), len(instances))

        account.fetch_creatives()
        self.assertEqual(AdCreative.objects.count(), len(instances))

    def test_fetch_campaigns_for_account(self):

        self.assertEqual(AdCampaign.objects.count(), 0)
        account = AdAccount.objects.create(account_id=ACCOUNT_ID)

        instances = account.fetch_campaigns()
        self.assertTrue(AdCampaign.objects.count() > 0)
        self.assertEqual(AdCampaign.objects.count(), len(instances))

        account.fetch_campaigns()
        self.assertEqual(AdCampaign.objects.count(), len(instances))

    def test_fetch_groups_for_campaign(self):

        self.assertEqual(AdGroup.objects.count(), 0)
        account = AdAccount.objects.create(account_id=ACCOUNT_ID)
        campaign = AdCampaign.objects.create(campaign_id=CAMPAIGN_ID, account=account)

        instances = campaign.fetch_groups()
        self.assertTrue(AdGroup.objects.count() > 0)
        self.assertEqual(AdGroup.objects.count(), len(instances))
        self.assertEqual(Targeting.objects.count(), len(instances))

        campaign.fetch_groups()
        self.assertEqual(AdGroup.objects.count(), len(instances))
        self.assertEqual(Targeting.objects.count(), len(instances)) # TODO: Not Critical. Fix it!

    def test_fetch_stats_for_account(self):

        self.assertEqual(AdStatistic.objects.count(), 0)
        account = AdAccount.objects.create(account_id=ACCOUNT_ID)

        instance = account.fetch_stats()
        self.assertTrue(AdStatistic.objects.count() == 1)
        self.assertTrue(isinstance(instance, AdStatistic))

        account.fetch_stats()
        self.assertEqual(AdStatistic.objects.count(), 2)

    def test_fetch_stats_for_campaign(self):

        self.assertEqual(AdStatistic.objects.count(), 0)
        account = AdAccount.objects.create(account_id=ACCOUNT_ID)
        campaign = AdCampaign.objects.create(campaign_id=CAMPAIGN_ID, account=account)
        campaign.fetch_groups()
        group = AdGroup.objects.all()[0]

        instance = group.fetch_stats()
        self.assertTrue(AdStatistic.objects.count() == 1)
        self.assertTrue(isinstance(instance, AdStatistic))

        group.fetch_stats()
        self.assertEqual(AdStatistic.objects.count(), 2)

    def test_fetch_stats_for_group(self):

        self.assertEqual(AdStatistic.objects.count(), 0)
        account = AdAccount.objects.create(account_id=ACCOUNT_ID)
        campaign = AdCampaign.objects.create(campaign_id=CAMPAIGN_ID, account=account)

        instance = campaign.fetch_stats()
        self.assertTrue(AdStatistic.objects.count() == 1)
        self.assertTrue(isinstance(instance, AdStatistic))

        campaign.fetch_stats()
        self.assertEqual(AdStatistic.objects.count(), 2)

    def test_fetch_stats_campaigns_for_account(self):

        self.assertEqual(AdStatistic.objects.count(), 0)
        account = AdAccount.objects.create(account_id=ACCOUNT_ID)

        account.fetch_campaigns()
        instances = account.fetch_stats_campaigns()
        self.assertTrue(AdStatistic.objects.count() > 0)
        self.assertEqual(AdStatistic.objects.count(), len(instances))
        self.assertEqual(AdStatistic.objects.count(), AdCampaign.objects.count())

        account.fetch_stats_campaigns()
        self.assertEqual(AdStatistic.objects.count(), len(instances)*2)

    def test_fetch_stats_groups_for_account(self):

        self.assertEqual(AdStatistic.objects.count(), 0)
        account = AdAccount.objects.create(account_id=ACCOUNT_ID)

        account.fetch_campaigns()
        account.fetch_groups()
        instances = account.fetch_stats_groups() # TODO: fix it - Exception: Impossible to save statistic ... for unexisted adgroup ...
        self.assertTrue(AdStatistic.objects.count() > 0)
        self.assertEqual(AdStatistic.objects.count(), len(instances))
        self.assertEqual(AdStatistic.objects.count(), AdGroup.objects.count())

        account.fetch_stats_groups()
        self.assertEqual(AdStatistic.objects.count(), len(instances)*2)


    def test_fetch_account(self):

        self.assertEqual(AdAccount.objects.count(), 0)
        AdAccount.remote.fetch(ACCOUNT_ID)
        self.assertEqual(AdAccount.objects.count(), 1)
        AdAccount.remote.fetch(ACCOUNT_ID)
        self.assertEqual(AdAccount.objects.count(), 1)

    def test_fetch_account_images(self):

        account = AdAccount.objects.create(account_id=ACCOUNT_ID)

        self.assertEqual(AdImage.objects.count(), 0)
        account.fetch_images()
        self.assertTrue(AdImage.objects.count() > 0)

    def test_parse_account(self):

        response = '''
            {
              "id": "act_213548191",
              "account_id": 213548191,
              "name": "Имя",
              "account_status": 1,
              "currency": "RUB",
              "timezone_id": 115,
              "timezone_name": "Europe/Kaliningrad",
              "is_personal": 0,
              "business_name": "",
              "business_street": "Онежская, 17, 74",
              "business_street2": "",
              "business_city": "Москва",
              "business_state": "",
              "business_zip": "125438",
              "business_country_code": "RU",
              "vat_status": 2,
              "daily_spend_limit": 6100000,
              "users": [
                    {
                      "uid": 508397176,
                      "permissions": [
                        2,
                        3,
                        4,
                        7
                      ],
                      "role": 1002
                    },
                    {
                      "uid": 576628256,
                      "permissions": [
                        2,
                        3,
                        4,
                        7
                      ],
                      "role": 1002
                    }
               ]
            }
            '''
        account = AdAccount()
        account.parse(json.loads(response))
        account.save()

        self.assertEqual(account.account_id, 213548191)
        self.assertEqual(account.name, u"Имя")
        self.assertEqual(account.account_status, 1)
        self.assertEqual(account.currency, "RUB")
        self.assertEqual(account.timezone_id, 115)
        self.assertEqual(account.timezone_name, "Europe/Kaliningrad")
        self.assertEqual(account.is_personal, 0)
        self.assertEqual(account.business_name, "")
        self.assertEqual(account.business_street, u"Онежская, 17, 74")
        self.assertEqual(account.business_street2, "")
        self.assertEqual(account.business_city, u"Москва")
        self.assertEqual(account.business_state, "")
        self.assertEqual(account.business_zip, "125438")
        self.assertEqual(account.business_country_code, "RU")
        self.assertEqual(account.vat_status, 2)
        self.assertEqual(account.daily_spend_limit, 6100000)

        self.assertEqual(account.users.count(), 2)
        user = account.users.get(uid=508397176)
        self.assertEqual(user.role, 1002)
        self.assertEqual(user.permissions, '2,3,4,7')

    def test_parse_campaign(self):

        response = '''
            {
              "account_id": 213548191,
              "campaign_id": 6003513277933,
              "name": "American Eagle",
              "daily_budget": 150000,
              "campaign_status": 1,
              "daily_imps": 0,
              "id": "6003513277933",
              "start_time": "2011-11-04T14:09:42+0000",
              "end_time": null,
              "updated_time": "2011-12-10T14:11:18+0000"
            }
            '''
        AdAccount.objects.create(account_id=213548191)
        campaign = AdCampaign()
        campaign.parse(json.loads(response))
        campaign.save()

        self.assertEqual(campaign.account.account_id, 213548191)
        self.assertEqual(campaign.campaign_id, 6003513277933)
        self.assertEqual(campaign.name, "American Eagle")
        self.assertEqual(campaign.daily_budget, 150000)
        self.assertEqual(campaign.campaign_status, 1)
        self.assertEqual(campaign.daily_imps, 0)
        self.assertEqual(campaign.start_time, datetime(2011,11,4,14,9,42))
        self.assertEqual(campaign.end_time, None)
        self.assertEqual(campaign.updated_time, datetime(2011,12,10,14,11,18))

    def test_parse_creative(self):

        response = '''
            {
              "view_tag": "",
              "alt_view_tags": [
              ],
              "creative_id": 6003589918533,
              "type": 1,
              "title": "Моя Москва.",
              "body": "Помоги своему городу стать лучше. Это  в твоих силах. ",
              "image_hash": "ecb930e27b60eeba288cb56ff769ea16",
              "link_url": "http://gorod.mos.ru/statistics/",
              "name": "Моя Москва.",
              "run_status": 1,
              "preview_url": "http://www.facebook.com/ads/api/creative_preview.php?cid=6003589918533",
              "count_current_adgroups": 1,
              "id": "6003589918533",
              "image_url": "http://creative.ak.fbcdn.net/v41818/flyers/86/1/1323382428794231472_1_0357d622.jpg"
            }
            '''
        creative = AdCreative()
        creative.parse(json.loads(response))
        creative.save()

        self.assertEqual(creative.view_tag, "")
        self.assertEqual(creative.creative_id, 6003589918533)
        self.assertEqual(creative.type, 1)
        self.assertEqual(creative.title, u"Моя Москва.")
        self.assertEqual(creative.body, u"Помоги своему городу стать лучше. Это  в твоих силах. ")
        self.assertEqual(creative.image_hash, "ecb930e27b60eeba288cb56ff769ea16")
        self.assertEqual(creative.link_url, "http://gorod.mos.ru/statistics/")
        self.assertEqual(creative.name, u"Моя Москва.")
        self.assertEqual(creative.run_status, 1)
        self.assertEqual(creative.preview_url, "http://www.facebook.com/ads/api/creative_preview.php?cid=6003589918533")
        self.assertEqual(creative.count_current_adgroups, 1)
        self.assertEqual(creative.image_url, "http://creative.ak.fbcdn.net/v41818/flyers/86/1/1323382428794231472_1_0357d622.jpg")

        response = '''
            {
              "story_id": "234311559969833",
              "type": "27",
              "object_id": "126910150718226",
              "name": "Page Post Ad #6003548863533",
              "run_status": 1,
              "preview_url": "http://www.facebook.com/ads/api/creative_preview.php?cid=6003548863533",
              "count_current_adgroups": 1,
              "id": "6003548863533"
            }
            '''
        creative = AdCreative()
        creative.parse(json.loads(response))
        creative.save()

        self.assertEqual(creative.creative_id, 6003548863533)
        self.assertEqual(creative.story_id, 234311559969833)
        self.assertEqual(creative.type, 27)
        self.assertEqual(creative.object_id, 126910150718226)
        self.assertEqual(creative.name, "Page Post Ad #6003548863533")
        self.assertEqual(creative.run_status, 1)
        self.assertEqual(creative.preview_url, "http://www.facebook.com/ads/api/creative_preview.php?cid=6003548863533")
        self.assertEqual(creative.count_current_adgroups, 1)

    def test_parse_adgroup(self):

        response = '''
            {
              "adgroup_id": 6003589918933,
              "ad_id": 6003589918933,
              "campaign_id": 6003578734133,
              "name": "Вика. Помоги Москве стать лучше.",
              "ad_status": 1,
              "adgroup_status": 1,
              "bid_type": 1,
              "max_bid": "1500",
              "bid_info": {
                "1": "1500"
              },
              "account_id": 213548191,
              "id": "6003589918933",
              "creative_ids": [
                6003589918533
              ],
              "targeting": {
                "genders": [
                  1
                ],
                "age_max": 65,
                "age_min": 18,
                "radius": "10",
                "cities": [
                  {
                    "id": "2020916",
                    "name": "Moscow"
                  },
                  {
                    "id": "2680078",
                    "name": "Zelenograd"
                  }
                ],
                "user_adclusters": [
                  {
                    "id": "6002714398372",
                    "name": "Parents (All)"
                  },
                  {
                    "id": "6002714884172",
                    "name": "Autos"
                  }
                ],
                "excluded_connections": [
                  {
                    "id": "249850718379421",
                    "name": "Suzuki Russia"
                  }
                ],
                "countries": [
                  "RU",
                  "US"
                ],
                "broad_age": 1
              },
              "start_time": null,
              "end_time": "2011-12-13T15:58:00+0000",
              "updated_time": "2011-12-12T07:05:51+0000"
            }
            '''
        account = AdAccount.objects.create(account_id=213548191)
        AdCampaign.objects.create(campaign_id=6003578734133, account=account)
        group = AdGroup()
        group.parse(json.loads(response))
        group.save()

        self.assertEqual(group.adgroup_id, 6003589918933)
        self.assertEqual(group.ad_id, 6003589918933)
        self.assertEqual(group.campaign.campaign_id, 6003578734133)
        self.assertEqual(group.name, u"Вика. Помоги Москве стать лучше.")
        self.assertEqual(group.ad_status, 1)
        self.assertEqual(group.adgroup_status, 1)
        self.assertEqual(group.bid_type, 1)
        self.assertEqual(group.max_bid, 1500)
        self.assertEqual(group.account.account_id, 213548191)

        # creative
        self.assertTrue(isinstance(group.creative, AdCreative))
        self.assertEqual(group.creative.creative_id, 6003589918533)

        # targeting
        self.assertTrue(isinstance(group.targeting, Targeting))
        self.assertEqual(group.targeting.age_max, 65)
        self.assertEqual(group.targeting.age_min, 18)
        self.assertEqual(group.targeting.radius, 10)
        self.assertEqual(group.targeting.countries, "RU,US")
        self.assertEqual(group.targeting.genders, "1")
        self.assertEqual(group.targeting.broad_age, 1)
        self.assertEqual(group.targeting.cities, [{'id': '2020916', 'name': 'Moscow'}, {'id': '2680078', 'name': 'Zelenograd'}])
        self.assertEqual(group.targeting.user_adclusters, [{'id': '6002714398372', 'name': 'Parents (All)'}, {'id': '6002714884172', 'name': 'Autos'}])
        self.assertEqual(group.targeting.excluded_connections, [{'id': '249850718379421','name': 'Suzuki Russia'}])

    def test_parse_statistic(self):

        response = '''
            {
              "id": "act_213548191/stats/0/1323785538",
              "account_id": 213548191,
              "start_time": null,
              "end_time": "2011-12-13T14:12:18+0000",
              "impressions": 35666467,
              "clicks": 33356,
              "spent": 41315559,
              "social_impressions": 6177154,
              "social_clicks": 5838,
              "social_spent": 7084534,
              "actions": 8623,
              "unique_impressions": 0,
              "unique_clicks": 0,
              "social_unique_impressions": 0,
              "social_unique_clicks": 0,
              "connections": 11185
            }
            '''
        AdAccount.objects.create(account_id=213548191)
        stat = AdStatistic()
        stat.parse(json.loads(response))
        stat.save()

        self.assertEqual(stat.statistic_id, "act_213548191/stats/0/1323785538")
        self.assertEqual(stat.account.account_id, 213548191)
        self.assertEqual(stat.start_time, None)
        self.assertEqual(stat.end_time, datetime(2011,12,13,14,12,18))
        self.assertEqual(stat.impressions, 35666467)
        self.assertEqual(stat.clicks, 33356)
        self.assertEqual(stat.spent, 41315559)
        self.assertEqual(stat.social_impressions, 6177154)
        self.assertEqual(stat.social_clicks, 5838)
        self.assertEqual(stat.social_spent, 7084534)
        self.assertEqual(stat.actions, 8623)
        self.assertEqual(stat.unique_impressions, 0)
        self.assertEqual(stat.unique_clicks, 0)
        self.assertEqual(stat.social_unique_impressions, 0)
        self.assertEqual(stat.social_unique_clicks, 0)
        self.assertEqual(stat.connections, 11185)

    def test_parse_image(self):

        response = '''
            {
              "data": {
                "f15c502c413f98e4f9b9f8efe24409f7": {
                  "hash": "f15c502c413f98e4f9b9f8efe24409f7",
                  "url": "http://creative.ak.fbcdn.net/v41818/flyers/105/61/1325238022303564436_1_aa8550c0.jpg"
                }
              }
            }
            '''
        stat = AdImage()
        stat.parse(json.loads(response)['data']['f15c502c413f98e4f9b9f8efe24409f7'])
        stat.save()

        self.assertEqual(stat.hash, "f15c502c413f98e4f9b9f8efe24409f7")
        self.assertEqual(stat.url, "http://creative.ak.fbcdn.net/v41818/flyers/105/61/1325238022303564436_1_aa8550c0.jpg")

    def test_calculate_statistic_auto_values(self):

        stat = AdStatistic.objects.create(impressions=87514, social_impressions=2362, social_clicks=1, clicks=34, spent=190.77, connections=8)
        stat.save()

        self.assertEqual(stat.ctr, 0.039)
        self.assertEqual(stat.social, 2.70)
        self.assertEqual(stat.social_ctr, 0.042)
        self.assertEqual(stat.cpc, 5.61)
        self.assertEqual(stat.cpm, 2.18)

    def test_parse_statistic_csv(self):

        scv_file = '''"Date Range",Campaign,"Campaign ID","Ad Name","Ad ID",Impressions,"Social Impressions","Social %",Clicks,"Social Clicks",CTR,"Social CTR",CPC,CPM,Spent,"Social Reach",Connections
02/11/2012-02/18/2012,Paulig,6003513603333,"Паша. Кофейная зависимость вдохновляет",6003513604333,1244,421,33.84%,6,0,0.482%,0.000%,5.42,26.15,32.53,257,3
02/11/2012-02/18/2012,Paulig,6003513603333,"Паша. Кофе может стать (осторожно)",6003523381133,27435,548,2.00%,24,0,0.087%,0.000%,4.73,4.14,113.56,249,6
02/11/2012-02/18/2012,Paulig,6003513603333,"Паша. Кофе может стать (доказано)",6003523384333,108390,21714,20.03%,140,0,0.129%,0.000%,8.28,10.69,1158.64,5390,79'''

        account = AdAccount.objects.create(account_id=ACCOUNT_ID)
        campaign = AdCampaign.objects.create(campaign_id=6003513603333, account=account)
        adgroup = AdGroup.objects.create(adgroup_id=6003513604333, campaign=campaign, account=account)

        stats = AdStatistic.objects.import_from_csv(StringIO(scv_file), ACCOUNT_ID)
        self.assertEqual(stats[0].account, account)
        self.assertEqual(stats[0].campaign, campaign)
        self.assertEqual(stats[0].adgroup, adgroup)

        self.assertEqual(stats[0].start_time, datetime(2012,2,11,0,0))
        self.assertEqual(stats[0].end_time, datetime(2012,2,18,0,0))

        self.assertEqual(stats[0].impressions, 1244)
        self.assertEqual(stats[0].social_impressions, 421)
        self.assertEqual(stats[0].social_clicks, 0)
        self.assertEqual(stats[0].clicks, 6)
        self.assertEqual(stats[0].social_clicks, 0)
        self.assertEqual(stats[0].ctr, 0.482)
        self.assertEqual(stats[0].social_ctr, 0.000)
        self.assertEqual(stats[0].cpc, 5.42)
        self.assertEqual(stats[0].cpm, 26.15)
        self.assertEqual(stats[0].spent, 32.53)
        self.assertEqual(stats[0].social_reach, 257)
        self.assertEqual(stats[0].connections, 3)

        self.assertEqual(stats[1].account, account)
        self.assertEqual(stats[1].campaign, campaign)
        self.assertNotEqual(stats[1].adgroup, adgroup)
        self.assertEqual(stats[1].adgroup.name, 'Паша. Кофе может стать (осторожно)')

        scv_file = '''Date,Campaign,"Campaign ID","Ad Name","Ad ID",Impressions,"Social Impressions","Social %",Clicks,"Social Clicks",CTR,"Social CTR",CPC,CPM,Spent,Reach,Frequency,"Social Reach",Connections,"Unique Clicks","Unique CTR"
"Week of 01/22/2012",Paulig,6003513603333,"Паша. Кофейная зависимость вдохновляет",6003513604333,7649,6870,89.82%,5,5,0.065%,0.073%,14.34,9.37,71.68,1749,4.4,1615,2,5,0.286%
"Week of 01/22/2012",Quelle,6003446974133,"Размер имеет значение",6003516792133,90762,2959,3.26%,37,0,0.041%,0.000%,7.42,3.02,274.41,17348,5.2,391,6,37,0.213%'''

        stats = AdStatistic.objects.import_from_csv(StringIO(scv_file), ACCOUNT_ID)
        self.assertEqual(stats[0].account, account)
        self.assertEqual(stats[0].campaign, campaign)
        self.assertEqual(stats[0].adgroup, adgroup)

        self.assertEqual(stats[0].start_time, datetime(2012,1,22,0,0))
        self.assertEqual(stats[0].end_time, datetime(2012,1,29,0,0))

        self.assertEqual(stats[0].impressions, 7649)
        self.assertEqual(stats[0].social_impressions, 6870)
        self.assertEqual(stats[0].social, 89.82)
        self.assertEqual(stats[0].clicks, 5)
        self.assertEqual(stats[0].social_clicks, 5)
        self.assertEqual(stats[0].ctr, 0.065)
        self.assertEqual(stats[0].social_ctr, 0.073)
        self.assertEqual(stats[0].cpc, 14.34)
        self.assertEqual(stats[0].cpm, 9.37)
        self.assertEqual(stats[0].spent, 71.68)
        self.assertEqual(stats[0].reach, 1749)
        self.assertEqual(stats[0].frequency, 4.4)
        self.assertEqual(stats[0].social_reach, 1615)
        self.assertEqual(stats[0].connections, 2)
        self.assertEqual(stats[0].unique_clicks, 5)
        self.assertEqual(stats[0].unique_ctr, 0.286)

        self.assertEqual(stats[1].account, account)
        self.assertNotEqual(stats[1].campaign, campaign)
        self.assertNotEqual(stats[1].adgroup, adgroup)
        self.assertEqual(stats[1].campaign.name, 'Quelle')
        self.assertEqual(stats[1].adgroup.name, 'Размер имеет значение')

        scv_file = '''Date,Campaign,"Campaign ID","Ad Name","Ad ID",Impressions,"Social Impressions","Social %",Clicks,"Social Clicks",CTR,"Social CTR",CPC,CPM,Spent,Reach,Frequency,"Social Reach",Connections,"Unique Clicks","Unique CTR"
02/13/2012,Paulig,6003513603333,"Паша. Кофейная зависимость вдохновляет",6003513604333,960,320,33.33%,4,0,0.417%,0.000%,4.96,20.68,19.85,656,1.5,200,2,3,0.457%'''

        stats = AdStatistic.objects.import_from_csv(StringIO(scv_file), ACCOUNT_ID)

        self.assertEqual(stats[0].start_time, datetime(2012,2,13,0,0))
        self.assertEqual(stats[0].end_time, datetime(2012,2,14,0,0))

        scv_file = '''Date,Campaign,"Campaign ID","Ad Name","Ad ID",Impressions,"Social Impressions","Social %",Clicks,"Social Clicks",CTR,"Social CTR",CPC,CPM,Spent,Reach,Frequency,"Social Reach",Connections,"Unique Clicks","Unique CTR"
"Dec 2011",SX4,6003399254533,"городская философия",6003400321533,1672,709,42.40%,0,0,0.000%,0.000%,0,0,0.00,,,,0,,'''

        stats = AdStatistic.objects.import_from_csv(StringIO(scv_file), ACCOUNT_ID)

        self.assertEqual(stats[0].start_time, datetime(2011,12,1,0,0))
        self.assertEqual(stats[0].end_time, datetime(2012,1,1,0,0))