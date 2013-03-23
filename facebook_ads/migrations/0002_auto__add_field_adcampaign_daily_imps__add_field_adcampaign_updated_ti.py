# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'AdCampaign.daily_imps'
        db.add_column('facebook_ads_adcampaign', 'daily_imps', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'AdCampaign.updated_time'
        db.add_column('facebook_ads_adcampaign', 'updated_time', self.gf('django.db.models.fields.DateTimeField')(default=None), keep_default=False)

        # Changing field 'AdCampaign.daily_budget'
        db.alter_column('facebook_ads_adcampaign', 'daily_budget', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'AdCampaign.lifetime_budget'
        db.alter_column('facebook_ads_adcampaign', 'lifetime_budget', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'AdCampaign.end_time'
        db.alter_column('facebook_ads_adcampaign', 'end_time', self.gf('django.db.models.fields.DateTimeField')(null=True))


    def backwards(self, orm):
        
        # Deleting field 'AdCampaign.daily_imps'
        db.delete_column('facebook_ads_adcampaign', 'daily_imps')

        # Deleting field 'AdCampaign.updated_time'
        db.delete_column('facebook_ads_adcampaign', 'updated_time')

        # Changing field 'AdCampaign.daily_budget'
        db.alter_column('facebook_ads_adcampaign', 'daily_budget', self.gf('django.db.models.fields.IntegerField')(default=9))

        # Changing field 'AdCampaign.lifetime_budget'
        db.alter_column('facebook_ads_adcampaign', 'lifetime_budget', self.gf('django.db.models.fields.IntegerField')(default=0))

        # Changing field 'AdCampaign.end_time'
        db.alter_column('facebook_ads_adcampaign', 'end_time', self.gf('django.db.models.fields.DateTimeField')(default=None))


    models = {
        'facebook_ads.adaccount': {
            'Meta': {'object_name': 'AdAccount'},
            'account_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'account_status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'business_city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_country_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_street2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_zip': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'daily_spend_limit': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_personal': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timezone_id': ('django.db.models.fields.IntegerField', [], {}),
            'timezone_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'vat_status': ('django.db.models.fields.IntegerField', [], {})
        },
        'facebook_ads.adcampaign': {
            'Meta': {'object_name': 'AdCampaign'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facebook_ads.AdAccount']"}),
            'campaign_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'campaign_status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'daily_budget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'daily_imps': ('django.db.models.fields.IntegerField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lifetime_budget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'facebook_ads.adcreative': {
            'Meta': {'object_name': 'AdCreative'},
            'auto_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'count_current_adgroups': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'creative_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_hash': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'link_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'preview_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'related_fan_page': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'run_status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'story_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'facebook_ads.adgroup': {
            'Meta': {'object_name': 'AdGroup'},
            'ad_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'adgroup_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'adgroup_status': ('django.db.models.fields.IntegerField', [], {}),
            'bid_type': ('django.db.models.fields.IntegerField', [], {}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facebook_ads.AdCampaign']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_bid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['facebook_ads']
