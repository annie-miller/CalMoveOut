# CalMoveOut
Cal Move Out Cooperative Reuse Matching Algorithm and Documentation


Table of Contents
About The Project
Built With
Getting Started
Installation
Usage
Roadmap
Contributing
Contact
Acknowledgments



1. About the Project

	This project was meant to minimize the manual labor of cooperative reuse. It is an algorithm that matches the survey entries by time slots that they are available for and distance, in order to reduce emissions from pickups. 

Notes from the building of this algorithm and the meeting notes: https://docs.google.com/document/d/1Prk5LO6nRVdOV_FogytPioiG2TcuR7rPBW81MA1G-F0/edit?usp=sharing

2. Built With
Jupyterhub in Python


3. Getting Started
	Open Jupyterhub and create a new folder. Go to the google sheet with the google form responses and download the responses as a csv. Next go to your downloads folder and change the name of the file to “addresses.csv” then upload the file to the Jupyterhub folder that you created. Go to the github link below and download the “updated_algorithm.ipynb” file and upload this to the Jupyterhub folder as well. 

	Github repository: https://github.com/anniemiller49/CalMoveOut 


4. Installation
	No installation should be required, as everything can be run through Jupyter Hub. 

5. Usage
	This algorithm should be used to create the groupings by day and time slot for people who are participating in cooperative reuse. The algorithm is currently built to output 8 tables, two for each of the four days of move out pickups. Some of the dates and values are hardcoded so these will need to be updated each year to reflect those changes. 

6. Roadmap
The overall steps of the algorithm are:
Reading in the data
Cleaning the data
Group by date/time for one with only one time slot
Group instances with more than one time slot available by best fit of location
Check group sizes/potentially break up groups/or add to groups
Least path matching algorithm implementation once all instances are grouped

Throughout the process of trying to create this project Kathryn and I met with many people that have helped with the cooperative reuse program. They gave insights and background that were crucial in the development of this algorithm. The process started by learning more about cooperative reuse from Kathryn Wilson, who was my main advisor for this project and a huge help in building this algorithm, Emily Que, Julie Zhu, Julia Sherman, and Jen Loy. After learning more about their matching process, I was able to begin the process of trying to automate it. I started out by researching different established distance algorithms or geographic information systems that could be used to match students to a time slot that would reduce emissions and distance traveled. This process of reading through different online forums and the meetings that took place resulted in the algorithm that I have written. I settled on a program that was written on the JupyterHub platform in python, as this was a platform and language that I have a wide range of experience in. In the future, it could be helpful to consider other more geographically focused data platforms for routing. 
In the past there have been times when the movers were sent back to the same block twice in one day, so in order to try to reduce the repeats for the movers and the emissions from their trucks I focused on matching form submissions by location and availability. My starting point for matching people to certain time slots was their overall availability and their location. The first step in writing the algorithm was reading in the data that was collected from the forms. After that the data needed to be cleaned to make sure that all entries were in the proper format. Next, I filtered the table by entries that were only available for one time slot, as priority is given to those who fill out the form first.  I then put each entry that was only available for one time slot into the respective table for that time. After that was done, I then went through the process of matching each of the entries that was available for more than one time slot. For each time slot that the entry was available I went through each of the rows in each table and found the shortest distance to the entry that was trying to be matched. I then went through each of the items in the list with the shortest distance for each table, and matched the entry with the table with the shortest distance to the stops already in being made for that slot. Once each entry was matched, I checked the length of the tables to make sure that those who filled out the form first still have priority over those who filled it out later.  There was a constraint on how many stops could be done for each shift which depended on the number of items and amount of time for each slot. The number that was decided was 13 stops for each time slot. If a table had less than 13, I re-matched entries for tables that had more than 13 in order to redistribute the values. After that was done, I reordered the tables so they were sorted by their original index, and then I put them in order of distance. This last step was meant to help the routing and have a starting point for that process. 



7. Contributing:

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated. 

8. Contact:

Annie Miller - anniemiller@berkeley.edu or anniemiller054@gmail.com 
Project Link on Github: https://github.com/anniemiller49/CalMoveOut 


9. Acknowledgements

	Thank you to Kathryn Wilson, Grace Martin, Jessica Heiges, Dr. Kate O’Neill and the ZWL team and students, Jen Loy,  Emily Que, Julie Zhu, Tamera Garlock,  David Sorrell, Julia Sherman, and Michelle Fong for all their help. 

