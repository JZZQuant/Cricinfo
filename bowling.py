import csv
import lxml.html

url1='http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;orderby=start;'
url2 ='page='
url3 ='template=results;type=bowling;view=innings'
url5 = ['http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;orderby=start;template=results;type=bowling;view=innings']
for i in range(2,1717):
    url4 = url1 + url2 + str(i) + ';' + url3
    url5.append(url4)

out = csv.writer(open('test_bowl.csv','wb',))
out.writerow(('Player', 'Country', 'Overs','BPO','Mdns', 'Runs','Wkts','Econ','Inns','Opposition','Ground','Start Date'))
for page in url5:
    Player = []
    country = []
    Overs = []
    BPO = []
    Mdns = []
    Runs = []
    Wkts=[]
    Econ = []
    innings = []
    opposition = []
    ground = []
    startdate = []
    content = lxml.html.parse(page)

    Playe = content.xpath('//tr[@class="data1"]/td[1]/a')
    countr = content.xpath('//tr[@class="data1"]/td[1]/*')
    Over = content.xpath('//tr[@class="data1"]/td[2]')
    BP = content.xpath('//tr[@class="data1"]/td[3]')
    Mdn = content.xpath('//tr[@class="data1"]/td[4]')
    Run = content.xpath('//tr[@class="data1"]/td[5]')
    Wkt = content.xpath('//tr[@class="data1"]/td[6]')
    Eco = content.xpath('//tr[@class="data1"]/td[7]')
    inns = content.xpath('//tr[@class="data1"]/td[8]')
    oppos = content.xpath('//tr[@class="data1"]/td[10]/a')
    grou = content.xpath('//tr[@class="data1"]/td[11]/a')
    std = content.xpath('//tr[@class="data1"]/td[12]/b')

    Play = [bat.text for bat in Playe]
    cou = [c.tail for c in countr]
    Ove = [r.text for r in Over]
    B = [mint.text for mint in BP]
    Md = [bfaced.text for bfaced in Mdn]
    Ru = [fs.text for fs in Run]
    Wk = [s.text for s in Wkt]
    Ec = [srt.text for srt in Eco]
    inngs = [inn.text for inn in inns]
    opps = [opp.text for opp in oppos]
    grnd = [gr.text for gr in grou]
    sdate = [sd.text for sd in std]

    Player.extend(Play)
    country.extend(cou)
    Overs.extend(Ove)
    BPO.extend(B)
    Mdns.extend(Md)
    Runs.extend(Ru)
    Wkts.extend(Wk)
    Econ.extend(Ec)
    innings.extend(inngs)
    opposition.extend(opps)
    ground.extend(grnd)
    startdate.extend(sdate)
    zipped = zip(Player,country,Overs,BPO,Mdns,Runs,Wkts,Econ,innings,opposition,ground,startdate)
    for row in zipped:
        out.writerow(row)
        zipped = None
