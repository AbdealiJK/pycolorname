# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 22:57:26 2012

@author: drtrigon
"""

import pickle

from helper import store_data, load_data


# === Pantone Formula Guide Solid ===
# PMS_cal-print looks most reliable when compared to others
colors_01 = load_data('PMS_cal-print.pkl')
#colors_02 = load_data('PMS_logodesignteam.pkl')
#colors_03 = load_data('PMS_ackerdesign.pkl')
Formula_Guide_Solid = colors_01

# === Pantone Fashion + Home paper ===
# === Pantone Fashion + Home New Colors paper ===
colors_04 = load_data('PMS_pantonepaint_raw.pkl')
Fashion_Home_paper = colors_04


def get_pms_data_calprint():
    site = pywikibot.getSite()
    request_data = http.request(
        site, u'http://www.cal-print.com/InkColorChart.htm', no_hostname=True)
    bs_data = BeautifulSoup.BeautifulSoup(request_data)
    data = bs_data.table.table.table.tbody.findAll('tbody')
    result = {}
    for item in data:
        item = item.findAll('tr')
        key = re.sub('\s+', ' ', item[0].td.font.contents[0])
        val = item[1].td['bgcolor']
        val = (int(val[1:3], 16), int(val[3:5], 16), int(val[5:7], 16))
        if ('PMS' not in key) and ('Pantone' not in key):
            key = u'Pantone ' + key
        result[key] = val
    return result


def get_pms_data_logodesignteam():
    site = pywikibot.getSite()
    data = http.request(
        site,
        u'http://www.logodesignteam.com/logo-design-pantone-color-chart.html',
        no_hostname=True)
    css = http.request(
        site,
        u'http://www.logodesignteam.com/css/all.css',
        no_hostname=True).splitlines()
    data = BeautifulSoup.BeautifulSoup(data).findAll(
        'div', {'class': "pantone_colors_holder"})[0]
    color_text = data.findAll('ul', {'class': "color_text"})
    colors = data.findAll('ul', {'class': "colors"})
    result = {}
    for i in range(len(color_text)):
        a = color_text[i].findAll('li')
        b = colors[i].findAll('li')
        for j in range(len(a)):
            if (b[j]['class'] == 'clr'):
                break
            val = tuple()
            for item in css:
                if ('.%s{' % b[j]['class']) in item:
                    val = re.split('[\s;]', item)
                    val = val[1][17:]
                    val = (int(val[1:3], 16),
                           int(val[3:5], 16),
                           int(val[5:7], 16))
            if val:
                key = a[j].contents[0]
                if 'Pantone' not in key:
                    key = u'Pantone ' + key
                key = re.sub('Pantone (?P<ID>\d+)', 'PMS \g<ID>', key)
                result[key] = val
    return result


def get_pms_data_ackerdesign():
    site = pywikibot.getSite()
    data = http.request(
        site,
        u'http://www.ackerdesign.com/acker-design-pantone-chart.html',
        no_hostname=True)
    data = BeautifulSoup.BeautifulSoup(data).body.table.findAll('pre')
    result = {}
    for block in data:
        for item in block.contents:
            item = unicode(item).strip()
            item = [item[0:8].strip(), item[8:16].strip(), item[16:24].strip(),
                    item[24:32].strip(), item[32:40].strip(), ]
            if item[0][0] == u'<':
                continue
            key = u'PMS ' + item[0]
            val = tuple(map(int, item[1:4]))
            result[key] = val
    return result


def get_pms_data_materialsworld():
    # http://www.materials-world.com/pantone/pantone.htm
    pass


def get_pms_data_pantonepaint():
    site = pywikibot.getSite()
    data = http.request(
        site,
        u'http://www.pantonepaint.co.kr/color/colorchipsearch.asp?cmp=TPX',
        no_hostname=True)
    data = BeautifulSoup.BeautifulSoup(data).findAll(
        'div', {'onmouseover': "s(this);"})
    result = {}
    for item in data:
        val = re.split('[:;]', item['style'])[1]
        val = eval(unicode(val[3:]))
        key = u'PMS %s %s (%s)' % (re.split('&', item.contents[1])[0],
                                   item.contents[2],
                                   item.contents[0])
        key = re.sub('<.*?>', '', key)
        key = re.sub('PANTONE', ' Pantone', key)
        result[key] = val
    return result


def find_names(data):
    result = []
    for key in data:
        if not (key[:3] == 'PMS'):
            result.append(key)
    return result


def assign_color_names(data, names):
    from colormath.color_objects import RGBColor

    result = {}
    for key in data:
        rgb = data[key]

        # print "=== RGB Example: RGB->LAB ==="
        # Instantiate an Lab color object with the given values.
        rgb = RGBColor(rgb[0], rgb[1], rgb[2], rgb_type='sRGB')
        # Show a string representation.
        # print rgb
        # Convert RGB to LAB using a D50 illuminant.
        lab = rgb.convert_to('lab', target_illuminant='D65')
        # print lab
        # print "=== End Example ===\n"

        # Reference color.
        #color1 = LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22)
        # Color to be compared to the reference.
        #color2 = LabColor(lab_l=0.7, lab_a=14.2, lab_b=-1.80)
        color2 = lab

        res = (1.E100, '')
        for c in names:
            rgb = data[c]
            rgb = RGBColor(rgb[0], rgb[1], rgb[2], rgb_type='sRGB')
            color1 = rgb.convert_to('lab', target_illuminant='D65')

            # print "== Delta E Colors =="
            # print " COLOR1: %s" % color1
            # print " COLOR2: %s" % color2
            # print "== Results =="
            # print " CIE2000: %.3f" % color1.delta_e(color2, mode='cie2000')
            # Typically used for acceptability.
            # print "     CMC: %.3f (2:1)" % color1.delta_e(color2,
            #                                               mode='cmc',
            #                                               pl=2,
            #                                               pc=1)
            # Typically used to more closely model human percetion.
            # print "     CMC: %.3f (1:1)" % color1.delta_e(color2, mode='cmc',
            # pl=1, pc=1)

            r = color1.delta_e(color2, mode='cmc', pl=2, pc=1)
            if (r < res[0]):
                res = (r, c, data[c])
#        data[key]['Color']   = res[1]
#        data[key]['Delta_E'] = res[0]
#        data[key]['RGBref']  = res[2]
        result['%s (%s)' % (key, res[1])] = data[key]

    return result


def refresh():
    data_01 = get_pms_data_calprint()
    store_data('PMS_cal-print_raw.pkl', data_01)
    data_02 = get_pms_data_logodesignteam()
    store_data('PMS_logodesignteam_raw.pkl', data_02)
    data_03 = get_pms_data_ackerdesign()
    store_data('PMS_ackerdesign_raw.pkl', data_03)
    data_04 = get_pms_data_pantonepaint()
    store_data('PMS_pantonepaint_raw.pkl', data_04)
#    data_01 = load_data('PMS_cal-print_raw.pkl')
#    data_02 = load_data('PMS_logodesignteam_raw.pkl')
#    data_03 = load_data('PMS_ackerdesign_raw.pkl')

#    print len(data_01), len(data_02), len(data_03)
#    for item in data_01:
#        if (item in data_02) and (data_01[item] == data_02[item]):
#            continue
#        print item, \
#              (data_01[item] == data_02[item]), \
#              (data_01[item] == data_03[item])
#    print "So set 'data_01' looks most reliable to me..."
    data = data_01

    print "Retrieved number of colors:", len(data)

    data['White'] = (255, 255, 255)
    print "Added color 'White' to Pantone set."

    names = find_names(data)
    print "Number of human readable names:", len(names)

    data = assign_color_names(data, names)
    for item in data:
        print item, data[item]
    store_data('PMS_cal-print.pkl', data)
    print "Processed number of colors:", len(data)


if __name__ == '__main__':
    import re
    import sys

    sys.path.insert(0, '..')
    sys.path.insert(0, '.')

    import wikipedia as pywikibot
    from pywikibot.comms import http
    import BeautifulSoup

    refresh()
