# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AdCreative.body'
        db.alter_column('facebook_ads_adcreative', 'body', self.gf('django.db.models.fields.CharField')(max_length=135))

        # Changing field 'AdCreative.title'
        db.alter_column('facebook_ads_adcreative', 'title', self.gf('django.db.models.fields.CharField')(max_length=25))

        # Changing field 'AdCreative.story_id'
        db.alter_column('facebook_ads_adcreative', 'story_id', self.gf('django.db.models.fields.BigIntegerField')(null=True))

        # Changing field 'AdCreative.link_url'
        db.alter_column('facebook_ads_adcreative', 'link_url', self.gf('django.db.models.fields.CharField')(max_length=1024))

        # Changing field 'AdCreative.object_id'
        db.alter_column('facebook_ads_adcreative', 'object_id', self.gf('django.db.models.fields.BigIntegerField')(null=True))

        # Changing field 'AdCreative.run_status'
        db.alter_column('facebook_ads_adcreative', 'run_status', self.gf('django.db.models.fields.SmallIntegerField')())

        # Changing field 'AdCreative.type'
        db.alter_column('facebook_ads_adcreative', 'type', self.gf('django.db.models.fields.IntegerField')())


    def backwards(self, orm):

        # Changing field 'AdCreative.body'
        db.alter_column('facebook_ads_adcreative', 'body', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'AdCreative.title'
        db.alter_column('facebook_ads_adcreative', 'title', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'AdCreative.story_id'
        db.alter_column('facebook_ads_adcreative', 'story_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=100))

        # Changing field 'AdCreative.link_url'
        db.alter_column('facebook_ads_adcreative', 'link_url', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'AdCreative.object_id'
        db.alter_column('facebook_ads_adcreative', 'object_id', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'AdCreative.run_status'
        db.alter_column('facebook_ads_adcreative', 'run_status', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'AdCreative.type'
        db.alter_column('facebook_ads_adcreative', 'type', self.gf('django.db.models.fields.CharField')(max_length=100))


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
            'run_status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'story_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'view_tag': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
