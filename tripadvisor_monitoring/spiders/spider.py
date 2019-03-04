## import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from tripadvisor_monitoring.items import Tripadvisor_monitoringItem
from csv import DictReader
from lxml import html
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
import json
import jsonpath
class TripadvisorSpider(CrawlSpider):
    name = "tripadvisor_monitoring"
    item_count = 0
    base = "http://www.tripadvisor.com"
    next_page = None
    # start_urls = ["https://www.tripadvisor.com/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS_RESP&metaReferer="]

    def start_requests(self):
        with open('tripadvisor_monitoring_input133.csv') as rows:
            for row in DictReader(rows):
                listing = row["listing"].replace(',', '')
                yield scrapy.Request(listing, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        review_codes =[]
        codes_id = []
        reviews = None
        print "Parsing Post"
        response = response.replace(body=response.body.replace('<br />', '\n'))
        parser = html.fromstring(response.text)
        review_codes = parser.xpath('//div[@data-reviewid]/@data-reviewid')
        self.next_page = response.xpath('//div[contains(@class, "responsive_pagination")]//div[contains(@class,"ui_pagination")]//a[contains(@class, "nav next")]/@href').extract_first()
        if self.next_page == "":
            next_page = response.xpath(
                '//div[contains(@class,"ui_pagination")]//a[contains(@class, "nav next")]/@href').extract()

        for code in review_codes:
            if code not in codes_id:
                codes_id.append(code)
        reviews = ','.join(codes_id)

        headers = {
            'authority': 'www.tripadvisor.com',
            'method': 'POST',
            'path': '/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS_RESP&metaReferer=',
            'scheme': 'https',
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'es-ES,es;q=0.9',
            'content-length': '1654',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'TAUnique=%1%enc%3AyofKqfE%2BzOIsMFjl%2FEpZ7M4QzOyhVhDnLdUp3PqwlFqRqDIW%2BjDBvQ%3D%3D; __gads=ID=afebf7b4dd07f4e3:T=1537873235:S=ALNI_MbXz3mm1Mj-_Ov2UM196W7V7AJgEQ; G_ENABLED_IDPS=google; _omappvp=bSZt2nyWoJAozOWb0JGPpB8qLsWm7Jh32xF3TeXMymGhmhjLL8u32IS0XCXq7kvsALg3i5Gmy0BAVEyZIxB73bHXPKH01jwz; _ga=GA1.2.893450275.1539088267; TALanguage=en; TACds=B.1.374855.2.2018-11-04; TASSK=enc%3AALLymim%2FPL5%2FazFDRlcQdQ5ufU7RYDEIzRUJwX22j77zbWo3%2FQzYkePK70QBNukV14RlfnWeeD1ZDj1O3iPn7jCpTTiaXPkiiExXxKIto7Y4xuoJryWdn7cxrp6NuZeQXg%3D%3D; PMC=V2*MS.37*MD.20181220*LD.20181220; TATravelInfo=V2*AY.2018*AM.12*AD.30*DY.2018*DM.12*DD.31*A.2*MG.-1*HP.2*FL.3*DSM.1545302096642*RS.1; TART=%1%enc%3AnwTB3EI6RpYnPcciQ2b0DTo8r74nwcW7hA%2BllATrxf0YDFsR0iwx%2BXomWUu932oTYEWlR3T%2BCYs%3D; CM=%1%HanaPersist%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CHanaSession%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CMobSess%2C1%2C-1%7CWShadeSeen%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CCCUVOwnPers%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCpmPopunder_1%2C%2C-1%7CCCSess%2C9%2C-1%7CCpmPopunder_2%2C1%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7C%24%2CUSD%2C0%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CMobPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7CCCUVOwnSess%2C%2C-1%7CUVOwnersPers%2C%2C-1%7CLastPopunderId%2C137-1859-null%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7CShownMobilePopup%2Ctrue%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; VRMCID=%1%V1*id.10568*llp.%2FTripAdvisorInsights*e.1545911817104; _gid=GA1.2.918751501.1545307018; PAC=AAzdqvc4HOeLl0uK8gy_9SqLTytf2_ETCu13SMQYkTqsDpewbU08t5nuQYLNtN-BSAYcRKIf2f9IKunXF6jRcc8amsDzHEsLkI1TGP3Le5nlOxPxiDiGWkCAlv1dxCFDDh1iJa8wBigRJm2jnuhAY41vDzDELFdw5vgbVCzv-f5Txt519KfbUrqflHQQXpdbSH1g0DTpbXaRanp15ko6Z2S-S9jR6y6cuqZNb_mQvufa6C7aHzd5YVo7T4wLVGc5SvgJD2TYjtoHbn4PDGWAzpTcdZM42cIAd044zGutmhJ2pQtNJ6usu-FtyFBajVNh4YrvM1Irvy3nd_YN6lBzuIo%3D; TAPD=tripadvisor.es; ServerPool=X; TAReturnTo=%1%%2FHotel_Review-g580293-d254860-Reviews-Barcelo_Illetas_Albatros-Calvia_Majorca_Balearic_Islands.html; roybatty=TNI1625!AOlBpmKWUR7Q6ad5QMNBuU6tYnNd5NCQC53N07D57B3nlNBpF6pyTkklWoJxytDrFOJXtbMPOB1hN39tnLckGMxYoRsW%2FBKqWsicSWlesV3nNPbzPj6kAe66EL7PstKdp%2BFGigKAOTUOXOaFn74MCsCzqONWrDqU8e7r50aZ75g1%2C1; TASession=V2ID.9DDAD98F705B27B6B2BFF6667910C359*SQ.46*LS.PageMoniker*GR.89*TCPAR.94*TBR.15*EXEX.32*ABTR.74*PHTB.39*FS.59*CPU.8*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*FLO.254860*TRA.false*LD.254860; TAUD=LA-1545302114717-1*RDD-1-2018_12_20*HDD-45263-2018_12_30.2018_12_31.1*LD-34760532-2018.12.30.2018.12.31*LG-34760534-2.1.F.',
            'origin': 'https://www.tripadvisor.com',
            'referer': response.url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'x-puid': 'XBv4JwokG4sAAfgICZEAAACB',
            'X-Requested-With': 'XMLHttpRequest'
        }
        form_data = {'reviews': reviews,
                     'contextChoice': 'DETAIL_HR',
                     'loadMtHeader': 'false',
                     'haveJses': 'earlyRequireDefine%2Camdearly%2Cglobal_error%2Clong_lived_global%2Capg-Hotel_Review%2Capg-Hotel_Review-in%2Cbootstrap%2Cdesktop-rooms-guests-dust-en_US%2Cresponsive-calendar-templates-dust-en_US%2Cresponsive-heatmap-calendar-templates-dust-en_US%2C%40ta%2Fcommon.global%2C%40ta%2Ftracking.interactions%2C%40ta%2Fsocial.button%2C%40ta%2Fpublic.maps%2C%40ta%2Foverlays.pieces%2C%40ta%2Foverlays.managers%2C%40ta%2Foverlays.headers%2C%40ta%2Foverlays.fullscreen-overlay%2C%40ta%2Foverlays.toast%2C%40ta%2Foverlays.modal%2C%40ta%2Ftrips.save-to-trip%2C%40ta%2Ftrips.trip-link%2C%40ta%2Fcross-sells.types%2C%40ta%2Fcross-sells.logic%2C%40ta%2Fcross-sells.container%2C%40ta%2Fsocial.blocks%2C%40ta%2Fsocial.review-inline-follow-widget%2C%40ta%2Fmedia.image%2C%40ta%2Fhotels.hotel-review-layout%2C%40ta%2Fhotels.hotel-review-new-hotel-preview%2C%40ta%2Foverlays.shift%2C%40ta%2Foverlays.internal%2C%40ta%2Foverlays.attached-overlay%2C%40ta%2Fhotels.tags%2C%40ta%2Foverlays.attached-arrow-overlay%2C%40ta%2Foverlays.tooltip%2C%40ta%2Fcross-sells.items%2C%40ta%2Fcross-sells.rendering%2C%40ta%2Fcross-sells.component%2C%40ta%2Fhotels.hotel-review-new-hotel-banner%2C%40ta%2Fhotels.hotel-review-atf-photos-2018-redesign%2C%40ta%2Fmaps.snapshot%2Chotels.hotel-review-overview%2Chotels.hotel-review-roomtips%2Chotels.hotel-review-photos%2C%40ta%2Fplatform.import%2C%40ta%2Fplatform.runtime%2Cmasthead_search_late_load%2Ctaevents%2Cp13n_masthead_search__deferred__lateHandlers',
                     'haveCsses': 'apg-Hotel_Review-in%2Cresponsive_calendars_corgi',
                     'Action': 'install'
                     }
        #cookies = {"SetCurrency": "USD"}
        return scrapy.FormRequest.from_response(
                response, url="https://www.tripadvisor.com/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS_RESP&metaReferer=",
                formdata=form_data, headers=headers,
                callback=self.parse_review)

    def parse_review(self, response):
        ml_item = Tripadvisor_monitoringItem()
        #c = response.xpath('//div[contains(@class, "responsive_pagination")]//div[contains(@class,"ui_pagination")]//a[contains(@class, "nav next")]/@href').extract_first()
        print "Parsing results"
        response = response.replace(body=response.body.replace('<br/>', '\n'))
        parser = html.fromstring(response.text)
        review_lists = parser.xpath('//div[contains(@class,"reviewSelector")]')
        for review in review_lists:
            ml_item['review_text'] = review.xpath('.//div[@class="prw_rup prw_reviews_text_summary_hsx"]//div[@class="entry"]//p[@class="partial_entry"]//text()')[0].replace(',', '').replace('\n', '').replace('... More', '').replace('\n\n', '').replace('\r\n', '').replace('\r', '')
            #ml_item['review_text'] = ' '.join(i.strip() for i in review_text if i.strip()).replace(',', '').replace('\n', '').replace('... More', '')
            response_text = review.xpath(
                './/div[@class="mgrRspnInline"]//div[@class="prw_rup prw_reviews_text_summary_hsx"]//text()')
            ml_item['response_text'] = ' '.join(i.strip() for i in response_text if i.strip()).replace(',', '').replace('\n', '').replace('... More', '').replace('\n\n', '').replace('\r\n', '').replace('\r', '')
            rating = review.xpath('.//span[contains(@class,"ui_bubble_rating bubble")]/@class')
            ml_item['rating'] = ' '.join(i.strip() for i in rating if i.strip()).replace('ui_bubble_rating bubble_', '')
            self.item_count += 1
            if self.item_count > 100000:
                raise CloseSpider('item_exceeded')
            yield ml_item

        #next_page = response.xpath('//div[contains(@class,"ui_pagination")]//a[contains(@class, "nav next")]/@href').extract()
        if self.next_page:
            url = self.base + self.next_page
            print 'Next results page %s' % url
            yield scrapy.Request(url, self.parse_item)

