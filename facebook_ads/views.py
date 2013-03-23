# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from forms import StatisticImportForm
from models import AdStatistic, AdGroup, CSVFormatError
#import requests

def import_statistic(request):

    context = {}

    if request.method == 'POST':
        form = StatisticImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                statistic_instances = AdStatistic.objects.import_from_csv(request.FILES['csv'], request.POST['account'])
                context['message'] = u'Imported successful'
            except CSVFormatError, e:
                context['message'] = e.message
    else:
        form = StatisticImportForm()

    context['form'] = form

    return render_to_response('facebook_ads/import_statistic.html', context, context_instance=RequestContext(request))

def ad_preview(request, ad_id):
    '''
    Return preview of ad without restriction tag for preventing output preview in iframes
    '''
#    response = requests.get("http://www.facebook.com/ads/api/creative_preview.php?cid=%d" % int(graph_id))
#    content = response.content.replace('<noscript><meta http-equiv="X-Frame-Options" content="deny" /></noscript>', '')

    adgroup = AdGroup.objects.get(adgroup_id=ad_id)

    content = '''
<!DOCTYPE html>
<html lang="en" id="facebook" class="no_js">
<head><meta charset="utf-8" />
<noscript> <meta http-equiv="refresh" content="0; URL=/ads/api/creative_preview.php?cid=6003592156733&amp;_fb_noscript=1" /> </noscript>
<meta name="robots" content="noodp, noydir" /><meta name="description" content=" Facebook is a social utility that connects people with friends and others who work, study and live around them. People use Facebook to keep up with friends, upload an unlimited number of photos, post links and videos, and learn more about the people they meet." /><link rel="alternate" media="handheld" href="http://www.facebook.com/ads/api/creative_preview.php?cid=6003592156733" />
<link type="text/css" rel="stylesheet" href="http://static.ak.fbcdn.net/rsrc.php/v1/yh/r/MUvfLtq3lI8.css" />
<link type="text/css" rel="stylesheet" href="http://static.ak.fbcdn.net/rsrc.php/v1/yD/r/6pZwh33RDO6.css" />
<script type="text/javascript" src="http://static.ak.fbcdn.net/rsrc.php/v1/yS/r/6vX4bKXSO7V.js"></script>
<script>window.Bootloader && Bootloader.done(["aomZC"]);</script><script></script><title>Creative Preview</title>
<link rel="search" type="application/opensearchdescription+xml" href="http://static.ak.fbcdn.net/rsrc.php/yJ/r/H2SSvhJMJA-.xml" title="Facebook" />
<link rel="shortcut icon" href="http://static.ak.fbcdn.net/rsrc.php/yi/r/q9U99v3_saj.ico" /></head>
<body class="safari4 Locale_en_US">
<input type="hidden" autocomplete="off" id="post_form_id" name="post_form_id" value="08978deefa0577f13c0e87ae920b5c62" />
<div class="emu_ad emu_preview"><div>
<div class="fbAdUnit" data-ad="&#123;&quot;adid&quot;:null,&quot;segment&quot;:&quot;premium&quot;&#125;" id="-id_4f5b263a197b40d33756167">
<div class="fbEmu fbEmuEgo">
<a class="fbEmuTitleBodyImageLink fbEmuLink" onclick="">
    <div class="fbEmuTitleBodyImageDiv">
        <div class="title"><span class="forceLTR">%(name)s</span></div>
        <div class="adInfo"><span class="identity"></span></div>
        <div class="clearfix uiImageBlock image_body_block">
            <div class="image fbEmuImage uiImageBlockImage uiImageBlockMediumImage lfloat"><img class="img" src="%(image_url)s" alt="" /></div>
            <div class="uiImageBlockContent "><div class="body"><div class="forceLTR">%(body)s</div></div></div>
        </div>
    </div>
</a>
</body>
</html>
'''
# like: <div class="inline"><div class="clearfix action"><a class="uiIconText emuEventfad_fan  fbEmuLink lfloat" style="padding-left: 17px;" href="#" rel="async-post" ajaxify="/ajax/emu/end.php?eid=AQJDFfM-OfPxguKQmGEPMaLTgy5NRuKWzCUAElDtJ9ulm2C4A3h4b_LomH0ZeKYfAY-o2xwLTiuaUvn_Hhem-0iglwArUib-3qY-uvcllFVyWigsNaW3h_ZyfjjBfADYR3m689l914VvEON6CAlor174VqWD3ye1Jqy8Jjm9kNdqmORxHAG8MMOtJbZUMsew1pHgYYn1mvStOSBysnHZqVtHIzbgqr0CFBNBzeZsIw8z2-eKMRmpP43CjsJ-N1cCV-k3KfDxldJzxaS2tJxfUuCaEjjNVnO8y-AxkidtFmFkWM6DlzepMuVA9f2vWWovvbU0Ckup0eqOYVDd1Tz3kx6U4MkQ3Zt9F-NjKwkKlK73EacfgNygpmeW243vumvsLRp4ob5WHeWSN-P8tE-_FXvur7412WDRI5zjtnuT4pToHZ58u7ybtAisno7UC21QFzgO54D1TBPtsNoSD5A70KTFnfKc6E5Bq3w_jOF2e1QBD5r3D1Qqvkfj_wDLChkg8OI&amp;f=0&amp;ui=-id_4f5b263a197b40d33756167&amp;en=fad_fan&amp;ed=244611672256865&amp;a=1"><i class="img sp_4kdh1e sx_253e6f" style="top: 1px;"></i>Like</a><span class="fbEmuContext"> &middot; 1,907 people like this.</span></div></div></div></div></div></div>
    try:
        content = content % adgroup.creative.__dict__
    except AttributeError:
        content = _('Sorry, no preview data for ad')

    return HttpResponse(content)