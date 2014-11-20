import csv
import lxml.html

url1='http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;orderby=start;'
url2 ='page='
url3 ='template=results;type=batting;view=innings'
url5 = ['http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;orderby=start;template=results;type=batting;view=innings']
for i in range(2,1669):
    url4 = url1 + url2 + str(i) + ';' + url3
    url5.append(url4)

out = csv.writer(open('test_batsmen.csv','wb',))
out.writerow(('Player', 'Country', 'Minutes', 'Runs','Balls Faced','Fours','Sixes','Strike Rate','Inns','Opposition','Ground','Start Date'))
for page in url5:
    bmen = []
    country = []
    mins_crease = []
    runs = []
    balls_faced = []
    fours_hit = []
    sixes_hit=[]
    strike_rate = []
    innings = []
    opposition = []
    ground = []
    startdate = []
    content = lxml.html.parse(page)
    bats = content.xpath('//tr[@class="data1"]/td[1]/a')
    ct = content.xpath('//tr[@class="data1"]/td[1]/*')
    run = content.xpath('//tr[@class="data1"]/td[2]')
    mins = content.xpath('//tr[@class="data1"]/td[3]')
    bfs = content.xpath('//tr[@class="data1"]/td[4]')
    fours = content.xpath('//tr[@class="data1"]/td[5]')
    sixes = content.xpath('//tr[@class="data1"]/td[6]')
    strike = content.xpath('//tr[@class="data1"]/td[7]')
    inns = content.xpath('//tr[@class="data1"]/td[8]')
    oppos = content.xpath('//tr[@class="data1"]/td[10]/a')
    grou = content.xpath('//tr[@class="data1"]/td[11]/a')
    std = content.xpath('//tr[@class="data1"]/td[12]/b')
    batsmen = [bat.text for bat in bats]
    cou = [c.tail for c in ct]
    rus = [r.text for r in run]
    mints = [mint.text for mint in mins]
    bf = [bfaced.text for bfaced in bfs]
    four = [fs.text for fs in fours]
    six = [s.text for s in sixes]
    sr = [srt.text for srt in strike]
    inngs = [inn.text for inn in inns]
    opps = [opp.text for opp in oppos]
    grnd = [gr.text for gr in grou]
    sdate = [sd.text for sd in std]
    bmen.extend(batsmen)
    country.extend(cou)
    mins_crease.extend(mints)
    runs.extend(rus)
    balls_faced.extend(bf)
    fours_hit.extend(four)
    sixes_hit.extend(six)
    strike_rate.extend(sr)
    innings.extend(inngs)
    opposition.extend(opps)
    ground.extend(grnd)
    startdate.extend(sdate)
    zipped = zip(bmen,country,mins_crease,runs,balls_faced,fours_hit,sixes_hit,strike_rate,innings,opposition,ground,startdate)
    for row in zipped:
        out.writerow(row)
        zipped = None
