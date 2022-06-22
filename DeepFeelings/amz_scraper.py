import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

def get_data_amz(product_id, pages=5, verbose=True):
    '''
    Returns a Dataframe with the comments and dates of the comments of an amazon product.
        product_id (str): product id from Amazon
        pages (int): number of pages to get comments
    '''

    # start scraper
    scraper = cloudscraper.create_scraper()

    # create the lists for the data
    reviews = []
    dates = []

    # go through pages
    for i in range(1, pages+1):

        # URL to scrape
        url = f"https://www.amazon.com/en/product-reviews/{product_id}/ref=cm_cr_dp_d_paging_btm_next_{i}?ie=UTF8&reviewerType=all_reviews&pageNumber={i}"

        # get html
        soup = BeautifulSoup(scraper.get(url).text, "html.parser")

        # get reviews
        reviews_html = soup.find_all("span", attrs={"data-hook": "review-body"})
        for review in reviews_html:
            reviews.append(review.text.replace("\n",""))

        # get reviews date
        dates_html = soup.find_all("span", attrs={"data-hook": "review-date"})
        for date in dates_html:
            if '...' not in review.text.split()[-1]:
                dates.append(' '.join(date.text.split()[-3:]))
        if verbose==True:
            print(f"page {i} of {pages} scraped")

    #create df
    data = pd.DataFrame(dates, columns={'date'})
    data['date'] = pd.to_datetime(data['date'])
    data['text'] = reviews

    return data
