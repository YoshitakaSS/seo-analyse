import urllib.request, urllib.error
import requests
import pandas as pd # csv用のライブラリ
from bs4 import BeautifulSoup
import re # 正規表現用のライブラリ

################
# SEO分析
################

# Google検索上位1ページの情報を取得する
inputWord = input("検索したいワードを入力: ");

# カラムの用意
columns = ["TopTitle", "Link", "Description", "Keywords", "H1", "H2"];
df = pd.DataFrame(columns=columns);


# url: 検索結果上位のURL
def getSeoParts(url):

	pattren = r'^https://|http://'

	# 検索するURLが正しいURLかをチェックする
	urlcheck = re.match(pattren, url);

	seoParts = [];
	if urlcheck:
		res = requests.get(url);

		soup = BeautifulSoup(res.text, "html.parser");

		##############
		# SEOでは、description,keyword,title,h1,h2,h3
		# そのため、それらを取得する
		##############

		headers = soup.find("head");
		if headers is not None:
			# descriptionの取得
			description = headers.find('meta', attrs={"name" : "description"});
			description = description.attrs['content'] if description is not  None else '';
			
			# keywords取得
			keywords = headers.find('meta', attrs={"name" : "keywords"});
			keywords = keywords.attrs['content'] if keywords is not None else '';

			print("Description: " + str(description));
			print("Keywords: " + str(keywords));
		
		h1 = soup.find('h1');
		h1 = str(h1.string) if h1 is not None else '';
		h2 = soup.find('h2');
		h2 = str(h2.string) if h2 is not None else '';

		print("H1: " + h1);
		print("H2: " + h2);
		print('######################################'); 

		seoParts = {
			'description' : description,
			'keywords' : keywords,
			'h1' : h1,
			'h2' : h2,
		};

		return seoParts;

	else:
		print("Error occur Invalid url: " + url);


def query_string_remove(url):
	return url[:url.find('&')];



if inputWord is not "":

	rootUrl = "https://www.google.co.jp/search?q=";

	param = "&oq=";

	paramSecure = "&sourceid=chrome&ie=UTF-8";

	# 検索URLを取得
	accessUrl = rootUrl + str(inputWord) + param + str(inputWord) + paramSecure;

	res = requests.get(accessUrl);

	soup = BeautifulSoup(res.text, "html.parser");

	searchContent = soup.find_all(class_="g");
	
	for content in searchContent:
		# h3タグに検索結果のタイトル、URLがあるため取得
		h3 = content.find('h3');
		if h3 is not None:
			# googleの検索結果のwebページタイトルを取得
			title = h3.find('a').getText();
			
			# 余計なクエリを削除する
			link =query_string_remove(h3.find('a').get('href').replace("/url?q=", ""));

			# ログ用に出力
			print("Title: " + title)
			print("Link: " + link);

			# SEO（metaタグ）の中身を取得
			seo = getSeoParts(link);

			# seoの取得がうまくいかなかった場合は処理をスキップ
			if seo is not None:

				# CSVに落とし込む
				csv = pd.Series([title, link, seo['description'], seo['keywords'], seo['h1'], seo['h2']], columns);
				df = df.append(csv, columns);
				df.to_csv("analyzeSEO.csv", encoding="shift_jis");
			else:
				continue;
else:
	print("検索ワードを入力してください");

