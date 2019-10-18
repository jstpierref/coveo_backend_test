# Coveo Backend Coding Challenge

## How it works: the indexer

## How it works: the score

* length: based query keyword and index keyword respective length. The score is higher if query and found keyword have similar length
* type: The score is higher if query corresponds to
    an official name (`name`) than an alternative name (`alt_name`) or a
    subname of city name (`sub_name`) in the index (e.g.: 'york' is a subname of 'new-york').
* position: based on query keyword position in index keyword. If query is a subname of a city name, 
    gives higher score if the substring is located at the beginning of city 
    name (e.g.: 'new' and 'york' have positions 0 and 1 respectively 
    in 'new-york')

* Distance between points is first calculated in km, assuming the Earth is 
a perfect sphere, and a simple math.exp(-d/300) is applied.

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

## Potential improvments

* Cache layer
* Database
* POST requests handling to change backend state
* Authentication
* Improve API engine with:
	* n-gram models for fuzzy string search
	* Word embedding based (neural nets) to capture semantics