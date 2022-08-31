# Project to webscrape and analyse news articles from various papers

Want to analyse if the behaviour of premium to non premium articles correlates between different newspapers

## TODO

test abos for premium article length?

## Data to collect:
* Autor name
* date and time
* premium article
* length (maybe not possible for premium)
* position on title page?
* title (for no double counting)
* average length of words
* type of article (commentary, sth.)
* occurence (repetition)

## News paper list
* FAZ
* TAZ
* Bild
* Zeit
* Welt
* sz
* new york times

## Webscraper



set fixed number of articles per news paper
cron job
how to do constant download time?
how to no double counting (maybe we want doublecounting)
Some sites dont want to bescraped-> use additional headers ()

### Links
* https://realpython.com/beautiful-soup-web-scraper-python/

## Database

way to check if all went right
own database for every paper

* author: string
* date: date?
* time: timestemp
* premium article: bool
* length: int count of words
* position: int number of articles above ("above definition")
* title: string
* average length of words: float

## Analysis

* correlation length to premium non premium
* correlation length to author
* number of articles author
* date time published vs author
* articles published vs week day
