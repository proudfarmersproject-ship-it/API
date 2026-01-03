# API
## SetUp Guide
1. Clone from main branch using ```git clone https://github.com/proudfarmersproject-ship-it/API.git```
2. move to API folder with ```cd ./API```
3. Create the virtual environment by running : ```python -m venv nameofyourvenv```
4. Now activate the environment using the ```.\nameofyourvenv\Scripts\activate```
5. You need to activate this environment before everytime you run the code.
6. Upon successfull avtivation you will see ```(nameofyourvenv) C:\yourpath``` of the folder in terminal.
7. Now Install all the requirements by running ```pip install -r requirements.txt```with acivated environment.
8. Now run ```py app.py``` with activated environment in place the app will start at ```localhost:5000```
9. after finsihing you can run ```deactivate``` to stop the environment

## EndPoints Access or Testing 
1. .env is most important as it contains all the db creds and backblaze creds.
2. If you examine app.py you'll find the endpoints supported.
3. Sample endpoints 
```
/api/categories - POST, GET, PATCH, DELETE
/api/products/create - POST
/api/products - GET

```
4. To know the supported request fields thay are placed in ```/resources``` of the directory.
5. For each component there is a seperate folder and Each file inside the folder has the methods ctreated for the endpoints. 