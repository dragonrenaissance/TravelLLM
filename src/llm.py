# -*- coding: utf-8 -*-



#from pyairtable import Api
import requests
from  bs4  import BeautifulSoup
import os

#URLcolumnName = 'Viator Review URL'
#api = Api('patcDd4BxY9AUt83Z.2c4b2d9b982fcce36a4aeb935f81340ef1de7060b552e6c6f4e272dd4b9275ca')
#TableID = 'tblU03vJ8ows50vKC'
#BaseID = 'appNmMXYkVezxHRQA'

#table = api.table(BaseID,TableID)
#input = table.all(fields =[URLcolumnName ],formula="{"+URLcolumnName+"}")

#recordID = input[0]["id"]
#URL = input[0]["fields"][URLcolumnName]

def remove_newlines(serie):
    serie = serie.replace('\n', ' ')
    serie = serie.replace('\\n', ' ')
    serie = serie.replace('  ', ' ')
    serie = serie.replace('  ', ' ')
    return serie
def Scrape(url):
    response = requests.get(url='https://proxy.scrapeops.io/v1/',
                            params={'api_key': 'd03cb24a-6881-4020-a06a-e5e0aa695130','url': url,},)
    soup =  BeautifulSoup(response.text,"html.parser")
    text = remove_newlines(soup.get_text())
    words = text.split()[:2300]
    return ' '.join(words)



from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import openai
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY
# Define the system message


# Create a dataset using GPT
def BinaryGen(user_msg):
  system_msg = "You will be presented with user reviews and your job is to provide a set of tags from the following list. Provide your answer in bullet point form. Choose ONLY from the list of tags provided here (choose either the positive or the negative tag but NOT both):\n    \n    - Top attractions  OR Culture authentic\n    - Relaxed OR Adventurous\n    - Spontaneous OR Fully Planned Schedule"

  response = openai.ChatCompletion.create(model="gpt-3.5-turbo",temperature=0,
                                        messages=[{"role": "system", "content": system_msg},
                                         {"role": "user", "content": user_msg}])
  return response.choices[0].message["content"]

def BudgetGen(user_msg):
# Define the system message
  system_msgBudget = "You will be presented with user reviews and your job is to estimate the budge of the each activity. Provide your answer in dollar amount"

# Create a dataset using GPT
  responseBudget = openai.ChatCompletion.create(model="gpt-3.5-turbo",temperature=0,
                                        messages=[{"role": "system", "content": system_msgBudget},
                                         {"role": "user", "content": user_msg}])
  return responseBudget.choices[0].message["content"]

import os.path
from langchain.chains.summarize import load_summarize_chain
import textwrap


gpt_35_turbo_max_tokens = 4097
def SummaryGen(user_msg,url):
  with open("_"+url[8:].replace("/","_")+".txt","w",encoding = "UTF-8") as fw:

    fw.write(user_msg)

    fw.close()
  loader = TextLoader("_"+url[8:].replace("/","_")+".txt")
  news_article = loader.load()
  model_name = "gpt-3.5-turbo"
  llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name=model_name)
  gpt_35_turbo_max_tokens = 4097
  verbose = True
  prompt_template = """Write a concise summary of the following:


  {text}


  SUMMARY IN POSITIVE INTRODUCE EXPLAIN MORE ACTIVITIES ："""

  prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
  chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt, verbose=verbose)
  summary = chain.run(news_article)
  return remove_newlines(textwrap.fill(remove_newlines(summary), width=200))
import re

def CruateGen(URL):
  text = Scrape(URL)
  print("__________data read: " + text)

  if 'Failed' in text:
    return text
  mydict = {}
  
  b = BinaryGen(text)

  s = b.split("-")
  if len(s)==4:

    mydict["Culture"] = s[1].strip()
    mydict["Activity"] = s[2].strip()
    mydict["Schedule"] = s[3].strip()
    
  
  else:
     output = b

     

  print("__________binary value"+b)

  p = BudgetGen(text)
  print("__________budget"+p)
  x = re.findall(r"\$[^\]]+", p)



  if len(x)==1:
     mydict['Budget'] = x[0]
  if len(x)>1:
     mydict['Budget'] = f'from {x[0]} to {x[1]}'
  if len(x)==0:
     mydict['Budget'] = f'Not Estimatable'

  sum = SummaryGen(text,URL)


  mydict["summarization"]=sum
  if len(s) == 4:
    return str(mydict) 
  else:
    return output +' Budget: ' + x + ' Summization: '+ sum



                                                                                                       
