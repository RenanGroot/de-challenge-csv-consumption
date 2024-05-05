**Table of Contents**

# Introduction
This repository was created as a delivery to a Data Engineering Challenge. The task and the solution are better explained below:
## Task/ Problem
> Your task is to build an automatic process to ingest data on an on-demand basis. The data represents trips taken by different vehicles, and include a city, a point of origin and a destination.
> 
> We do not need a graphical interface. Your application should preferably be a REST API, or a
console application.
Draw a brief model of how it is working.

# Main Features
- **Upload CSV files to Database. (API endpoint)**
    - It is possible to use the solution to upload new data into the database thought an POST method, containing the csv file, to ("/") endpoint.
- **Upload status check. (API endpoint)**
    - It is possible to check the upload status of the file sent in the upload endpoint. There are two possible status: "Uploading" and "Done".
- **SQL Database**
    - SQL database holding two main tables, one with the trips details and another with the upload status details:
     - trips (TABLE) 
         - id, region, origin_lat, origin_long, dest_lat, dest_long, datetime, datasource
     - status (TABLE)
         - filename, status, datetime
- **Weekly average number of trips for an area, defined by a bounding box (given by coordinates) or by a region. (API endpoint)**
- **Sample CSV files for testing purpouses. ("/samples/")**
    - You can use some sample files to test the solution, those files are inside the "samples" folder.
- **Simple index.html when using GET method in homepage ("/"), for making test uploads more easily.**
    - To make it more user friendly testing the csv files upload, it was created a simple index.html page with few buttons to upload the csv files.

# How to execute
1. **Clone the repository ino the desired folder**
```
git clone https://github.com/RenanGroot/de-challenge-csv-consumption.git
```

2. **Python and PIP version.**

   The Python version used during this project was `Python 3.11.9` and the pip version was `pip 23.3.1`. You should have these tools installed on your environment in order to use the solution.
   
3. **Install the libraries from the requirements.txt using pip.**
```
pip install -r requirements.txt
```
4. **Start Flask**
   
   Execute the command in your terminal to start the flask application (server side).
```
flask run
```
5. **Access the API though an browser or other local request tool.**

   You can access the running solution in the url: 127.0.0.1:500
   
   It also may have another url, please check in your terminal which url the flask is running. When you execute `flask run` it also shows you an url path in the terminal.

6. **Explore the endpoints**

   You can explore the endpoints looking more in deep into their documentation in the next section.
   
# Endpoints Documentation

## Upload CSV files
<details>
  <summary> Upload (POST)(file) </summary>
  <br>
 
  | Method | Feature | URL |
  |---|---|---|
  | `POST` | Upload a csv file to database | `127.0.0.1:5000/`

  Attached to your request, you should send a file ´.csv´. If you face some issues trying to reach the endpoint directly though a request, you also can access thought GET method the same endpoint using a browser. This last option is going to allow you to use a simple UI to send the csv file.

</details>

# de-challenge-csv-consumption
 This is a repository for a Data Engineering Challenge, envolving the .csv comsumption and distribuition by REST API
