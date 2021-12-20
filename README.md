# Data query exam for Python

## Prerequisite

- Python 3.7 and up

## Testing
Run tests by running file test_it.py 
From shell:
`python3 -m unittest discover -v test`

## What do I need to implement?

service.py - the service that implement query and save functions  


# Data Query

## Description:
Your task is to implement a service able to store and retrieve data.
Data does not have to be persisted meaning storing it in-memory is enough. 
Data structure is pre-defined as following:

| Fields                                        | Example     | 
| -----------                                   | ----------- | 
| id - text <br>title - text<br> content - text <br>views - integer number<br>timestamp - integer number|{ "id": "first-post", "title": "My First Post","content": "Hello World!","views": 1,"timestamp": 1555832341 }
 
      
### API requirements
API consists of two end-points - one to store data and one to retrieve it.  

| Endpoint                                        | Example     | Response  | 
| -----------                                     | ----------- |-----------|
| Query<br> Takes query as input and returns matching entries. Query format is defined below.| query("EQUAL(id,"abc")") | [{"id":"abc","title":"Alphabet","content":"A, B, C, ...","views":1,"timestamp":1555832341}]     |
| Store<br> Take entity and stores it. ID must remain unique. If record with given ID already exists, it should be overwritten.| store({"id":"abc","title":"Alphabet","content":"A, B, C, ...","views":1,"timestamp":1555832341}) | |
 
### Query
| Operator                                        | Example     | 
| -----------                                     | ----------- |
| EQUAL(property,value) <br> Filters only values which have matching property value.| EQUAL(id,"first-post") <br> EQUAL(views,100)   |
| AND(a,b) <br> Filters only values for which both a and b are true.| AND(EQUAL(id,"first-post"),EQUAL(views,100)) | 
| OR(a,b) <br> Filters only values for which either a or b is true (or both).| OR(EQUAL(id,"first-post"),EQUAL(id,"second-post")) | 
| NOT(a) <br> Filters only values for which a is false.| NOT(EQUAL(id,"first-post")) | 
| GREATER_THAN(property,value) <br> Filters only values for which property is greater than the given value. Valid only for number values.| GREATER_THAN(views,100) | 
| LESS_THAN(property,value) <br> Filters only values for which property is less than the given value. Valid only for number values.| LESS_THAN(views,100) |
                                                                                                                           
