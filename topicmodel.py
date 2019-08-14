sent_lis=[' My name is John ', 
' Hello,What is your name? ', 
' Where do you stay? ', 
" I don't undetstand anything ", 
' Please wait for sometime ', 
' What is your age? ', 
' How many people are there in your family? ', 
' What are you doing? ', ' Please call me later ',
 ' can we meet tomorrow? ',
  ' There are four people in my family ',
   ' had your lunch? ', ' Hello What is your name? ',
    ' What is your mobile number? ', ' Please use dustbin, dont throw garbage ', 
    ' Nice to meet you. ', ' I had to say something but i forgot ', 
    ' had your lunch? ', ' What is your age? ', ' I am fine ', 
    ' Dont worry ', ' flower is beautiful ', ' What is your job ? ', 
    ' Sundry ', ' Synthesis ', ' Take care ', ' Arise ', ' Be careful ', 
    ' How are you? ', ' you are wrong ', ' Are you sick? ', ' All the best ',
     ' What is the problem? ', ' When is your Interview? ', ' Stand up ', 
     ' Shall i help you? ', ' Where is the police station? ', ' Good morning  ', 
     ' Discipline ', ' Where is the bathroom? ', ' Please call me later. ', 
     ' Where do you stay? ', ' Wait i am thinking ', ' Irresponsible ', 
     ' Comfort / comfortable ', " What is today's date ? ", ' I am thinking ', 
     ' There was traffic jam ', ' sit down  ', ' Where do you stay? ', ' Where is the hospital? ', 
     ' I dont understand anything. ', ' What are your expectation from job? ', 
     ' Where is the police station? ', ' Are you hungry ? ', ' Mutual Fund ',
      ' What are you doing? ', ' Where is the bathroom ? ', ' FD Fixed deposit ', 
      ' Are you angry? ', ' Sign Language interpreter ', ' Tell me about yourself ', 
      ' I have headache. ', ' Good Night ', ' My name is JOHN ', 
      ' What is your mobile number? ', ' Good Evening ', " Let's go for lunch ", 
      ' what is your father doing? ', ' I am fine ', ' I am bore doing nothing. ', 
      ' when will we go ? ', ' PF Provident Fund ', ' Good Question ', ' My mother is a homemaker. ',
       " What's up ? ", ' Can we meet tommorow? ', ' Do you have any questions for you? ', 
       ' RD Recurring Deposits ', ' Good Afternoon ', ' How many people are there in your family? ', 
       ' Open the door ', ' Please give me your pen. ', ' Hello What is your name ? ', 
       ' do you consider yourself successful? ', ' what position do you prefer ', 
       ' Please wait for sometime. ', ' I am sorry. ', ' Any questions? ', 
       ' Please call an ambulance ', ' Are you busy? ', ' Shall we go together tommorow? ', 
       ' There are four people in my family. ', ' My name is JOHN. ', ' No smoking please ', 
       ' I live in Nagpur. ', ' Please clean the room  ', ' When is your interview? ', 
       ' When will we go ? ', ' I am a clerk. ', ' Happy Journey ', ' Did you finish your home work ? ', 
       ' You are wrong ', ' Did you book tickets? ', ' I am tired. ', ' Do you want something to drink? ',
        ' I go to theatre. ', ' I like pink color ', ' Do you have money? ', ' Do you want Tea or Coffee? ',
         ' Please use dustbin, dont throw garbage. ', ' Do you go to office? ', ' I love to shop. ', 
         ' Do you watch TV? ', ' I had to say something but i forgot. ']

import gensim
from gensim import corpora
doc_lis=[ i.lower().split() for i in sent_lis]
# dictionary = corpora.Dictionary(doc_lis)
# corpus = [dictionary.doc2bow(text) for text in doc_lis]
# tfidf=gensim.models.TfidfModel(corpus)
# tfidf_corpus=tfidf[corpus]

# ldamodel = gensim.models.ldamodel.LdaModel(tfidf_corpus, num_topics = 17, id2word=dictionary, passes=100)
# ldamodel.save('model5.gensim')
# #topics = ldamodel.print_topics(num_words=6)
# topic_number=[]
# percent=[]
# for idx,row in enumerate(ldamodel[tfidf_corpus]):
#     row=sorted(row,key=lambda x:(x[1]),reverse=True)
#     topic_number.append(row[0][0])
#     percent.append(row[0][1])
import pandas as pd 
#topic_model=pd.DataFrame({"documents":sent_lis,"topic":topic_number,"percent":percent})
from gensim.models import Word2Vec

from nltk.cluster import KMeansClusterer
import nltk


from sklearn import cluster
from sklearn import metrics

model = Word2Vec(doc_lis, min_count=1)
X = model[model.wv.vocab]
model.wv.n_similarity(doc_lis[0],doc_lis[1])
def createSimilarGroups(lis=[],idx=1,sim=.4,topic_dict={}):
    if lis:
        topic_dict[idx]=[lis.pop(0)]
        topic_dict[idx].extend([lis[i] for i in range(len(lis)) if model.wv.n_similarity(lis[i],topic_dict[idx][0])>sim])
        for i in topic_dict[idx][1:]:
            lis.remove(i)
        n=idx+1
        #print(n)
        if not lis:
            #print(topic_dict)
            return topic_dict           
        else:
            createSimilarGroups(lis=lis,idx=n,sim=.3,topic_dict=topic_dict)

    else:

        return topic_dict
            
    return {key:[" ".join(sent)for sent in topic_dict[key]]for key in topic_dict}
 
topics=createSimilarGroups(lis=doc_lis)
df_dict={"topics":[],"sentences":[]}
for key in topics.keys():
    df_dict["topics"].extend([key]*len(topics[key]))
    df_dict["sentences"].extend(topics[key])
pd.DataFrame(df_dict).to_excel("topics_similarity.xlsx")