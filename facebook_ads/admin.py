from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django import forms
from models import AdAccount, AdCampaign, AdCreative, AdGroup, AdStatistic, AdUser, ADCREATIVE_TYPE_CHOICES

def ad_image_preview(obj):
    return u'<a href="%s"><img src="%s" height="30" /></a>' % (obj.creative.image_url, obj.creative.image_url)
ad_image_preview.short_description = _('Image')
ad_image_preview.allow_tags = True

def related_adaccount_link(obj):
    return u'<a href="%s">%s</a>' % (reverse('admin:facebook_ads_adaccount_change', args=(obj.account.id,)), obj.account)
related_adaccount_link.short_description = _('Account')
related_adaccount_link.allow_tags = True

def related_adcampaign_link(obj):
    return u'<a href="%s">%s</a>' % (reverse('admin:facebook_ads_adcampaign_change', args=(obj.campaign.id,)), obj.campaign)
related_adcampaign_link.short_description = _('Campaign')
related_adcampaign_link.allow_tags = True

def related_adgroup_link(obj):
    return u'<a href="%s">%s</a>' % (reverse('admin:facebook_ads_adgroup_change', args=(obj.adgroup.id,)), obj.adgroup)
related_adgroup_link.short_description = _('Adgroup')
related_adgroup_link.allow_tags = True

def adgroup_link(obj):
    return u'<a href="%s">%s</a>' % (reverse('admin:facebook_ads_adgroup_change', args=(obj.id,)), obj)
adgroup_link.short_description = _('Adgroup')
adgroup_link.allow_tags = True


class StatsInline(admin.TabularInline):
    model = AdStatistic
    readonly_fields = (
        'start_time','end_time',
        related_adaccount_link,related_adcampaign_link,related_adgroup_link,
        'impressions','clicks','spent','social_impressions','social_clicks','social_spent','social_reach','actions','unique_impressions','unique_clicks','social_unique_impressions','social_unique_clicks','connections',
        'reach','frequency','ctr','social','social_ctr','cpc','cpm','unique_ctr',
        'page_likes','app_installs','event_responses',
    )
    extra = 0
    can_delete = False

class AccountStatsInline(StatsInline):
    exclude = ('statistic_id','campaign','adgroup')
class CampaignStatsInline(StatsInline):
    exclude = ('statistic_id','account','adgroup')
class GroupStatsInline(StatsInline):
    exclude = ('statistic_id','account','campaign')

class UserInlineForm(forms.ModelForm):
    permissions = forms.MultipleChoiceField(
        choices = AdUser._meta.get_field('permissions').choices,
        label = AdUser._meta.get_field('permissions').name
    )

class UserInline(admin.TabularInline):
    model = AdUser
    form = UserInlineForm
    extra = 0
    can_delete = False
    readonly_fields = ('uid','permissions','role')

class AdsInline(admin.TabularInline):

    model = AdGroup
    fields = (ad_image_preview,adgroup_link,'adgroup_status','ad_status')
    readonly_fields = fields
    extra = 0
    can_delete = False

class AdAccountAdmin(admin.ModelAdmin):
    inlines = [AccountStatsInline, UserInline]

class AdCampaignAdmin(admin.ModelAdmin):
    list_display = ('name','campaign_status','daily_budget','start_time')
    list_filter = ('campaign_status','account',)
    search_fields = ('name',)
    inlines = [AdsInline, CampaignStatsInline]

#def ad_preview(self):
#    lib = '''
#<script type="text/javascript">
#    $(document).ready(function() {
#        $(".fancybox").fancybox();
#    });
#</script>
#'''
#    return lib + '<a class="various fancybox" href="/auth/">%s_</a>' % (self.creative.preview_url)
#ad_preview.short_description = _('Preview')
#ad_preview.allow_tags = True

class AdGroupAdmin(admin.ModelAdmin):
#    class Media:
#        css = {
#            "all": ("http://fancyapps.com/fancybox/source/jquery.fancybox.css?v=2.0.4",)
#        }
#        js = (
#            "http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js",
#            "http://fancyapps.com/fancybox/lib/jquery.mousewheel-3.0.6.pack.js",
#            "http://fancyapps.com/fancybox/source/jquery.fancybox.pack.js?v=2.0.4",
#        )

    def creative__type(self, obj):
        return dict(ADCREATIVE_TYPE_CHOICES)[obj.creative.type]

    list_display = (ad_image_preview, 'name', related_adcampaign_link,'adgroup_status','ad_status','creative__type','max_bid','start_time','end_time','updated_time')
    list_display_links = ('name',)
    list_filter = ('campaign','adgroup_status','ad_status',)
    search_fields = ('name','creative__name','creative__title','creative__body',)
    inline_type = 'stacked'
    inline_reverse = ('creative','targeting')
    inlines = [GroupStatsInline]

class AdCreativeAdmin(admin.ModelAdmin):
    list_display = ('name','run_status','type','title','body')
    list_filter = ('run_status','type',)

class AdStatisticAdmin(admin.ModelAdmin):
    list_display = StatsInline.readonly_fields
    list_display_links = ('start_time','end_time',)
    list_filter = ('account','campaign',)

admin.site.register(AdAccount, AdAccountAdmin)
admin.site.register(AdCampaign, AdCampaignAdmin)
admin.site.register(AdCreative, AdCreativeAdmin)
admin.site.register(AdGroup, AdGroupAdmin)
admin.site.register(AdStatistic, AdStatisticAdmin)