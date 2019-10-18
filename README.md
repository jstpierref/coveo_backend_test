# Coveo Backend Coding Challenge

The current version is deployed on Heroku as a Docker container. I used Semaphore platform to handle the CI/CD pipeline.

Basically, Semaphore builds the image, runs the tests and deploy the container to Heroku.

HTTP API endpoint: [http://city-search-engine.herokuapp.com/](http://city-search-engine.herokuapp.com/)

HTTPS API endpoint: [https://city-search-engine.herokuapp.com/](https://city-search-engine.herokuapp.com/) (Swagger not showing up for now)

Public Docker image: [https://hub.docker.com/r/jstpierref/flask_city_search_engine](https://hub.docker.com/r/jstpierref/flask_city_search_engine)

## How it works: the indexer

General city data are stored in memory in a hash table and the search index itself uses a trie data structure, which ensures fast lookups.

## How it works: the score

Multiple criterias are used to obtained a general search score for each suggestion given a keyword `q`:
* Length: based query keyword and index keyword respective length. The score is higher if query and found keyword have similar length. The score is obtained via len(query_word)/len(index_keyword) and it is allways between 0 and 1.
* Type: The score is higher if query corresponds to
    an official name (`name`, score: 1.) than an alternative name (`alt_name`, score: 0.5) or a
    subname of city name (`sub_name`, score: 0.5) in the index (e.g.: 'york' is a subname of 'new-york').
* Position: based on query keyword position in index keyword. If query is a subname of a city name, 
    gives higher score if the substring is located at the beginning of city 
    name (e.g.: 'new' and 'york' have positions 0 and 1 respectively 
    in 'new-york'). The score is obtained via 1/(position+1), so it is allways between between 0 and 1.
* Geographical distance: a distance in km is calculated between query coordinates and index keyword coordinates and a simple math.exp(-d/300) operation is applied to to get a score between 0 and 1.

If geographical coordinates are given, the score is calculated as:<br />
`score = 0.3*length_score + 0.1*type_score + 0.1*position_score + 0.5*geo_score`<br /><br />
And if it not the case the score is obtained via:<br />
`score = 0.4*length_score + 0.3*type_score + 0.3*position_score`

Many of those choices are subjective. One improvement would be to optimized the implied functions and parameters according to some preferred behaviors.

### Build, test and run locally
Install and create a virtual environement
```bash
pip install --upgrade pip
pip install --upgrade virtualenv
virtualenv venv
```

Install project dependencies and run unit tests
```bash
pip install -r requirements.txt
python manage.py test
```
Run the project and use Postman/browser/curl to access the API
```bash
python manage.py run 
```

## Sample responses

These responses are meant to provide guidance. The exact values can vary based on the data source and scoring algorithm

**Near match**

    GET /suggestions?q=Londo&latitude=43.70011&longitude=-79.4163

```json
{
  "suggestions": [
    {
      "name": "London, ON, Canada",
      "latitude": "42.98339",
      "longitude": "-81.23304",
      "score": 0.74
    },
    {
      "name": "London, OH, USA",
      "latitude": "39.88645",
      "longitude": "-83.44825",
      "score": 0.53
    },
    {
      "name": "London, KY, USA",
      "latitude": "37.12898",
      "longitude": "-84.08326",
      "score": 0.48
    },
    {
      "name": "Londontowne, MD, USA",
      "latitude": "38.93345",
      "longitude": "-76.54941",
      "score": 0.41
    },
    {
      "name": "Londonderry, NH, USA",
      "latitude": "42.86509",
      "longitude": "-71.37395",
      "score": 0.39
    }
  ]
}
```

**No match**

    GET /suggestions?q=SomeRandomCityInTheMiddleOfNowhere

```json
{
  "suggestions": []
}
```

## Potential improvements

* Cache layer
* Database
* POST requests handling to change backend state
* Authentication
* Improve API engine with:
	* n-gram based distances for fuzzy string search
	* Word embedding based distances (neural nets) to capture semantics
