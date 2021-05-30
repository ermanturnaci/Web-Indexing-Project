from bs4 import BeautifulSoup
import requests
from string import punctuation
from collections import Counter
from flask import Flask, request, render_template,jsonify

app = Flask(__name__)

def islemYap(adres):
    html_text = requests.get(adres).text
    soup = BeautifulSoup(html_text,'lxml')
    kelimeler = soup.find('body').text
    noktalama= str.maketrans('','',punctuation)
    kelimeler= kelimeler.translate(noktalama)
    kelimeler= kelimeler.upper()
    kelimeler= kelimeler.split()
    print(kelimeler)
    kelime_say= Counter(kelimeler)
    print(type(kelime_say),'\n')
    return kelime_say.most_common(30)

def islemYap2(adres4,adres5):
    html_text = requests.get(adres4).text
    soup = BeautifulSoup(html_text,'lxml')
    kelimeler = soup.find('body').text
    noktalama= str.maketrans('','',punctuation)
    kelimeler= kelimeler.translate(noktalama)
    kelimeler= kelimeler.upper()
    kelimeler= kelimeler.split()
    
    html_text2 = requests.get(adres5).text
    soup2 = BeautifulSoup(html_text2,'lxml')
    kelimeler2 = soup2.find('body').text
    noktalama2= str.maketrans('','',punctuation)
    kelimeler2= kelimeler2.translate(noktalama)
    kelimeler2= kelimeler2.upper()
    kelimeler2= kelimeler2.split()
    
        
    baglaclar= ["A","AN","IN","THE","AND","TO","OF","YOU","ME","OUR","WE","WILL","BE","HE","SHE","IT","WAS","WERE","HERE","SO","AS","ON","DO","YOUR","FOR","BY","THAT","US","ONE","IS","OR","ARE"]

    count = 0 
    # print(kelime_say)
    dizi= []
    dizi2= []
    for kelime in kelimeler:  
        if kelime not in baglaclar:
            dizi.append(kelime)
    kelimeSayici = Counter(dizi)  
    print(dizi) 

    for kelime2 in kelimeler2:  
        if kelime2 not in baglaclar:
            dizi2.append(kelime2)
    kelimeSayici2 = Counter(dizi2)  
    print(dizi2)   

    return kelimeSayici.most_common(5),kelimeSayici2.most_common(5)
        

def islemYap3(adres2,adres3):
    html_text = requests.get(adres2).text
    soup = BeautifulSoup(html_text,'lxml')
    kelimeler = soup.find('body').text
    noktalama= str.maketrans('','',punctuation)
    kelimeler= kelimeler.translate(noktalama)
    kelimeler= kelimeler.upper()
    kelimeler= kelimeler.split()
    kelime_say= Counter(kelimeler)
    print(type(kelime_say),'\n')

    html_text2 = requests.get(adres3).text
    soup2 = BeautifulSoup(html_text2,'lxml')
    kelimeler2 = soup2.find('body').text
    noktalama2= str.maketrans('','',punctuation)
    kelimeler2= kelimeler2.translate(noktalama)
    kelimeler2= kelimeler2.upper()
    kelimeler2= kelimeler2.split()
    kelime_say2= Counter(kelimeler2)
    aynıKelimeler = []
    print(type(kelime_say2),'\n')
    count = 0 
    for kelime in kelime_say:  
        
        for kelime2 in kelime_say2:  
            if(kelime == kelime2):  
                count = count + 1
                aynıKelimeler.append(kelime)
                benzerlikOran= (count*2)*100/(len(kelime_say+kelime_say2))
    return ("ayni kelimeler",aynıKelimeler),("benzerlik orani %", benzerlikOran),("ayni kelime sayisi",count)         
def islemYap5(adres6,adres7):
    baglaclar= ["AMA","ANCAK","FAKAT","VE","ASLINDA","KİME","NEYİ","VEYA","BEN","SEN","O","BİZ","SİZ","ONLAR","BIR","CUNKU","DE","DA","ILE","GEREK","BELKI","HALBUKI","YANI","ISE","GIBI","OLARAK"]
    html_text = requests.get(adres6).text
    soup = BeautifulSoup(html_text,'lxml')
    kelimeler = soup.find('body').text
    
    noktalama= str.maketrans('','',punctuation)
    kelimeler= kelimeler.translate(noktalama)
    kelimeler= kelimeler.upper()
    kelimeler= kelimeler.split()

    adres7= adres7.split(",")
    kelimeSayici2= []
    for adresSayisi in adres7:
        html_text2 = requests.get(adresSayisi).text
        soup2 = BeautifulSoup(html_text2,'lxml')
        kelimeler2 = soup2.find('body').text
        
        noktalama2= str.maketrans('','',punctuation)
        kelimeler2= kelimeler2.translate(noktalama)
        kelimeler2= kelimeler2.upper()
        kelimeler2= kelimeler2.split()
        dizi= []
        for kelime2 in kelimeler2:  
            if kelime2 not in baglaclar:
                dizi.append(kelime2)
        kelimeSayici2.append(Counter(dizi).most_common(5))

    for kelime in kelimeler:  
        if kelime not in baglaclar:
            dizi.append(kelime)
    kelimeSayici = Counter(dizi) 
    kelimeSayici= kelimeSayici.most_common(5)     

    #return kelimeSayici2,kelimeSayici

    filepath = 'kelime-esanlamlisi.txt'
    sozluk= {}
    with open(filepath,"r",encoding="utf-8") as fp:
        line = fp.readline()
        cnt = 1
        while line:
            line= line.split()
            #print(line[1])
            line[0]=line[0].upper()
            line[1]=line[1].upper()
            d= {line[0]:line[1]}
            
            if not sozluk.get(line[0]):
                sozluk.update(d)
            #print("Line {}: {}".format(cnt, line.strip()))
            line = fp.readline()
            cnt += 1
    esAnlamSozluk= {}      
    for url in kelimeSayici2:
         for i in range(0,len(url)):
        
             if sozluk.get(url[i][0]):
                 a= sozluk.get(url[i][0]) 
                 b= {url[i][0]:a}
                 esAnlamSozluk.update(b)
             else:
                b= {url[i][0]:url[i][0]}
                esAnlamSozluk.update(b)
    for i in range(0,len(kelimeSayici)):
        if sozluk.get(kelimeSayici[i][0]):
            a= sozluk.get(kelimeSayici[i][0]) 
            b= {kelimeSayici[i][0]:a}
            esAnlamSozluk.update(b)
        else:
            b= {kelimeSayici[i][0]:kelimeSayici[i][0]}
            esAnlamSozluk.update(b)    


    return '{}'.format(esAnlamSozluk)
    
    print(esAnlamSozluk)    
@app.route('/')
def home2():
    return render_template('index.html')

@app.route('/frekans.html')
def home():
    return render_template('frekans.html')

@app.route('/anahtar.html')
def home4():
    return render_template('anahtar.html')

@app.route('/benzerlik.html')
def home3():
    return render_template('benzerlik.html')

@app.route('/esAnlam.html')
def home5():
    return render_template('esAnlam.html')

@app.route('/veriAl', methods=['GET','POST'])
def my_form_post():
    adres = request.form['adres']
    kelime = islemYap(adres)
    result = {
        "output": kelime
        
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

@app.route('/veriAl2', methods=['GET','POST'])
def my_form_post3():
    adres4 = request.form['adres4']
    adres5 = request.form['adres5']
    
    kelime = islemYap2(adres4,adres5)
    result = {
        "output": kelime
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)    

@app.route('/veriAl3', methods=['GET','POST'])
def my_form_post2():
    adres2 = request.form['adres2']
    adres3 = request.form['adres3']
    kelime = islemYap3(adres2,adres3)
    result = {
        "output": kelime
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)  

@app.route('/veriAl5', methods=['GET','POST'])
def my_form_post5():
    adres6 = request.form['adres6']
    adres7 = request.form['adres7']
    
    kelime = islemYap5(adres6,adres7)
    result = {
        "output": kelime
    }
    result = {str(key): value for key, value in result.items()}
    print(result)
    return jsonify(result=result)         
   

if __name__ == '__main__':
    app.static_folder = 'templates'
    app.run(debug=True)