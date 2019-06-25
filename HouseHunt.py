# -*- coding: utf-8 -*-

import requests
import time
import ZillowService as zl
import pandas as pd
from bs4 import BeautifulSoup
import json




MAPQUEST_KEY=""
driver=""
WORKING_PLACE = ""  # Use for calculating commuting cost
LIST_PAGES =21  # pages of list of house will be captured
SLEEP_TIME =4


def getListAndSaveToFiles():
    #
    for pageNumber in range(1,LIST_PAGES):
        # ROOTURL Changes based on the need
        ROOTURL = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22mapBounds%22%3A%7B%22west%22%3A-77.4733463314796%2C%22east%22%3A-77.05998573577648%2C%22south%22%3A38.93444846452984%2C%22north%22%3A39.388585897241214%7D%2C%22mapZoom%22%3A11%2C%22savedSearchEnrollmentId%22%3A%22X1-SSseqdhlxosil10000000000_aovso%22%2C%22isMapVisible%22%3Atrue%2C%22customRegionId%22%3A%22f293b5ced9X1-CR1akrq7ku4664e_uigbv%22%2C%22filterState%22%3A%7B%22sortSelection%22%3A%7B%22value%22%3A%22days%22%7D%2C%22price%22%3A%7B%22min%22%3A400000%2C%22max%22%3A500000%7D%2C%22monthlyPayment%22%3A%7B%22min%22%3A1560%2C%22max%22%3A1950%7D%2C%22beds%22%3A%7B%22min%22%3A3%7D%2C%22isMultiFamily%22%3A%7B%22value%22%3Afalse%7D%2C%22isCondo%22%3A%7B%22value%22%3Afalse%7D%2C%22isManufactured%22%3A%7B%22value%22%3Afalse%7D%2C%22isLotLand%22%3A%7B%22value%22%3Afalse%7D%2C%22enableSchools%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22pagination%22%3A%7B%22currentPage%22%3A" + str(
            pageNumber) + "%7D%7D&includeMap=false&includeList=true"

        zl.navigate_to_website(driver, ROOTURL)
        # Save
        zl.saveSourceToFile("list_"+str(pageNumber), driver.page_source.encode("utf-8"))
        time.sleep(SLEEP_TIME)

def getDetailsAndSaveToFiles(link,zpid):
    output = []
    zl.navigate_to_website(driver, link)
    zl.saveSourceToFile(str(zpid), driver.page_source.encode("utf-8"))
    time.sleep(SLEEP_TIME)

def listPaser(fileName):
    list_page_Data=""
    with open(fileName, "r") as text_file:
        list_page_Data=text_file.read().encode("utf-8")
    soup = BeautifulSoup(list_page_Data)
    list_page_Data = json.loads(soup.get_text())
    houses = []
    for house in list_page_Data["searchResults"]["listResults"]:
        houses_d = []
        houses_d.append(house["addressWithZip"])  # address
        houses_d.append(house["statusText"])
        houses_d.append(house["detailUrl"])
        houses_d.append(str(house["price"]).replace("$","").replace(",","").replace("+",""))
        houses_d.append(house["zpid"])
        houses_d.append(house["beds"])
        houses_d.append(house["baths"])
        houses_d.append(house["area"])
        houses_d.append(house["latLong"]["latitude"])
        houses_d.append(house["latLong"]["longitude"])
        houses_d.append(house["hdpData"]["homeInfo"]["city"])
        houses_d.append(house["hdpData"]["homeInfo"]["yearBuilt"])
        houses_d.append(house["hdpData"]["homeInfo"]["daysOnZillow"])
        if( "zestimate" in house["hdpData"]["homeInfo"]):
            houses_d.append(house["hdpData"]["homeInfo"]["zestimate"])
        else:
            houses_d.append("null")
        if("rentZestimate" in house["hdpData"]["homeInfo"]):
            houses_d.append(house["hdpData"]["homeInfo"]["rentZestimate"])
        else:
            houses_d.append("null")
        houses_d.append(house["hdpData"]["homeInfo"]["hiResImageLink"])
        houses_d.append(house["hdpData"]["homeInfo"]["homeType"])
        houses.append(houses_d)
    return houses


def detailsPaser(fileName,zpid,school_dic):

    output=[]
    detail_page_Data=""
    with open(fileName, "r") as text_file:
        detail_page_Data = text_file.read()
    try:
        soup_d = BeautifulSoup(detail_page_Data)
        detail_page_Data = json.loads(soup_d.find('script', id='hdpApolloPreloadedData').text)
        detail_page_Data = json.loads(detail_page_Data["apiCache"])
        for i in range(0, 3):
            school1=[]
            flag = False
            if detail_page_Data.has_key("OffMarketSEORenderQuery{\"zpid\":" + str(zpid) + "}"):
                school1 = detail_page_Data["OffMarketSEORenderQuery{\"zpid\":" + str(zpid) + "}"][
                    "property"][
                    "schools"][i]
                flag = True
            if detail_page_Data.has_key("ForRentDoubleScrollInitialRenderSEOQuery{\"zpid\":" + str(zpid) + "}"):
                school1 = detail_page_Data["ForRentDoubleScrollInitialRenderSEOQuery{\"zpid\":" + str(zpid) + "}"][
                    "property"][
                    "schools"][i]
                flag = True
            if detail_page_Data.has_key("ForSaleDoubleScrollInitialRenderSEOQuery{\"zpid\":" + str(zpid) + "}"):
                school1 = detail_page_Data["ForSaleDoubleScrollInitialRenderSEOQuery{\"zpid\":" + str(zpid) + "}"][
                    "property"][
                    "schools"][i]
                flag = True
            if detail_page_Data.has_key("NewConstructionDoubleScrollInitialRenderSEOQuery{\"zpid\":" + str(zpid) + "}"):
                school1 = detail_page_Data["NewConstructionDoubleScrollInitialRenderSEOQuery{\"zpid\":" + str(zpid) + "}"][
                    "property"][
                    "schools"][i]
                flag = True

            if flag:
                output.append(school1["name"])
                if(school_dic.has_key(school1["name"])):
                    output.append(school_dic[school1["name"]])
                else:
                    output.append(999)
                output.append(school1["rating"])
                output.append(school1["level"])
                output.append(school1["link"])
                output.append(school1["size"])
            else:
                for key, value in detail_page_Data.items():
                    print key
    except:
        print "This is an error in detailsPaser :" +fileName
        output = ""

    return output


def getSchoolRankfromNICHEandSaveToFile():
    count = 0
    for level in ["middle","elementary","high"]:
        for pageIndex in range(1,21):
            count = count + 1
            time.sleep(2)
            link ="https://www.niche.com/api/renaissance/results/?state=maryland&gradeLevel="+level+"&listURL=best-schools&page="+str(pageIndex)+"&searchType=school"
            zl.navigate_to_website(driver, link)
            zl.saveSourceToFile("school_rank"+str(count), driver.page_source.encode("utf-8"))


def parserSchoolRank():
    school_dic = {}
    for pageIndex in range(1, 61):
        with open("school_rank"+str(pageIndex)+".txt", "r") as text_file:
            page_source = text_file.read()
        soup = BeautifulSoup(page_source)
        data = json.loads(soup.text)
        for i in range(0, len(data["entities"])):
            if data["entities"][i].has_key("badge"):
                order = data["entities"][i]["badge"]["ordinal"]
                school_name = data["entities"][i]["content"]["entity"]["name"]
                school_dic[school_name] = order
    return  school_dic



def close():
    zl.close_connection(driver)



def saveToCVS(output_data):
    # Write data to data frame, then to CSV file.
    file_name = "%s_%s.csv" % (str(time.strftime("%Y-%m-%d")),
                               str(time.strftime("%H%M%S")))
    columns =["addressWithZip","statusText","detailUrl","price","zpid","beds","baths","area","latitude","longitude","city","yearBuilt","daysOnZillow","zestimate","rentZestimate","hiResImageLink","homeType","school name","rating","rating","level","link","size","school name","rating","rating","level","link","size","school name","rating","rating","level","link","size","distance","travel_time"]
    pd.DataFrame(output_data, columns = columns).drop_duplicates().to_csv(
        file_name, index=False, encoding="UTF-8"
    )


def distanceCalculator(start_from,target_to):

    baseURL ="https://www.mapquestapi.com/directions/v2/route?key="+MAPQUEST_KEY+"&from="+start_from+"&to="+target_to+"0&outFormat=json&ambiguities=ignore&routeType=fastest&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false"
    response = requests.get(baseURL)
    return response.json()



if __name__ == '__main__':

    # Step 1:  Get list of houses and save to files
    # Step 2:  Parse the step1's saved file to get house url, get house details by go through the house URL
    # Step 3:  Get extra School Ranking info and save to files
    # Step 4:  Parse house info and add extra school ranking info and commute cost into house details
    # Step 5:  Save into excel file

    # Initialize the webdriver.
    driver = zl.init_firefox_driver("/Users/cheny39/Documents/tools/geckodriver")

    # save list data into file
    #getListAndSaveToFiles()

    # parser list data
    for i in range(11,21):
        print "list_"+str(i)+" under processing"
        houses = listPaser("list_"+str(i)+".txt")
        # save details data into file
        for house in houses:
            getDetailsAndSaveToFiles(house[2],house[4])


    # get school rank

    getSchoolRankfromNICHEandSaveToFile()

    school_ranking =parserSchoolRank()

    # get all houses
    output = []
    for i in range(1,21):
        try:
            houses = listPaser("list_"+str(i)+".txt")
            for house in houses:
                print str(house[4])+".txt"
                schools = detailsPaser(str(house[4])+".txt",house[4],school_ranking)
                if schools!="":
                    for school in schools:
                        house.append(school)
                    distance_matrix = distanceCalculator(house[0], WORKING_PLACE)
                    # calculate distance
                    if distance_matrix["route"].has_key("distance") and distance_matrix["route"].has_key("realTime"):
                        house.append(distance_matrix["route"]["distance"])
                        house.append(distance_matrix["route"]["realTime"])
                    output.append(house)
                    print  len(output)
        except:
            print "Error : house's in list " + str(i) + " " + str(len(houses))
            continue
    saveToCVS(output)
    # close driver
    close()
