# Academic World Dashboard

## Purpose:
The application scenario is an academic research collaboration dashboard and it provides information about faculty members, universities, and publications related to the field of data and machine learning. It enables users to search for and view information about faculty members, follow favorite professors, view top universities in specific fields, and identify the top faculty members in the field of data and machine learning.

The target users of this application are academic researchers, faculty members, and students who are interested in collaborating and sharing knowledge in the field of data and machine learning.

## The objectives:

The objectives of this application are to provide users with an easy-to-use dashboard that allows them to search for and view information about faculty members, universities, and publications related to the field of data and machine learning. The application also enables users to add favorite professors, view the top universities, and view the top faculty members in the field of data and machine learning.

## Demo:
A video demo of the application can be found at this link: https://mediaspace.illinois.edu/media/t/1_t5uykcpo

## Installation:
To install the application, follow these steps:

Clone the repository to your local machine: git clone https://github.com/drew7459/DrewPatel.git

Start the application by running: python app.py
## Usage:
To use the application, follow these steps:

Access the web interface by opening a web browser and navigating to http://localhost:8050/
Use the search bar to find faculty members or universities based on their research interests
View the data tables and graphs to explore academic data
Add faculty members to your favorites list by searching for them and clicking add to favorites
View your saved faculty members by navigating to the Favorites tab in the sidebar
Click X to remove them from favorites

## Design:
The Academic World Dashboard is built using the Dash framework for Python. The application consists of several components, including search bars for faculty and universities, data tables for displaying academic data, and graphs for visualizing data.

The architecture of the application consists of a front-end, built using Dash, and a back-end, consisting of a MySQL database. The front-end sends SQL queries to the back-end, which returns the requested data in JSON format. The front-end then renders the data using Dash components.

## Implementation:
The Academic World Dashboard is built using the following frameworks and libraries:

Dash: for building the web interface
MySQL/MongoDB/Neo4j: for storing and querying academic data

Database Techniques:
The database techniques used in this program are indexing, constraints, and stored procedures. 

Indexes were added to the faculty table in the MySQL database to speed up queries that involve sorting or searching on specific columns. Specifically, an index was added on the **`name`** column to speed up searches on faculty names, and an index was added on the **`favorite`** column to speed up searches for favorite faculty.

A unique constraint was added to the **`email`** column in the faculty table to ensure that each email address is unique and that no two faculty members can have the same email.

Lastly, a stored procedure was added to the MySQL database to calculate the KRC score for faculty members based on their publications and keywords. This stored procedure is called from the **`get_topFaculty()`** function in the Python code to retrieve the top faculty in "Data" keywords.

## Contributions:
Drew Patel - ALL
Total time spent on the project: 60 hours

Widgets:

1 - Top Most Popular Keywords
  - Table 
  - Filter ability
  
2 - UIUC Faculty in "Machine Learning"
  - Table 

3 - Top 10 Universities by Faculty Count Keywords
  - Bar Chart
  - Ability to change keyword 

4 - Top Faculty at All Universities in "Data" Keywords
  - Bar Chart

5 - Faculty Search
  - Table
  - Add to favorites
  
6 - Saved Faculty
  - Table
  - Ability to add and remove faculty

