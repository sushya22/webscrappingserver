from flask import Flask,request,jsonify,render_template
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app=Flask(__name__)

@app.route("/",methods=['GET'])
@app.route("/home",methods=['GET'])
#@cross_origin()
def home():
    return "WELCOME USER"

@app.route("/review/<string:product>",methods=['GET','POST'])
#@cross_origin()
def review(product):
    if request.method=='GET':
        try:
            
            print(product)
            searchproduct = product.replace(" ","")
            flipkart_url="https://www.flipkart.com/search?q="+searchproduct
            uclient=uReq(flipkart_url)
            flipkartpage=uclient.read()
            uclient.close()
            flipkarthtml=bs(flipkartpage,"html.parser")
            flipkartitems=flipkarthtml.findAll("div",{"class":"_4ddWXP"})
            result=[]
            for item in flipkartitems[0:10]:
                a_elements=item.find_all('a')
                div_elements=item.find_all('div')
                d={
        "product_name":item.find_all('a')[1].text,
        "product_price":item.find_all('div',{"class":"_30jeq3"})[0].text,
        "product_order":"https://www.flipkart.com"+item.a['href']
                  }
                result.append(d)
        except:
            result="Error"            
        finally:
            return jsonify(result)
        
@app.route("/amazon/<string:product>",methods=['GET','POST'])
#@cross_origin()
def amazonreview(product):
    if request.method=='GET':
        try:
            searchproduct=product.replace(" ","")
            amazon_url="https://www.amazon.in/s?k="+searchproduct
            HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/90.0.4430.212 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
            data=requests.get(amazon_url,headers=HEADERS)
            amazon_page=data.text
            amazon_html=bs(amazon_page,'html.parser')
            amazon_items=amazon_html.findAll('div',{"class":"sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20"})
            result=[]
            for item in amazon_items:
                try:
                    d={
                        "product_name":item.div.div.div.div.div.find_all('h2')[0].a.span.text,
                        "product_price":item.div.div.div.div.div.div.find_all('div')[2].find_all('div',{"class":"a-section a-spacing-none a-spacing-top-small s-price-instructions-style"})[0].span.span.text,
                        "product_order":"https://www.amazon.in/"+item.div.div.div.div.div.find_all('h2')[0].a['href']
                    }
                    result.append(d)
                except:
                    d={

                    }
        except:
            result="error"
        finally:
            return jsonify(result)
           





        
if __name__=='__main__':
    app.run()
                

    
   




    

        
            

        


