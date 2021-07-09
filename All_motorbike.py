from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import xlsxwriter
import string
import time

###########################################################################################
#SUSUKI####################################################################################
###########################################################################################

url = 'https://bikes.suzuki.co.uk/bikes/'
uClient = uReq(url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
containers = page_soup.findAll("div",{"class":"vehicle-card"})

SWorkbook = xlsxwriter.Workbook("Susuki.xlsx")
Ssheet = SWorkbook.add_worksheet()
Ssheet.write("A1","Bike_Name")
Ssheet.write("B1","Bike_Price")

Sbike_name = []
Sbike_price = []
for container in containers:
	my_string  = container.a.h2.span
	my_string = str(my_string)
	stringnew = re.search(">(.+?)<",my_string)
	if stringnew:
		found = stringnew.group(1)
	bike_name = found

	my_string2 = container.a.h2
	my_string2 = str(my_string2)
	stringnew2 = re.search("£(.+?)<",my_string2)
	if stringnew2:
		found2 = stringnew2.group(1)
	bike_price = found2
	
	Sbike_name.append(bike_name)
	Sbike_price.append(bike_price)

for item in range(len(Sbike_name)):
	Ssheet.write(item + 1 , 0, Sbike_name[item])
	Ssheet.write(item + 1 , 1, Sbike_price[item])
SWorkbook.close()

###########################################################################################
#YAMAHA####################################################################################
###########################################################################################

YWorkbook = xlsxwriter.Workbook("Yamaha.xlsx")
Ysheet = YWorkbook.add_worksheet()
Ysheet.write("A1","Bike_Name")
Ysheet.write("B1","Bike_Price")
pages = ["supersport/","hyper-naked/","sport-touring/","sport-heritage/","adventure/"]
Ybikes = []
Yprices = []
for page in pages:
	Yurl = 'https://www.yamaha-motor.eu/gb/en/products/motorcycles/'
	YuClient = uReq(Yurl + str(page))
	Ypage_html = YuClient.read()
	YuClient.close()

	#html parsing
	Ypage_soup = soup(Ypage_html, "html.parser")

	Ycontainers = Ypage_soup.findAll("div",{"class":"blockgrid__item-image"})
	YPcontainers = Ypage_soup.findAll("a",{"class":"blockgrid__item-link"})
	
	for Ycontainer in Ycontainers:
		Ybike_name = Ycontainer.img["alt"]
		Ybikes.append(Ybike_name)

	for YPcontainer in YPcontainers:
		New_loc = YPcontainer["href"]
		Yurl = ("https://www.yamaha-motor.eu/" + New_loc )
		YuClient = uReq(Yurl)
		Ypage_html = YuClient.read()
		YuClient.close()
		Ypage_soup = soup(Ypage_html, "html.parser")
		YP2containers = Ypage_soup.findAll("h3",{"class":"price"})
		Ystring = YP2containers
		Ystring = str(Ystring)
		Ystringnew = re.search(">(.+?)<",Ystring)
		if Ystringnew:
			Yfound = Ystringnew.group(1)
		Ybike_price = Yfound
		Yprices.append(Ybike_price)

for item in range(len(Ybikes)):
	Ysheet.write(item + 1 , 0, Ybikes[item])
	Ysheet.write(item + 1 , 1, Yprices[item])
YWorkbook.close()

###########################################################################################
#KTM#######################################################################################
###########################################################################################

KWorkbook = xlsxwriter.Workbook("KTM.xlsx")
Ksheet = KWorkbook.add_worksheet()
Ksheet.write("A1","Bike_Name")
Ksheet.write("B1","Bike_Price")

Kurl = 'https://www.ktm.com/en-gb.html'
KuClient = uReq(Kurl)
Kpage_html = KuClient.read()
KuClient.close()
Kpage_soup = soup(Kpage_html, "html.parser")
Kcontainers = Kpage_soup.findAll("ul",{"class":"bike-list"})
Kbikes = []
Kprices = []

def Kname(numb):
	global Kcontainers 
	global kprices
	global Kbikes
	test = Kcontainers[numb]
	for link in test.findAll("a"):
		Klocation = (link.get("href"))
		change = link
		change = str(change)
		Kstringnew4 = re.search(">(.+?)<",change)
		if Kstringnew4:
			Kfound4 = Kstringnew4.group(1)
		Kbike_name = Kfound4
		Kbikes.append(Kbike_name)
		
		Kurl2 = "https://www.ktm.com/"
		KuClient2 = uReq(Kurl2 + str(Klocation))
		Kpage_html2 = KuClient2.read()
		KuClient2.close()
		Kpage_soup2 = soup(Kpage_html2, "html.parser")
		Kcontainers2 = Kpage_soup2.findAll("div",{"class":"models__price-rates"})
		Kstring = Kcontainers2
		Kstring = str(Kstring)
		Kstringnew2 = re.search(">(.+?)<",Kstring)
		if Kstringnew2:
			Kfound2 = Kstringnew2.group(1)
		Kfound2= str(Kfound2)
		Kstringnew3 = re.search(":(.+?)G",Kfound2)
		if Kstringnew3:
			Kfound3 = Kstringnew3.group(1)
		Kprice2 = Kfound3
		Kprice = Kprice2
		Kprices.append(Kprice)
Kname(7)
Kname(8)
Kname(9)
Kname(10)
Kname(11)
rangew = len(Kbikes)
rangew = int(rangew)
for item in range(rangew):
	Ksheet.write(item + 1 , 0, Kbikes[item])
	Ksheet.write(item + 1 , 1, Kprices[item])
KWorkbook.close()

###########################################################################################
#BMW#######################################################################################
###########################################################################################

Bbikes = []
Bprices = []
BWorkbook = xlsxwriter.Workbook("BMW.xlsx")
Bsheet = BWorkbook.add_worksheet()
Bsheet.write("A1","Bike_Name")
Bsheet.write("B1","Bike_Price")
Burl = 'https://www.bmw-motorrad.co.uk/en/models/modeloverview.html'
BuClient = uReq(Burl)
Bpage_html = BuClient.read()
BuClient.close()
Bpage_soup = soup(Bpage_html, "html.parser")
Bcontainers = Bpage_soup.findAll("div",{"class":"wall__item-headline"})
Bcontainers4 = Bpage_soup.findAll("a",{"class":"wall__item-btn hidden mnm-tracking-link mnm-tracking-link-label"})
for Bcontain in Bcontainers:
	Bsting = Bcontain
	Bsting= str(Bsting)
	Bstringnew = re.search(">(.+?)<",Bsting)
	if Bsting:
		Bfound = Bstringnew.group(1)
	Bbike = Bfound.replace(" ","",1)
	Bbikes.append(Bbike)
for Bcontain4 in Bcontainers4:
	Bstring4 = Bcontain4["href"]
	Burl2 = "https://www.bmw-motorrad.co.uk"
	if Bstring4 != "/en/models/adventure/f900xr.html":
		BuClient2 = uReq(Burl2 + str(Bstring4))
		Bpage_html2 = BuClient2.read()
		BuClient2.close()
		Bpage_soup2 = soup(Bpage_html2, "html.parser")
		Bcontainers3 = Bpage_soup2.findAll("p",{"class":"pricing"})
		for Bcontain2 in Bcontainers3:
			Bcontain2 = str(Bcontain2)
			Bstringnew3 = re.search(">(.+?)<",Bcontain2)
			if Bcontain2:
				Bprice = Bstringnew3.group(1)
			Bprices.append(Bprice)
	else:
		pass
Bbikess = list(filter(('F900 XR').__ne__, Bbikes))
Brangew = len(Bbikess)
Brangew = int(Brangew)
for item in range(Brangew):
	Bsheet.write(item + 1 , 0, Bbikess[item])
	Bsheet.write(item + 1 , 1, Bprices[item])
BWorkbook.close()

###########################################################################################
#MV_AGUSTA#################################################################################
###########################################################################################
from urllib.request import Request, urlopen

MWorkbook = xlsxwriter.Workbook("MV AGUSTA.xlsx")
Msheet = MWorkbook.add_worksheet()
Msheet.write("A1","Bike_Name")
Msheet.write("B1","Bike_Price")
Mbike = []
Mprice = []
req = Request('https://www.mvagusta.com', headers={'User-Agent': 'XYZ/3.0'})
webpage = urlopen(req, timeout=10).read()
page_soup = soup(webpage, "html.parser")
containers = page_soup.findAll("div",{"class":"product-menu__name product-menu__name_column"})
containers2 = page_soup.findAll("a",{"class":"product-menu__name"})
for contain2 in containers2:
	Mstring4 = contain2["href"]
	if "product" in Mstring4:
		Mstring4 = str(Mstring4)
		Mstring3 = Mstring4.replace("/product/","")
		Mstring2 = Mstring3.replace("/"," ")
		Mbike.append(Mstring2)
containers3 = page_soup.findAll("div",{"class":"product-card__price"})
for contain in containers3:
	contain = str(contain)
	Mstring_new = re.search(">(.+?)<",contain)
	if contain:
		Mprices = Mstring_new.group(1)
	Mprice.append(Mprices)

Mrangew = len(Mbike)
Mrangew = int(Mrangew)
for item in range(Mrangew):
	Msheet.write(item + 1 , 0, Mbike[item])
	Msheet.write(item + 1 , 1, Mprice[item])
MWorkbook.close()

###########################################################################################
#DUCATI####################################################################################
###########################################################################################


Prices_list = []
Bikes_list = []
DWorkbook = xlsxwriter.Workbook("Ducati.xlsx")
Dsheet = DWorkbook.add_worksheet()
Dsheet.write("A1","Bike_Name")
Dsheet.write("B1","Bike_Price")
path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://configurator.ducati.com/bikes/gb/en/?_ga=2.40522530.127932919.1616703970-1651249536.1584812462")
page = soup(driver.page_source, "html.parser")
Dcontainers = page.findAll("div",{"class":"dmh-card__title"})
for Dcontain in Dcontainers:
	my_string = Dcontain
	my_string = str(my_string)
	stringnew = re.search(">(.+?)<",my_string)
	if stringnew:
		bike = stringnew.group(1)
	bike = bike.lower()
	path2 = "C:\Program Files (x86)\chromedriver.exe"
	driver2 = webdriver.Chrome(path2)
	driver2.get("https://configurator.ducati.com/bikes/gb/en/" + bike)
	page2 = soup(driver2.page_source, "html.parser")
	Dcontainers2 = page2.findAll("div",{"class":"dmh-card__title"})
	DcontainersP = page2.findAll("div",{"class":"dmh-model-card__price"})
	for Dcontain2 in Dcontainers2:
		my_string2 = Dcontain2
		my_string2 = str(my_string2)
		stringnew2 = re.search(">(.+?)<",my_string2)
		if stringnew2:
			bikes = stringnew2.group(1)
		Bikes_list.append(bikes)

	for DcontainP in DcontainersP:
		my_stringP = DcontainP
		my_stringP = str(my_stringP)
		stringnewP = re.search(">(.+?)<",my_stringP)
		if stringnewP:
			Prices = stringnewP.group(1)
		Prices_list.append(Prices)
	driver2.close()
driver.close()

Dpath3 = "C:\Program Files (x86)\chromedriver.exe"
Ddriver3 = webdriver.Chrome(Dpath3)
Ddriver3.get("https://configurator.ducati.com/bikes/gb/en/superbike")
Dpage3 = soup(Ddriver3.page_source, "html.parser")
DcontainersG = Dpage3.findAll("div",{"class":"dmh-card__title"})
DcontainersGP = Dpage3.findAll("div",{"class":"dmh-model-card__price"})
for Dcontain3 in DcontainersG:
	my_string3 = Dcontain3
	my_string3 = str(my_string3)
	stringnew3 = re.search(">(.+?)<",my_string3)
	if stringnew3:
		DbikesG = stringnew3.group(1)
	Bikes_list.append(DbikesG)
for Dcontain4 in DcontainersGP:
	my_string4 = Dcontain4
	my_string4 = str(my_string4)
	stringnew4 = re.search(">(.+?)<",my_string4)
	if stringnew4:
		DpricesG = stringnew4.group(1)
	Prices_list.append(DpricesG)
Ddriver3.close()

x = True
DscramblersP = []
DscramblersB = []
path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://configurator.scramblerducati.com/bikes/gb/en/scrambler")
while x == True:
	page = soup(driver.page_source, "html.parser")
	containers = page.findAll("div",{"class":"models-list__model__name__text"})
	if containers != []:
		x = False
	else:
		pass
for contain in containers:
	Dstring = contain
	Dstring = str(Dstring)
	Dstringnew = re.search(">(.+?)<",Dstring)
	if Dstringnew:
		Dbike_scrambler = Dstringnew.group(1)
	DscramblersB.append(Dbike_scrambler)
	Dbike_scrambler = Dbike_scrambler.lower()
	print(Dbike_scrambler)
	Dpath_scrambler = "C:\Program Files (x86)\chromedriver.exe"
	Ddriver_scrambler = webdriver.Chrome(Dpath_scrambler)
	if Dbike_scrambler == "desert sled":
		scarmbler_use = "desert-sled"
	elif Dbike_scrambler == "nightshift":
		scarmbler_use = "icon-nightshift"
	elif Dbike_scrambler == "1100 dark pro":
		scarmbler_use = "scr11drk"
	elif Dbike_scrambler == "1100 sport pro":
		scarmbler_use = "scr11spr"
	elif Dbike_scrambler == "1100 pro":
		scarmbler_use = "scr11pro"
	elif Dbike_scrambler == "icon":
		scarmbler_use = "icon"
	elif Dbike_scrambler == "cafè racer":
		scarmbler_use = "cafe-racer"
	elif Dbike_scrambler == "full throttle":
		scarmbler_use = "full-throttle"
	elif Dbike_scrambler == "sixty2":
		scarmbler_use = "sixty2"
	elif Dbike_scrambler == "icon dark":
		scarmbler_use = "icon-dark"
	Ddriver_scrambler.get("https://configurator.scramblerducati.com/bikes/gb/en/scrambler/" + scarmbler_use)
	loop = True
	while loop == True:
		Dpage_scrambler = soup(Ddriver_scrambler.page_source, "html.parser")
		Dcontainers_scrambler = Dpage_scrambler.findAll("strong",{"class":"price-block__number"})
		if Dcontainers_scrambler != []:
			loop = False
	for contain_scrambler in Dcontainers_scrambler:
		Dstring2 = contain_scrambler
		Dstring2 = str(Dstring2)
		Dstringnew2 = re.search(">(.+?)<",Dstring2)
		if Dstringnew2:
			Dbike_scrambler_price = Dstringnew2.group(1)
		DscramblersP.append(Dbike_scrambler_price)
		

Dbikes = Bikes_list + DscramblersB
Dprices = Prices_list + DscramblersP

for item in range(len(Dbikes)):
	Dsheet.write(item + 1 , 0, Dbikes[item])
	Dsheet.write(item + 1 , 1, Dprices[item])
DWorkbook.close()

###########################################################################################
#HONDA####################################################################################
###########################################################################################

HWorkbook = xlsxwriter.Workbook("Honda.xlsx")
Hsheet = HWorkbook.add_worksheet()
Hsheet.write("A1","Bike_Name")
Hsheet.write("B1","Bike_Price")
cont = False
Hbikes = []
Hprices = []
Hurl = 'https://www.honda.co.uk/motorcycles.html'
HuClient = uReq(Hurl)
Hpage_html = HuClient.read()
HuClient.close()
Hpage_soup = soup(Hpage_html, "html.parser")
Hcontainers = Hpage_soup.findAll("span",{"class":"title"})
for Hcontain in Hcontainers:
	Hstring = Hcontain
	Hstring = str(Hstring)
	Hstringnew = re.search(">(.+?)<",Hstring)
	if Hstringnew:
		Hbike = Hstringnew.group(1)

Hurl2 = 'https://www.honda.co.uk/motorcycles.html'
HuClient2 = uReq(Hurl2)
Hpage_html2 = HuClient2.read()
HuClient2.close()
Hpage_soup2 = soup(Hpage_html2, "html.parser")
Hcontainers2 = Hpage_soup2.findAll("a",{"class":"link--secondary red-range"})
for Hcontain2 in Hcontainers2:
	link = (Hcontain2["href"])
	link = str(link)

	Hurl = 'https://www.honda.co.uk/motorcycles.html'
	HuClient = uReq(Hurl)
	Hpage_html = HuClient.read()
	HuClient.close()
	Hpage_soup = soup(Hpage_html, "html.parser")
	Hcontainers = Hpage_soup.findAll("span",{"class":"title"})
	

	if len(link) < 45 or "scooter" in link or "montesa" in link or "crf" in link or "125" in link:
		pass
	else:
		Hbike2 = link.split("/")[4]
		Hbikes.append(Hbike2)
		Huse = "https://www.honda.co.uk/" + link 
		Huse2 = Huse.split("overview",1)
		if Huse2 == Huse:
			Huse3 = Huse.split("Overview",1)
			link2 = Huse3[0]
		else:
			link2 = Huse2[0]	
		link3 = link2 + "specifications.html"
		if "nc750s-2016" in link:
			link3 = "https://www.honda.co.uk/motorcycles/range/street/nc750s-2016/specification.html#/"
		try:
			link3 = str(link3)
			HuClient3 = uReq(link3)
			Hpage_html3 = HuClient3.read()
			HuClient3.close()
			cont = True 
		except:
			Huse = "https://www.honda.co.uk/" + link 
			Huse2 = Huse.split("overview",1)
			if Huse2 == Huse:
				Huse3 = Huse.split("Overview",1)
				link2 = Huse3[0]
			else:
				link2 = Huse2[0]	
			link3 = link2 + "specifications-and-price.html"
			link3 = str(link3)
			HuClient3 = uReq(link3)
			Hpage_html3 = HuClient3.read()
			HuClient3.close()
			cont = True 
		try:
			Hpage_soup3 = soup(Hpage_html3, "html.parser")
			Hcontainers3 = Hpage_soup3.findAll("span",{"class":"fullPrice"})
			cont = True 
		except:
			Hpage_soup3 = soup(Hpage_soup3, "html.parser")
			Hcontainers3 = Hpage_soup3.findAll("span",{"class":"variant__price"})
			cont = True 
		Hcontainers3 = str(Hcontainers3)
		Hstringnew2 = re.search(">(.+?)<",Hcontainers3)
		if Hstringnew2:
			Hprice = Hstringnew2.group(1)
		Hprices.append(Hprice)

for item in range(len(Hprices)):
	Hsheet.write(item + 1 , 0, Hbikes[item])
	Hsheet.write(item + 1 , 1, Hprices[item])
HWorkbook.close()

###########################################################################################
#KAWASAKI##################################################################################
###########################################################################################

KAWorkbook = xlsxwriter.Workbook("KAWASAKI.xlsx")
KAsheet = KAWorkbook.add_worksheet()
KAsheet.write("A1","Bike_Name")
KAsheet.write("B1","Bike_Price")
KAlinks = []
KAbikes = []
KAprices = []
KAurl = "https://www.kawasaki-kalculator.co.uk/"
KAuClient = uReq(KAurl)
KApage_html = KAuClient.read()
KAuClient.close()
KApage_soup = soup(KApage_html, "html.parser")
KAcontainers = KApage_soup.findAll("option",{"class":"model-list-item"})
for KAcontain in KAcontainers:
	KAcontain = str(KAcontain)
	KAstringnew = re.search('/(.+?)"',KAcontain)
	if KAstringnew:
		KAfound = KAstringnew.group(1)
		KAlink = KAfound
		KAlink = str(KAlink)
		if "2020" in KAlink:
			KAlinks.append(KAlink)

for i in range(len(KAlinks)):
	j = i -1
	KApath = "C:\Program Files (x86)\chromedriver.exe"
	KAdriver = webdriver.Chrome(KApath)
	KAdriver.get("https://www.kawasaki-kalculator.co.uk/" + (KAlinks[j]) )
	KApage = soup(KAdriver.page_source, "html.parser")
	KAcontainers = KApage.findAll("div",{"class":"model-category-text"})
	for KAcontain in KAcontainers:
		KAmy_string = KAcontain.h3
		KAmy_string = str(KAmy_string)
		KAstringnew2 =  re.search('>(.+?)<',KAmy_string)
		if KAstringnew2:
			KAall = KAstringnew2.group(1)
			KAall2 = KAall.split("-")
			KAprice2 = (KAall2[1])
			KAprice = KAprice2.replace(" ","")
			KAbike = (KAall2[0])
			if KAbike in KAbikes:
				pass
			else:
				KAbikes.append(KAbike)
				KAprices.append(KAprice)
				
	KAdriver.close()

for item in range(len(KAbikes)):
	KAsheet.write(item + 1 , 0, KAbikes[item])
	KAsheet.write(item + 1 , 1, KAprices[item])
KAWorkbook.close()



###########################################################################################
#APRILIA###################################################################################
###########################################################################################

Abikes_final1 = []
Abikes_final2 = []
AWorkbook = xlsxwriter.Workbook("APRILIA.xlsx")
Asheet = AWorkbook.add_worksheet()
Asheet.write("A1","Bike_Name")
Asheet.write("B1","Bike_Price")
Abikes = []
Abikes_for = []
Aprices = []
Abikes_final = []
path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://www.aprilia.com/gb_EN/")
driver.set_window_position(-2000,0)
driver.execute_script("window.scrollTo(0, 5000)")
time.sleep(2)
page = soup(driver.page_source, "html.parser")
Acontainers = page.findAll("span",{"class":"card-product__name"})
for Acontain in Acontainers:
	Amy_string = Acontain
	Amy_string = str(Amy_string)
	Astringnew = re.search(">(.+?)<",Amy_string)
	if Astringnew:
		Abike = Astringnew.group(1)
	Abikes.append(Abike)
driver.close()
AbikeS = list(set(Abikes))
for i in AbikeS:
	j = i.replace(" ","-")
	Abikes_for.append(j)
Abikes_for_final = [x.lower() for x in Abikes_for]

#####################################################
for i in Abikes_for_final:
	path = "C:\Program Files (x86)\chromedriver.exe"
	driver2 = webdriver.Chrome(path)
	driver2.get("https://www.aprilia.com/gb_EN/models/" + str(i) + "/")
	time.sleep(3)
	driver2.execute_script("window.scrollTo(0, 850)")

	Apage2 = soup(driver2.page_source, "html.parser")
	Acontainers_p = Apage2.findAll("span",{"class":"card-product__price__list"})
	Alength = (len(Acontainers_p))
	for Acontain2 in Acontainers_p:
		Amy_string = Acontain2
		Amy_string = str(Amy_string)
		Astringnew = re.search(">(.+?)<",Amy_string)
		if Astringnew:
			Aprice = Astringnew.group(1)
		Aprices.append(Aprice)


	Append_to = []
	Acontainers_n = Apage2.findAll("span",{"class":"card-product__name"})
	for Acontain in Acontainers_n:
		Amy_string = Acontain
		Amy_string = str(Amy_string)
		Astringnew = re.search(">(.+?)<",Amy_string)
		if Astringnew:
			Abike = Astringnew.group(1)
		Append_to.append(Abike)
	
	if Alength == 1 :
		if i in Abikes_final1:
			del Aprices[-1]
		else:
			Abikes_final1.append(i)
	else:
		for i in range(len(Append_to)):
			i = i + 1
			if i > 8:
				j = i - 1 
				Ak = Append_to[j]
				if Ak in Abikes_final1:
					del Aprices[-1]
				else:
					Abikes_final1.append(Ak)

print(Abikes_final1)
print(Aprices)

driver2.close()
Arangew = len(Abikes_final1)
Arangew = int(Arangew)
for item in range(Arangew):
	Asheet.write(item + 1 , 0, Abikes_final1[item])
	Asheet.write(item + 1 , 1, Aprices[item])
AWorkbook.close()

















