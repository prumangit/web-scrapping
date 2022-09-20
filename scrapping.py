from importlib.resources import path
import json
import time
from attr import attrs
from selenium import webdriver;
from bs4 import BeautifulSoup;
from selenium.webdriver.common.by import By

website = "https://www.walmart.com";
path = "./chromedriver";
# searchFieldXpath = '//*[@id="twotabsearchtextbox"]';
# searchIconXpath = '//*[@id="nav-search-submit-button"]';
# paginationXpath = "//a[contains(@class, 's-pagination-next')]";
# manuXpath = "//span[starts-with(text(),'Manufacturer')]//following-sibling::span";

searchFieldXpath = '//*[@data-automation-id="header-input-search"]';
searchIconXpath = '//*[@aria-label="Search icon"]';
paginationXpath = "//*[aria-label='Next Page']";
manuXpath = "//h3[starts-with(text(),'Brand')]//following-sibling::p//span";

searchKeyword = 'curcumin dietary supplement';
appendDomainToProductLinks = True;

driver = webdriver.Chrome(path);
driver.get(website);

# soup = BeautifulSoup(content);
time.sleep(30);
search = driver.find_element(By.XPATH,searchFieldXpath)
search.send_keys(searchKeyword);

time.sleep(2);
searchIcon = driver.find_element(By.XPATH,searchIconXpath);
searchIcon.click();

time.sleep(10);
productLinks = [];
#productLinks = ["http://bit.ly/vinayakgfg"];
manufNames = [];

def getManufNames():
    for product in productLinks:
        driver.get(product);
        time.sleep(3);

        ele = driver.find_elements(By.XPATH,manuXpath);
        if len(ele) > 0:
            manuf = driver.find_element(By.XPATH,manuXpath).text;
            
            if manuf not in manufNames: 
                manufNames.append(manuf);
                file_to_delete = open("manuf.txt",'w');
                json_mylist = json.dumps(manufNames, separators=(',', ':'))
                file_to_delete.write(json_mylist)
                file_to_delete.close();



def getProductLinks():
    content =  driver.page_source;
    soup = BeautifulSoup(content);

    for product in soup.findAll("div",attrs={"class":"w-25"}):
        for link in product.findAll("a",attrs={"class":"hide-sibling-opacity"}): 
            if appendDomainToProductLinks:
                productLinks.append(link["href"]);
            else:
                productLinks.append(website+link["href"]);

    elements = driver.find_elements(By.XPATH,paginationXpath);
    size = len(elements)
    if size > 0:
        nextPage = driver.find_element(By.XPATH,paginationXpath);
        nextPage.click();
        time.sleep(5);
        getProductLinks();

    else:
        file1 = open("myfile.txt", "a")  # append mode
        json_mylist = json.dumps(productLinks, separators=(',', ':'))
        file1.write(json_mylist)
        file1.close()

getProductLinks();

getManufNames();

driver.quit();
