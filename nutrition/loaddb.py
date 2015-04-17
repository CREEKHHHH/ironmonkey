__author__ = 'sandeep.polisetty'
import urllib,re,os
pattern=re.compile("(\(w+\))(w+)")
from BeautifulSoup import BeautifulSoup as bs
from nutrition.models  import FoodItem
fileLink=os.path.join(os.getcwd(),'nutrition\\urls.txt')
# Takes the Url.txt File as input and gets Url for categories as generator Function
def get_url():
    def urlgen(line):
        url,pg=line.split()
        pg=int(pg)
        yield url
        if(pg>=1):
            for i in range(1,pg-1):
                yield url+"-"+str(i)
    with open(fileLink) as fp:
        for line in fp:
            yield urlgen(line)
def getFloat(element):
    if bool(element):
        return float(element)
    return float(0.0)    

#Takes input of get_url
def getFoodItemNutritionPage(pageUrl):
    page=urllib.urlopen(pageUrl)
    pageSoup=bs(page.read())
    paginatedList=pageSoup.findAll('div','browseright')[0].findAll('li')
    def getDictOfNameMfgDesc(pText):
        sp1=pText.split('-')
        d=getDictOfNameMfg(sp1[0])
        if(len(sp1)==1):
            d['desc']=None
        else:
            d['desc']=sp1[1]
        return d

    def getDictOfNameMfg(text):
        a=text.split(')')
        d={}
        if(len(a)==1):
            d['mfg']=None
            d['name']=a[0]
        else:
            d['mfg']=a[0].replace("(","")
            d['name']=a[1]
        return d

    for pageContainer in paginatedList:
        pText=pageContainer.getText()
        pdictionary=getDictOfNameMfgDesc(pText)
        aLinks=pageContainer.findAll('a')
        if(len(aLinks)==2):
            url=aLinks[1]['href']
        else:
            url=aLinks[0]['href']
        pdictionary['url']=url
        yield pdictionary
def getDictionaryOfAllNutritionalData(temDic):
    #url="http://www.caloriecount.com/calories-loven-fresh-bread-i299967"
    url=temDic['url']
    response=urllib.urlopen(url)
    sp=bs(response.read())
    ntlabel=sp.findAll('div','nutrition-label')
    foodPhoto=sp.find('div','food-photo')
    dic={}
    print url
    if(ntlabel[0].find("span","miniCarb-orig")!=None): dic['carb']=getFloat(ntlabel[0].find("span","miniCarb-orig").getText())
    if(ntlabel[0].find("span","miniSugar-orig")!=None): dic['sugar']=getFloat(ntlabel[0].find("span","miniSugar-orig").getText())
    if(ntlabel[0].find("span","miniProtein-orig")!=None): dic['protein']=getFloat(ntlabel[0].find("span","miniProtein-orig").getText())
    if(ntlabel[0].find("span","miniFat-orig")!=None): dic['fat']=getFloat(ntlabel[0].find("span","miniFat-orig").getText())
    if(ntlabel[0].find("span","miniCal-orig")!=None): dic['calories']=getFloat(ntlabel[0].find("span","miniCal-orig").getText())
    if(ntlabel[0].find("div").find("span","miniAmt")!=None):dic['servSizeNum']=ntlabel[0].find("div").find("span","miniAmt").getText()
    if(ntlabel[0].find("div").find("span","miniDesc")!=None):dic['servSizeDesc']=(ntlabel[0].find("div").find("span","miniDesc").getText())
    if(ntlabel[0].find("div").find("span","miniGram")!=None):dic['servSizeGram']=getFloat(ntlabel[0].find("div").find("span","miniGram").getText())
    if(foodPhoto!=None):dic['imgUrl']=str(foodPhoto.find('img')['src'])
    dic['name']=temDic['name']
    dic['mfg']=temDic['mfg']
    dic['desc']=temDic['desc']
    dic['url']=temDic['url']
    return dic

def loadObject(data):
    mod=FoodItem()
    mod.itemName=data['name']
    mod.mfgName=data['mfg']
    mod.itemDescription=data['desc']
    mod.url=data['url']
    if(data.has_key('imgUrl')):mod.imgUrl=data['imgUrl']
    mod.totalCal=data['calories']
    mod.carb=data['carb']
    mod.fat=data['fat']
    mod.sugar=data['sugar']
    mod.protein=data['protein']
    mod.servingDesc=data['servSizeDesc']
    mod.servingSize=data['servSizeNum']
    mod.servingGram=data['servSizeGram']
    mod.save()


def update_db():
    for mother_url in get_url():
        for page_url in mother_url:
            for nutritionPage in getFoodItemNutritionPage(page_url):
                loadObject(getDictionaryOfAllNutritionalData(nutritionPage))
            #loadObject(getDictionaryOfAllNutritionalData(getFoodItemNutritionPage(page_url)))

