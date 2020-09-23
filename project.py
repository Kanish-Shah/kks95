from bs4 import BeautifulSoup
import re
import time
import requests


def run(url):

    fw=open('watson.txt','w') # output file
	
    for p in range(0,3815,5): # for each page 

        print ('page',p)
        html=None
            
        if p==0: pageLink=url # url for page 1
        else: pageLink=url.replace('.html', '-or'+str(p)+'.html') # make the page url
        
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs 
				
		
        if not html:continue # couldnt get the page, ignore
        
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 

        reviews=soup.findAll('div', {'class':re.compile('location-review-review-list-parts-SingleReview__mainCol--1hApa')}) # get all the review divs

        for review in reviews: 

            text,rating='NA','NA' # initialize critic,rating,source,text and date

            textChunk=review.find('q',{'class':'location-review-review-list-parts-ExpandableReview__reviewText--gOmRC'})
            if textChunk: text=textChunk.text.strip()
            
            ratingChunk=review.find(class_ = "ui_bubble_rating")['class']
            if 'bubble_10' in ratingChunk:
                rating = '0'
            elif 'bubble_20' in ratingChunk:
                rating = '0'
            elif 'bubble_30' in ratingChunk:
                rating = '1'
            elif 'bubble_40' in ratingChunk:
                rating = '1'
            elif 'bubble_50' in ratingChunk:
                rating = '1'
            
            fw.write(text+'\t'+rating+'\n') # write to file
		
        

    fw.close()



if __name__=='__main__':
    url='https://www.tripadvisor.com/Hotel_Review-g60763-d93344-Reviews-The_Watson_Hotel-New_York_City_New_York.html#REVIEWS'
    run(url)


