Nevernote API
---
#### Deploying
    TODO
---
#### Testing
Nevernote API uses the PyTest framework to conduct it's unit tests. To start PyTest, simply run the follow from the root directory
```
python -m pytest
```
---
#### API Documentation
Nevernote API uses RAML to automatically create documentation for the API.
Visit the documentation after running the API at

##### Usage
```
[IP_ADDRESS]:[PORT]/documentation
```
##### Example
```
http://localhost:80/documentation
```
---
#### Regenerating API Documentation
To regenerate the API documentation automatically you must do the following
##### Install NodeJS
```
https://nodejs.org/en/download/
```

##### Install raml2html
```
npm i -g raml2html
```

##### Generate raml file
From the root directory run the following command
```
python documentation/generate_raml_file.py
```
---

###### Written by Blake DeBenon