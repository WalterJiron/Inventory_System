## First set up a virtual environment:


### 1. Create a virtual environment:

*On Windows:*

```bash
       python -m venv venv
```
*On Linux or MacOS:*
```bash
       python3 -m venv venv
```


### 2. Activate the virtual environment:

*On Windows:*
```bash
       .\venv\Scripts\activate
```
*On Linux or MacOS:*
```bash
       source venv/bin/activate
```
 
 ## Install dependencies:
 ```bash
        pip install -r requirements.txt
 ```
 
 ## Run the app:
 ```bash
        uvicorn src.main:app --reload
```