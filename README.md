jpmcResearchBot
===============

The main function of this tool is to extract suggested tags from a given document or a given string content.

The suggested tags will partly contain the keyword extracted from the content using the tf-idf algorithm and partly 

contain the name entity extracted using the NER(name entity recognition algorithm)

----------

# I. File List

----------

- [ ] DB.py

- [ ] NER

  - [ ] \_\_init\_\_.py

  - [ ] extractNER.py

  - [ ] sample.py

- [ ]  README.md

- [ ] TFIDF

  - [ ] \_\_init\_\_.py

  - [ ] extractTFIDF.py

  - [ ] initialIdf.py

  - [ ] sample.py

  - [ ] txtAssets

    - [ ] 20140702\_CMTI\_.txt

    - [ ] JPM\_EM\_Fixed\_Income\_Flow\_2014-02-06\_1316372.txt

    - [ ] JPM\_FX\_Markets\_Weekly\_Cu\_2014-07-19\_1444037.txt

    - [ ] JPM\_Municipal\_Bond\_Porti\_2014-01-31\_1311449.txt

    - [ ] JPM\_US\_Equity\_Strategy\_F\_2014-03-07\_1340480.txt

    - [ ] jpmc\_abstract.txt

- [ ] \_\_init\_\_.py

- [ ] config.py

- [ ] createTablesInDB.py

- [ ] deployscript.sh

- [ ] sample.py

- [ ] test.py

----------

# II. Design

----------

In the tf-idf algorithm, term frequency(tf) is the raw frequency of a term in a document. Inverse document frequency(idf) is a measure of how much information the word provides and it is the logiarithmically scaled fration of the documents contain the word, obtained by dividing the total number of documents by the number of documents containing the term, and then taking the logarithm of that quotient.

The NER algorithm will try to extract the name entities from the document. 

A mySQL database is created for the usage of idf, the table named idf and the table named doc\_num contain all the necessary information to calculate idf. These tables shall be created and initialized at the beginning and shall only be updated if new documents are imported.

Inclusion table and exclusion table are also maintained in the mySQL database as two tables named T\_inclusion and T\_exclusion accordingly.

-----------

# III. Configuration

-----------
Python Dependencies:
- Flask
- Numpy
- NLTK (see http://www.nltk.org/data.html, additional data needs to downloaded to /usr/share in order for the module to work correctly)
- MySQL-python (if you decide to use mysql as the backend)

0) Python + Flask needs to sit on some webserver in order for the API to serve extrernal HTTP calls. The test server is hosted on an Ubuntu Amazon cloud instance with Apache. Hosting the API on other webservers are possible. Please see this deployment section for examples and configuration:

http://flask.pocoo.org/docs/0.10/deploying/

For pure testing on localhost. It is possible to run \_\_init\_\_.py directly from your favorite Python IDE and ping your server on via localhost:5000.

Configuration parameters for the API are saved in the file config.py

1)

mySQL Configuration

  to enable mySQL, 4 paramters must be set in the config.py. MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB_NAME

2)

Documents configuration

  all the jpmc research documents are supposed to be kept in ./TFIDF/txtAssets/ 

  Those text files with extention '.txt' will enable the algorithm to generate the idf data in the 1st step.

-----------

# IV. Initialization

-----------

1) create tables (idf table, doc\_sum table, inclusion and exclusion tables)

  Run 'python createTablesInDB.py' will automatically create all the tables(after setting up config.py)

2) create or update the idf data table

  move all the documents to the directory ./TFIDF/txtAssets/

  go to directory ./TFIDF/

  Run 'python initialIDF.py' 
  
-----------

# V. Examples

-----------
Once your server is running. There are 3 types of HTTP calls available, they all require the POST method:

http://54.149.112.169:5000/getKeywords

  Uses a half and half approach for the algorithm: half from Named Entities, half from TFIDF
  
http://54.149.112.169:5000/getTFIDF

  Uses TFIDF. It returns unigrams (single words only).
  
http://54.149.112.169:5000/getNER

  Uses Named Entity Recognition (NER) returns significant name-like nouns (could be longer than a single word)
  
They all take the same text input. In the Header section of the HTTP request, you can specify this as a raw text or JSON input:

{
	"text":"<some text>",
	"max_n":<maximum keywords returned> 
}

Example:

{
	"text":" Near term, however, we would expect investors to continue reducing underweight positions indiscriminately in both E.ON and RWE given the perceived potential upside from capacity payments, higher power prices, further cost cutting and a burden sharing deal with the government on long-term nuclear liabilities. ",
	"max_n":30
}




