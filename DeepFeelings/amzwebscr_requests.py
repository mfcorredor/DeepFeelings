import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def parse_page(url):
    page = requests.get(url, headers={"Accept-Language":"en-US"})
    soup = bs(page.content, 'html.parser')

    names = soup.find_all('span', class_= 'a-profile-name')
    cust_name = []
    for i in range(0, len(names)):
        cust_name.append(names[i].get_text())

    titles = soup.find_all('a', class_= 'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold')
    review_titles = []
    for i in range(0, len(titles)):
        review_titles.append(titles[i].get_text())
    review_titles[:] = [titles.strip('\n') for titles in review_titles]

    ratings = soup.find_all('i', class_= 'a-icon a-icon-star a-star-5 review-rating')
    review_ratings = []
    for i in range(0, len(ratings)):
        review_ratings.append(ratings[i].get_text())

    reviews = soup.find_all('span', {'data-hook': 'review-body'})
    review_body = []
    for i in range(0, len(reviews)):
        review_body.append(reviews[i].get_text())
    review_body[:] = [reviews.lstrip('\n') for reviews in review_body]
    review_body[:] = [reviews.rstrip('\n') for reviews in review_body]

    return cust_name,  review_titles, review_ratings, review_body


def parse_pages(start=2, end=10):
    base_url = "https://www.amazon.co.uk/product-reviews/0241411793/ref=cm_cr_getr_d_paging_btm_next_{i}?ie=UTF8&reviewerType=all_reviews&pageNumber={i}"
    cust_names, review_titles, review_ratings, review_bodies = [], [], [], []
    for i in range(start, end):
        url = base_url.format(i=i)
        cust_name,  review_title, review_rating, review_body = parse_page(url)
        cust_names += cust_name
        review_titles += review_title
        review_ratings += review_rating
        review_bodies += review_body

    return cust_names, review_titles, review_ratings, review_bodies
