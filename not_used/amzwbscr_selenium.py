
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import os


# using the product ID to create url
def scrape_amz(product_id, pages = 5):

    #start webdriver
    absolute_path = os.path.abspath("../chromedriver")
    driver = webdriver.Chrome(absolute_path)

    #defining the url for the first page
    page_no = 1
    url = f"https://www.amazon.com/en/product-reviews/{product_id}/ref=cm_cr_dp_d_paging_btm_next_{page_no}?ie=UTF8&reviewerType=all_reviews&pageNumber={page_no}"

    #create the lists for the data
    reviews = []
    review_metas = []

    pages = pages

    #counting no of pages, can be used for pages =
    #driver.get(url)
    #soup = BeautifulSoup(driver.page_source, "html.parser")
    #review_count = soup.find("div", class_= "a-row a-spacing-base a-size-base").text
    #review_no = review_count.replace("\n", "").replace(" ","").replace(",","")
    #max_len_rno = min([13, len(review_no)])
    #review_no = review_no[:-max_len_rno].split("|")[1]
    #review_no = float(review_no)
    #pages_counted = round(review_no/10) -1
    #print(f"total pages would be {pages_counted} but we only look at {pages}")


    #go to every page
    for i in range(1, pages+1):

        #get the soup of each page
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        review_parent = soup.find_all("div", class_ = "a-row a-spacing-small review-data")

        #get each review text
        for i in review_parent:
            #review = review_parent.find("span", class_ = "cr-original-review-content")
            reviews.append(i.text.replace("\n",""))

        #get each review meta
        review_meta = soup.find_all("span",
                                   {"data-hook":True},
                                   class_="a-size-base a-color-secondary review-date")
        for i in review_meta:
            helper = i.text[12:]
            review_metas.append(helper.split(" on "))

        print(f"page {page_no} of {pages} scraped")

        #update url for next page
        page_no += 1
        url = f"https://www.amazon.com/product-reviews/{product_id}/ref=cm_cr_dp_d_paging_btm_next_{page_no}?ie=UTF8&reviewerType=all_reviews&pageNumber={page_no}"


    #create df
    metas_df = pd.DataFrame(review_metas)
    metas_df[1] = pd.to_datetime(metas_df[1])
    texts_df = pd.DataFrame(reviews)
    df = pd.DataFrame()
    #df["country"] = metas_df[0]
    df["date"] = metas_df[1]
    df["text"] = texts_df

    return df
