# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'AdStatistic'
        db.create_table('facebook_ads_adstatistic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('statistic_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length='100')),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='adstatistics', null=True, to=orm['facebook_ads.AdAccount'])),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(related_name='adstatistics', null=True, to=orm['facebook_ads.AdCampaign'])),
            ('adgroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='adstatistics', null=True, to=orm['facebook_ads.AdGroup'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('impressions', self.gf('django.db.models.fields.IntegerField')()),
            ('clicks', self.gf('django.db.models.fields.IntegerField')()),
            ('spent', self.gf('django.db.models.fields.IntegerField')()),
            ('social_impressions', self.gf('django.db.models.fields.IntegerField')()),
            ('social_clicks', self.gf('django.db.models.fields.IntegerField')()),
            ('social_spent', self.gf('django.db.models.fields.IntegerField')()),
            ('actions', self.gf('django.db.models.fields.IntegerField')()),
            ('unique_impressions', self.gf('django.db.models.fields.IntegerField')()),
            ('unique_clicks', self.gf('django.db.models.fields.IntegerField')()),
            ('social_unique_impressions', self.gf('django.db.models.fields.IntegerField')()),
            ('social_unique_clicks', self.gf('django.db.models.fields.IntegerField')()),
            ('connections', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('facebook_ads', ['AdStatistic'])

        # Adding field 'AdGroup.creative'
        db.add_column('facebook_ads_adgroup', 'creative', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='adgroups', to=orm['facebook_ads.AdCreative']), keep_default=False)

        # Changing field 'AdGroup.targeting'
        db.alter_column('facebook_ads_adgroup', 'targeting_id', self.gf('django.db.models.fields.related.OneToOneField')(default=0, unique=True, to=orm['facebook_ads.Targeting']))

        # Changing field 'AdCreative.run_status'
        db.alter_column('facebook_ads_adcreative', 'run_status', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'AdCreative.type'
        db.alter_column('facebook_ads_adcreative', 'type', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'AdCampaign.start_time'
        db.alter_column('facebook_ads_adcampaign', 'start_time', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'AdCampaign.updated_time'
        db.alter_column('facebook_ads_adcampaign', 'updated_time', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'AdCampaign.campaign_status'
        db.alter_column('facebook_ads_adcampaign', 'campaign_status', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'AdCampaign.daily_imps'
        db.alter_column('facebook_ads_adcampaign', 'daily_imps', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'AdAccount.daily_spend_limit'
        db.alter_column('facebook_ads_adaccount', 'daily_spend_limit', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'AdAccount.vat_status'
        db.alter_column('facebook_ads_adaccount', 'vat_status', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'AdAccount.timezone_id'
        db.alter_column('facebook_ads_adaccount', 'timezone_id', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'AdAccount.account_status'
        db.alter_column('facebook_ads_adaccount', 'account_status', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'AdAccount.is_personal'
        db.alter_column('facebook_ads_adaccount', 'is_personal', self.gf('django.db.models.fields.IntegerField')(null=True))


    def backwards(self, orm):

        # Deleting model 'AdStatistic'
        db.delete_table('facebook_ads_adstatistic')

        # Deleting field 'AdGroup.creative'
        db.delete_column('facebook_ads_adgroup', 'creative_id')

        # Changing field 'AdGroup.targeting'
        db.alter_column('facebook_ads_adgroup', 'targeting_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['facebook_ads.Targeting']))

        # Changing field 'AdCreative.run_status'
        db.alter_column('facebook_ads_adcreative', 'run_status', self.gf('django.db.models.fields.SmallIntegerField')(default=None))

        # Changing field 'AdCreative.type'
        db.alter_column('facebook_ads_adcreative', 'type', self.gf('django.db.models.fields.IntegerField')(default=None))

        # Changing field 'AdCampaign.start_time'
        db.alter_column('facebook_ads_adcampaign', 'start_time', self.gf('django.db.models.fields.DateTimeField')(default=None))

        # Changing field 'AdCampaign.updated_time'
        db.alter_column('facebook_ads_adcampaign', 'updated_time', self.gf('django.db.models.fields.DateTimeField')(default=None))

        # Changing field 'AdCampaign.campaign_status'
        db.alter_column('facebook_ads_adcampaign', 'campaign_status', self.gf('django.db.models.fields.SmallIntegerField')(default=None))

        # Changing field 'AdCampaign.daily_imps'
        db.alter_column('facebook_ads_adcampaign', 'daily_imps', self.gf('django.db.models.fields.IntegerField')(default=None))

        # Changing field 'AdAccount.daily_spend_limit'
        db.alter_column('facebook_ads_adaccount', 'daily_spend_limit', self.gf('django.db.models.fields.IntegerField')(default=None))

        # Changing field 'AdAccount.vat_status'
        db.alter_column('facebook_ads_adaccount', 'vat_status', self.gf('django.db.models.fields.IntegerField')(default=None))

        # Changing field 'AdAccount.timezone_id'
        db.alter_column('facebook_ads_adaccount', 'timezone_id', self.gf('django.db.models.fields.IntegerField')(default=None))

        # Changing field 'AdAccount.account_status'
        db.alter_column('facebook_ads_adaccount', 'account_status', self.gf('django.db.models.fields.SmallIntegerField')(default=None))

        # Changing field 'AdAccount.is_personal'
        db.alter_column('facebook_ads_adaccount', 'is_personal', self.gf('django.db.models.fields.IntegerField')(default=None))


    models = {
        'facebook_ads.adaccount': {
            'Meta': {'object_name': 'AdAccount'},
            'account_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'account_status': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'business_city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_country_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_street2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_zip': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'daily_spend_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_personal': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timezone_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'timezone_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'vat_status': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'facebook_ads.adcampaign': {
            'Meta': {'object_name': 'AdCampaign'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adcampaigns'", 'to': "orm['facebook_ads.AdAccount']"}),
            'campaign_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'campaign_status': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'daily_budget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'daily_imps': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lifetime_budget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'facebook_ads.adcreative': {
            'Meta': {'object_name': 'AdCreative'},
            'auto_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '135'}),
            'count_current_adgroups': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'creative_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_hash': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'link_url': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'object_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'preview_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'related_fan_page': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'run_status': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'story_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'view_tag': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'facebook_ads.adgroup': {
            'Meta': {'object_name': 'AdGroup'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adgroups'", 'to': "orm['facebook_ads.AdAccount']"}),
            'ad_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'ad_status': ('django.db.models.fields.IntegerField', [], {}),
            'adgroup_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'adgroup_status': ('django.db.models.fields.IntegerField', [], {}),
            'bid_type': ('django.db.models.fields.IntegerField', [], {}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adgroups'", 'to': "orm['facebook_ads.AdCampaign']"}),
            'creative': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adgroups'", 'to': "orm['facebook_ads.AdCreative']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_bid': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'targeting': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'adgroup'", 'unique': 'True', 'to': "orm['facebook_ads.Targeting']"}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'facebook_ads.adstatistic': {
            'Meta': {'object_name': 'AdStatistic'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adstatistics'", 'null': 'True', 'to': "orm['facebook_ads.AdAccount']"}),
            'actions': ('django.db.models.fields.IntegerField', [], {}),
            'adgroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adstatistics'", 'null': 'True', 'to': "orm['facebook_ads.AdGroup']"}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adstatistics'", 'null': 'True', 'to': "orm['facebook_ads.AdCampaign']"}),
            'clicks': ('django.db.models.fields.IntegerField', [], {}),
            'connections': ('django.db.models.fields.IntegerField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impressions': ('django.db.models.fields.IntegerField', [], {}),
            'social_clicks': ('django.db.models.fields.IntegerField', [], {}),
            'social_impressions': ('django.db.models.fields.IntegerField', [], {}),
            'social_spent': ('django.db.models.fields.IntegerField', [], {}),
            'social_unique_clicks': ('django.db.models.fields.IntegerField', [], {}),
            'social_unique_impressions': ('django.db.models.fields.IntegerField', [], {}),
            'spent': ('django.db.models.fields.IntegerField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'statistic_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'100'"}),
            'unique_clicks': ('django.db.models.fields.IntegerField', [], {}),
            'unique_impressions': ('django.db.models.fields.IntegerField', [], {})
        },
        'facebook_ads.targeting': {
            'Meta': {'object_name': 'Targeting'},
            'age_max': ('facebook_ads.fields.PositiveSmallIntegerRangeField', [], {'null': 'True', 'blank': 'True'}),
            'age_min': ('facebook_ads.fields.PositiveSmallIntegerRangeField', [], {'null': 'True', 'blank': 'True'}),
            'broad_age': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'cities': ('facebook_ads.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'college_majors': ('facebook_ads.fields.CommaSeparatedCharField', [], {'max_length': '100'}),
            'college_networks': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'college_years': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'connections': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'countries': ('facebook_ads.fields.CommaSeparatedCharField', [], {'max_length': '100', 'blank': 'True'}),
            'education_statuses': ('facebook_ads.fields.CommaSeparatedCharField', [], {'max_length': '100'}),
            'excluded_connections': ('facebook_ads.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'friends_of_connections': ('facebook_ads.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'genders': ('facebook_ads.fields.CommaSeparatedCharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interested_in': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'keywords': ('facebook_ads.fields.CommaSeparatedCharField', [], {'max_length': '4000'}),
            'locales': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'radius': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'regions': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'relationship_statuses': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_adclusters': ('facebook_ads.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'user_event': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'work_networks': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'zips': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['facebook_ads']
