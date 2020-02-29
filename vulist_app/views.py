from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from .models import Product
from requests.compat import quote_plus
import requests

BASE_PIK_URL = "https://www.olx.ba/pretraga?trazilica={}"
BASE_NJUSKALO_URL = "https://www.njuskalo.hr/?ctl=search_ads&keywords={}"
BASE_ITEM_NJUSKALO = "https://www.njuskalo.hr{}"

def home(request):
	return render(request, "base.html")

@csrf_exempt
def new_page(request):
	content = request.POST.get("search")
	new_item = Product.objects.create(title = content.title)
	final_url = BASE_PIK_URL.format(quote_plus(content))
	response = requests.get(final_url)
	data = response.text
	soup = BeautifulSoup(data, features='html.parser')

	post_listings1 = soup.find('div', {'id': 'rezultatipretrage'})

	final_postings = []

	all_divs = post_listings1.find_all("div")

	for post in all_divs:
		if post.find(class_="na") != None:
			post_title1 = post.find(class_="na").text
		if post.find("a") != None:
			post_url1 = post.find('a').get('href')
			print(post_url1)
		if post.find(class_="cijena") != None:
			post_price1 = post.find(class_="cijena").find("span").text
		if post.find("img") != None:
			post_img1 = post.find("img").get("src").split("-")
			if len(post_img1) > 2:
				post_img1[4] = "default.jpg"
				post_img1 = "-".join(post_img1)
			else:
				post_img1 = "-".join(post_img1)
		if post.find(class_="pna") != None:
			post_description1 = post.find(class_="pna").text

		final_postings.append((post_title1, post_url1, post_price1,
										 post_img1, post_description1))
		final_postings = list(dict.fromkeys(final_postings))


	njusklao_url = BASE_NJUSKALO_URL.format(quote_plus(content))
	response_njuskalo = requests.get(njusklao_url)
	data_njuskalo = response_njuskalo.text
	soup_njuskalo = BeautifulSoup(data_njuskalo, features="html.parser")

	post_listings2 = soup_njuskalo.find("ul", {"class":"EntityList-items"})

	for post in post_listings2.find_all("article", {"class":"entity-body cf"}):
		if post.find(class_="entity-title") != None:
			post_title2 = post.find(class_="entity-title").text
		if post.find("a") != None:
			post_url2 = post.find("a").get("href")
			post_url2 = BASE_ITEM_NJUSKALO.format(post_url2)
			print(post_url2)
		if post.find(class_="price price--hrk") != None:
			post_price2 = post.find(class_="price price--hrk").text
		if post.find(class_="entity-description-main") != None:
			post_description2 = post.find(class_="entity-description-main").text
		if post.find("img").get("src") != None:
			post_img2 = post.find("img").get("src")

		final_postings.append((post_title2, post_url2, post_price2,
										 post_img2, post_description2))

	return render(request, "index.html", {"content": content,
										"new_item": new_item,
										"final_postings": final_postings
										})

