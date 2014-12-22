# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AdAccount'
        db.create_table('facebook_ads_adaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('account_status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('daily_spend_limit', self.gf('django.db.models.fields.IntegerField')()),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('timezone_id', self.gf('django.db.models.fields.IntegerField')()),
            ('timezone_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_personal', self.gf('django.db.models.fields.IntegerField')()),
            ('business_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('business_street', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('business_street2', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('business_city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('business_state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('business_zip', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('business_country_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('vat_status', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('facebook_ads', ['AdAccount'])

        # Adding model 'AdCampaign'
        db.create_table('facebook_ads_adcampaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['facebook_ads.AdAccount'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('daily_budget', self.gf('django.db.models.fields.IntegerField')()),
            ('campaign_status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('lifetime_budget', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('facebook_ads', ['AdCampaign'])

        # Adding model 'AdCreative'
        db.create_table('facebook_ads_adcreative', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creative_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image_hash', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('count_current_adgroups', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('run_status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link_url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('preview_url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('related_fan_page', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('auto_update', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('story_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('facebook_ads', ['AdCreative'])

        # Adding model 'AdGroup'
        db.create_table('facebook_ads_adgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('adgroup_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('ad_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['facebook_ads.AdCampaign'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('adgroup_status', self.gf('django.db.models.fields.IntegerField')()),
            ('bid_type', self.gf('django.db.models.fields.IntegerField')()),
            ('max_bid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('facebook_ads', ['AdGroup'])


    def backwards(self, orm):
        
        # Deleting model 'AdAccount'
        db.delete_table('facebook_ads_adaccount')

        # Deleting model 'AdCampaign'
        db.delete_table('facebook_ads_adcampaign')

        # Deleting model 'AdCreative'
        db.delete_table('facebook_ads_adcreative')

        # Deleting model 'AdGroup'
        db.delete_table('facebook_ads_adgroup')


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
            'daily_budget': ('django.db.models.fields.IntegerField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lifetime_budget': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
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
