# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Targeting'
        db.create_table('facebook_ads_targeting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('countries', self.gf('facebook_ads.fields.CommaSeparatedCharField')(max_length=100, blank=True)),
            ('cities', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zips', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('regions', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('radius', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('locales', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('keywords', self.gf('facebook_ads.fields.CommaSeparatedCharField')(max_length=100)),
            ('user_adclusters', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('interested_in', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('genders', self.gf('facebook_ads.fields.CommaSeparatedCharField')(max_length=5, null=True, blank=True)),
            ('age_min', self.gf('facebook_ads.fields.PositiveSmallIntegerRangeField')(null=True, blank=True)),
            ('age_max', self.gf('facebook_ads.fields.PositiveSmallIntegerRangeField')(null=True, blank=True)),
            ('broad_age', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('relationship_statuses', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100, null=True, blank=True)),
            ('user_event', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('connections', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('excluded_connections', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('friends_of_connections', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('college_networks', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('work_networks', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('education_statuses', self.gf('facebook_ads.fields.CommaSeparatedCharField')(max_length=100)),
            ('college_years', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('college_majors', self.gf('facebook_ads.fields.CommaSeparatedCharField')(max_length=100)),
        ))
        db.send_create_signal('facebook_ads', ['Targeting'])

        # Adding field 'AdGroup.targeting'
        db.add_column('facebook_ads_adgroup', 'targeting', self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['facebook_ads.Targeting'], unique=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Targeting'
        db.delete_table('facebook_ads_targeting')

        # Deleting field 'AdGroup.targeting'
        db.delete_column('facebook_ads_adgroup', 'targeting_id')


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
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facebook_ads.AdAccount']"}),
            'ad_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'ad_status': ('django.db.models.fields.IntegerField', [], {}),
            'adgroup_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'adgroup_status': ('django.db.models.fields.IntegerField', [], {}),
            'bid_type': ('django.db.models.fields.IntegerField', [], {}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facebook_ads.AdCampaign']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_bid': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'targeting': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['facebook_ads.Targeting']", 'unique': 'True'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'facebook_ads.targeting': {
            'Meta': {'object_name': 'Targeting'},
            'age_max': ('facebook_ads.fields.PositiveSmallIntegerRangeField', [], {'null': 'True', 'blank': 'True'}),
            'age_min': ('facebook_ads.fields.PositiveSmallIntegerRangeField', [], {'null': 'True', 'blank': 'True'}),
            'broad_age': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'cities': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'college_majors': ('facebook_ads.fields.CommaSeparatedCharField', [], {'max_length': '100'}),
            'college_networks': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'college_years': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'connections': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'countries': ('facebook_ads.fields.CommaSeparatedCharField', [], {'max_length': '100', 'blank': 'True'}),
            'education_statuses': ('facebook_ads.fields.CommaSeparatedCharField', [], {'max_length': '100'}),
            'excluded_connections': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'friends_of_connections': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'genders': ('facebook_ads.fields.CommaSeparatedCharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interested_in': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'keywords': ('facebook_ads.fields.CommaSeparatedCharField', [], {'max_length': '100'}),
            'locales': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'radius': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'regions': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'relationship_statuses': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_adclusters': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_event': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'work_networks': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'zips': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['facebook_ads']
