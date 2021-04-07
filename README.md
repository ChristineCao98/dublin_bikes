# Dublin Bike Web Application (dublin_bikes)

## Authors:
- *AnYi Huang*
- *Rachel Courtney*
- *Xiaoyan Cao*

This Project is intended for the "COMP30830 Software Engineering" Module, taught by Dr. Aonghus Lawler.

### EC2 Address: http://54.173.55.247/
### Github Repo: https://github.com/ChristineCao98/dublin_bikes.git 

## Introduction 
- Dublin Bikes is a public bike rental scheme (operated by JCDdecaux) in Dublin's City Centre. Since its launch in 2009, Dublin Bikes has had over 2.5 million user journeys, and has recorded over 15,000 users on its busiest day.  
- The Goal of this Project is to develop a web application that displays live occupancy and weather information for Dublin Bikes. 

- Our website effectively displays a map of Dublin City with markers at every Dublin Bike stand location.
- A marker may be clicked on directly or can be selected in the drop-down menu. 

- For each marker selected the following can be seen:
 1. The Station Number 
 2. The Station Address
 3. The Number of availble bikes 
 4. The Number of free stands 
 5. Total capacity at that station 

- As well as station information (upon marker selection), our website enables you to see:
 1. The average nunber of bikes available per hour over a 24h period. 
 2. The average number of bikes available per day over a 1 week period
 3. A prediction (based off historical data) of bike number availablity for the next four days, showing an hour by hour prediction.
 4. Weather information for that day, as well as the next 5 days

- Our website allows you to enable location services on the map to provide users with the ability to find their closest bike station. 
- A filter may also be applied to the map to further highlight available bikes/stands. This enables users to find desired information at a greater convenience. 

#### Available Bikes Filter (default)
- A marker will appear green in colour if there are over 5 bikes available. The marker will appear larger in size if there is over 20 bikes available.
- A marker will appear red if there are 5 or less bikes available. The marker size will appear smaller in size if there less than 20 bikes available.

#### Available Stands Filter
- A marker will appear green in colour if there are over 5 stands available,. The marker will appear larger in size if there is over 20 stands available.
- A marker will appear red if there are 5 or less stands available. The marker size will appear smaller in size if there less than 20 stands available.

## User Interface 
![dublin_bikes](https://user-images.githubusercontent.com/71882629/113942534-d79ce780-97f8-11eb-8b64-4bc281a15911.png)

# References
1. Bike API: https://developer.jcdecaux.com/#/home
2. Weather API: https://openweathermap.org/api
3. Map API: https://developers.google.com/maps
4. Charts: https://developers.google.com/chart
5. Flask Documentation: https://flask.palletsprojects.com/en/1.1.x/
6. Testing: https://pypi.org/project/flask-unittest/ 


