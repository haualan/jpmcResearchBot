jpmcResearchBot

===============

The main function of this tool is to extract suggested tags from a given document or a given string content.

The suggested tags will partly contain the keyword extracted from the content using the tf-idf algorithm and partly 

contain the name entity extracted using the NER(name entity recognition algorithm)

----------

# I. File List

----------

├── DB.py
├── NER
│   ├── __init__.py
│   ├── extractNER.py
│   └── sample.py
├── README.md
├── TFIDF
│   ├── __init__.py
│   ├── extractTFIDF.py
│   ├── initialIdf.py
│   ├── sample.py
│   └── txtAssets
│       ├── 20140702_CMTI_.txt
│       ├── JPM_EM_Fixed_Income_Flow_2014-02-06_1316372.txt
│       ├── JPM_FX_Markets_Weekly_Cu_2014-07-19_1444037.txt
│       ├── JPM_Municipal_Bond_Porti_2014-01-31_1311449.txt
│       ├── JPM_US_Equity_Strategy_F_2014-03-07_1340480.txt
│       └── jpmc_abstract.txt
├── __init__.py
├── config.py
├── createTablesInDB.py
├── deployscript.sh
├── sample.py
└── test.py

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

0) Python + Flask needs to sit on some webserver in order for the API to serve extrernal HTTP calls. The test server is hosted on an Ubuntu Amazon cloud instance with Apache. Hosting the API on other webservers are possible. Please see this deployment section for examples and configuration:

http://flask.pocoo.org/docs/0.10/deploying/

For pure testing on localhost. It is possible to run __init__.py directly from your favorite Python IDE and ping your server on via localhost:5000.

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

