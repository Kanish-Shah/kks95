from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import re
import pandas as pd 

lemmatizer = WordNetLemmatizer()
def loadData(fname):
    reviews=[]
    labels=[]
    text = []
    text1 =[]
    f=open(fname,encoding = 'utf8')
    i=0
    for line in f:
        i+=1
        try:
            review,rating=line.strip().split('\t')
            review = review.lower()
            review = re.sub('[^a-z0-9]',' ',review)
            reviews.append(review) 
            labels.append(int(rating))
        except:
            print(i)
        
    f.close()
    for word in reviews:
        text = lemmatizer.lemmatize(word)
        text1.append(text)
    return text1,labels

rev_train,labels_train=loadData('train.txt')
rev_test=loadData('testrun.txt')

counter = CountVectorizer()
counter.fit(rev_train)


#count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(rev_train)#transform the training data
counts_test = counter.transform(rev_test)#transform the testing data

#train classifier
clf = MultinomialNB()

#train all classifier on the same datasets
clf.fit(counts_train,labels_train)

#use hard voting to predict (majority voting)
pred=clf.predict(counts_test)
output = pd.DataFrame(pred)
output.to_csv('testrunoutput.csv', index=False)
