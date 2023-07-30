# Installation

### python3 and postgreSQL must be installed in order to run this applications.

The user can create their own postgreSQL database, link to it and provide a JWT as per the .env.sample file. Otherwise, the user can follow the instructions below 



- open postgreSQL and create a database titled 'piano_tech_client_db'
- connect to the database
- create a user 'admin' with password '12345'
- grant user all privileges on piano_tech_client_db database
- create a new virtual environment 
- install the dependencies in the requirements.txt file
- create a new file in the project root directory and name it .env
- paste the following 2 lines of code -
        
        `DATABASE_URL="postgresql+psycopg2://admin:12345@localhost:5432/piano_tech_client_db"`


        `JWT_SECRET_KEY="secretkey"`

- run the create and seed commands and run the applications

- open your preferred development tool, the app will be in development mode and routes can be accessed through port 8080


# R1 - 
### Identification of the problem you are trying to solve by building this particular app.

Managing client information can be difficult for Piano Technicians. Not being fully aware of how many instruments and where they are located can lead to wasted time when scheduling services and searching for the instruments on campus.

# R2 - 
### Why is it a problem that needs solving?

Creating a database and API to store and manage this information is required to make the technician's life easier. Having this information readily at hand when liaising with staff will greatly speed up the scheduling process and also improve client relations by providing clients with their own access to the information stored on the database.

# R3 -
### Why have you chosen this database system. What are the drawbacks compared to others?

PostgreSQL has been chosen for this projects, while it has some drawbacks, it is excellent for applications such as this project. PostgreSQL is an industry standard DBMS. It has many advantages that make it suitable for web development applications. PostgreSQL is open source, so completely free to use. Due to this, it also has a huge user base and lots of high quality documentation and community support is available at low cost or free. This can make PostgreSQL very appealing in comparison to similar options such as Oracle which can be costly. One disadvantage to being open source is that there are none of the benefits enjoyed by other DBMS' backed by companies. Ie, there is no warranty or liability backing up the product should something go wrong in use. 

PostgreSQL is catalog-driven, most relational DBMS store database information in systems catalogues. PostgreSQL is no different, though it stores much more information in these catalogues, including data types, functions and access methods. As these tables are accessible and modifiable by the user, the database can be extended readily and easily by the end user. This is in contrast to many DBMS which would need to have changes coded by developers in the source code. Users can also define their own composite data types making it extremely flexible for the developer to design their database exactly as they require for the application. 

PostgreSQL Is also relatively old, it has been in use for over 25 years. Having been around for this long with a large user base means it has developed into a very stable and secure system. While it is highly flexible and scalable, this can be at the cost of speed as it performs worse than some other DBMS. Non-relational document type database systems such as mongoDB have a faster raw speed for reading and writing though they store data differently and doesn't have the benefits of table based relational databases like postgreSQL. These factors must be taken into account when deciding the most appropriate DBMS for a given use case. 

PostgreSQL is fully ACID compliant. This set if characteristics, Atomicity, Consistency, Isolation and Durability ensure that the system is robust and all transactions are full and efficiently completed.  PostgreSQL also has code comments which can help in understanding what code is doing and speed up the learning process.
For the developer, PostgreSQL can be initially somewhat difficult to instal. Simpler systems such as MySQL are more straightforward to set up. Future updates require double storage and data export adding complexity to these processes. 

# R4 -
### Identify and discuss the key functionalities and benefits of an ORM

An ORM is critical to develop an API for a relational database within an object-oriented programming language. The ORM gives us the means to seamlessly convert class instances and attributes into tables and columns stored within the relational database. This completely removes the need to write SQL code as this is handled by the ORM. This can help speed up and simplify the development process as well as lowering the chance for programming errors. All of these benefits lead to decreased development cost.

ORMs also have built in automatic tools to minimise and help prevent sql injection attacks. These occur when malicious parties gain unauthorised access to sensitive data by intercepting and interfering with the sql queries. One way in which ORMs help lower this risk is that ORMs reduce explicit queries, making them much less vulnerable to attack.

# R5 -
### Document all endpoints for your API

The API has full CRUD functionality for all models - 

## Client Authorisation

The /client_auth route with the POST method is used to create a new user. It accepts JSON input for the Client model. These are - 
- name (string max 100 characters)
- address (string max 100 characters)
- phone (string max 300 characters)
- email (string max 100 characters)
- password

The email and password fields are required for a successful instance creation. The function will return the client instance without the password field.

Client login is via /client_auth/login. Post method is used to login a client. It accepts and requires JSON input of both email and password fields. Should the email not be found it will return a not found error. Should the password entered not correspond to the password (unencrypted) stored on the instance shared with the password, it will return an incorrect password error. 

Successful login will return the user email and a JWT access token. The client/technician status of the user is stored along with the user ID in the token.

## Technician Authorisation

The /auth_tech route with the POST method is used to create a new technician user. It accepts JSON input for the Client model. These are - 
- first_name (string max 100 characters)
- last_name (string max 100 characters)
- address (string max 100 characters)
- phone (string max 300 characters)
- email (string max 100 characters)
- password

The first_name, last_name, email and password fields are required for a successful instance creation. The function will return the client instance without the password field.

/auth_tech/login route with post method is used to login a Technician. It accepts and requires JSON input of both email and password fields. Should the email not be found associated with a technician instance, it will return a not found error. Should the password entered not correspond to the password (unencrypted) stored on the instance shared with the password, it will return an incorrect password error. 

Successful login will return the technician email and a JWT access token. The client/technician status of the user is stored along with the user ID in the token.

## Client Controller

/clients route with GET method will return all client instances on the database without password information. It is only accessible to requests containing technician tokens.

/clients/<int:id> route with GET method will return the instance of the client who's client_id matches the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. The function returns all client information in the client_schema without the password. The route is only accessible to requests containing technician tokens or the client token who's id matches the instance to be returned.

/clients/<int:id> route with PUT or PATCH method will update the client instance who's client_id matches the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. The function accepts JSON input of any field wishing to be updated. It returns the updated instance without the password field. The route is only accessible to requests containing technician tokens.

/clients/<int:id> route with DELETE method will delete the instance of the who's client_id matches the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. On successful deletion, it returns a message stating the client has been deleted. The route is only accessible to requests containing technician tokens.

## Technician Controller
/technicians route with GET method will return all technician instances on the database without password information. It is only accessible to requests containing technician tokens.

/technicians/<int:id> route with GET method will return the instance of the technician who's client_id matches the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. The function returns all technician information in the technician_schema without the password. The route is only accessible to requests containing technician tokens.

Technicians/<int:id>/clients route with GET method will return all client instances where the technician id corresponds to the integer provided in the dynamic route. If the integer doesn't correspond to any technician instance id's, it will return an error message that the technician was not found. If the technician id is not found on any client instances. A message will be returned saying the technician has no clients. The route is only accessible to requests containing technician tokens.

/technicians/<int:id> route with PUT or PATCH method will update the technician instance who's id matches the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. The function accepts JSON input of any field wishing to be updated. It returns the updated instance without the password field. The route is only accessible to requests containing technician tokens.

/technicians/<int:id> route with DELETE method will delete the instance of the who's id matches the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. On successful deletion, it returns a message stating the technician has been deleted. The route is only accessible to requests containing technician tokens.



## Client Instrument Controller
/client_instruments route with GET method returns all client_instrument instances on the database. It is only accessible to requests containing technician tokens.

/client_instruments/client/<int:id> route with GET method returns all client_instrument instances who's client_id corresponds to the integer provided in the dynamic route. If no client is found, it returns a not found error. It returns all information on the client_instrument schema. The route is only accessible to requests containing technician tokens or the client token who's id matches the instance to be returned.

/client_instruments/<int:id> route with DELETE method deletes the client_instrument instance who's client_instrument_id corresponds to the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. On successful deletion, it returns a message stating the client_instrument has been deleted. The route is only accessible to requests containing technician tokens.

/client_instruments/ route with POST method creates a new client_instrument instance. It accepts JSON input of fields in the client_instrument model.
- room (string, max 50 characters)
- serial_number (string, max 50 characters)
- model_id (integer)
- client_id (integer)
- finish_id (integer)
- colour_id (integer)

model and client id's are required fields. The function will return the client_instrument instance.

/client_instrument/<int:id> route with PUT or PATCH method updates the details on the client_instrument instance who's id matches the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. The function accepts JSON input of any field wishing to be updated. It returns the updated instance The route is only accessible to requests containing technician tokens.

## Colour Controller

/colours route with GET method returns all colour instances on the database. It is only accessible to requests containing technician tokens.

/colours route with POST method creates a new colour instance.It accepts JSON input of the colour_name field and it is only accessible to requests containing technician tokens. Should the colour name being registered already exist, it will return a message that it is already there.

/colours/<int:id> route with PUT or PATCH method updates a colour instance who's id corresponds to the integer provided in the dynamic route. It accepts JSON input of the colour_name field and it is only accessible to requests containing technician tokens. Should the integer not correspond to a colour instance, it will return a not found error message.

/colours/<int:id> route with DELETE method deletes the colour instance who's id corresponds to the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. On successful deletion, it returns a message stating the colour has been deleted. The route is only accessible to requests containing technician tokens.

## Country Controller

/country route with GET method returns all country instances on the database. It is only accessible to requests containing technician tokens.

/country route with POST method creates a new country instance.It accepts JSON input of the name field and it is only accessible to requests containing technician tokens. Should the country name being registered already exist, it will return a message that it is already there.

/country/<int:id> route with PUT or PATCH method updates a country instance who's id corresponds to the integer provided in the dynamic route. It accepts JSON input of the name field and it is only accessible to requests containing technician tokens. Should the integer not correspond to a country instance, it will return a not found error message.

/country/<int:id> route with DELETE method deletes the country instance who's id corresponds to the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. On successful deletion, it returns a message stating the country has been deleted. The route is only accessible to requests containing technician tokens.

## Finish Controller
/finish route with GET method returns all finish instances on the database. It is only accessible to requests containing technician tokens.

/finish route with POST method creates a new finish instance.It accepts JSON input of the name field and it is only accessible to requests containing technician tokens. Should the finish name being registered already exist, it will return a message that it is already there.

/finish/<int:id> route with PUT or PATCH method updates a finish instance who's id corresponds to the integer provided in the dynamic route. It accepts JSON input of the name field and it is only accessible to requests containing technician tokens. Should the integer not correspond to a finish instance, it will return a not found error message.

/finish/<int:id> route with DELETE method deletes the finish instance who's id corresponds to the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. On successful deletion, it returns a message stating the finish has been deleted. The route is only accessible to requests containing technician tokens.

## Type Controller
/type route with GET method returns all type instances on the database. It is only accessible to requests containing technician tokens.

/type route with POST method creates a new type instance.It accepts JSON input of the name field and it is only accessible to requests containing technician tokens. Should the type name being registered already exist, it will return a message that it is already there.

/type/<int:id> route with PUT or PATCH method updates a type instance who's id corresponds to the integer provided in the dynamic route. It accepts JSON input of the name field and it is only accessible to requests containing technician tokens. Should the integer not correspond to a type instance, it will return a not found error message.

/finish/<int:id> route with DELETE method deletes the type instance who's id corresponds to the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. On successful deletion, it returns a message stating the type has been deleted. The route is only accessible to requests containing technician tokens.

## Make controller
/make route with GET method returns all make instances on the database. It is only accessible to requests containing technician tokens.
	
/make route with POST method creates a new make instance. It accepts JSON input of the name (string max 50 characters, required) and country_id (integer) fields and it is only accessible to requests containing technician tokens. Should the make name being registered already exist, it will return a message that it is already there.

/make/<int:id> route with PUT or PATCH method updates the make instance who's id corresponds to the integer provided in the dynamic route.  It accepts JSON input of the name and country_id fields and it is only accessible to requests containing technician tokens. Should the integer not correspond to a make instance, it will return a not found error message.

/make/<int:id> route with DELETE method deletes the make instance who's id corresponds to the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. On successful deletion, it returns a message stating the make has been deleted. The route is only accessible to requests containing technician tokens.


## Model controller

/model route with GET method returns all model instances on the database. It is only accessible to requests containing technician tokens.

/model route with POST method creates a new model instance.It accepts JSON input of the model class fields. 
- name (string, max 50 characters)
- type_id (integer)
- make_id (integer)
- manufacture_country_id (integer)
It is only accessible to requests containing technician tokens. Should the model name being registered already exist, it will return a message that it is already there.

/model/<int:id> route with PUT or PATCH method updates the model instance who's id corresponds to the integer provided in the dynamic route.  It accepts JSON input of the make class fields listed in the post route. It is only accessible to requests containing technician tokens. Should the integer not correspond to a model instance, it will return a not found error message.

/model/<int:id> route with DELETE method deletes the model instance who's id corresponds to the integer provided in the dynamic route. Should an instance not be found, it will return a not found error. On successful deletion, it returns a message stating the model has been deleted. The route is only accessible to requests containing technician tokens.

# R6
### An ERD for your app

_______ put the link to ERD _______

# R7
### Detail any third party services that your app will use

## Flask

Flask is a python we development package with many tools to create web apps exclusively in python files. This application was created entirely with flask 
## Marshallow
Marshmallow is an object relational mapper, used here with flask to map databases and return json serialised python objects. It was used extensively in this project to validate and sanitise data.

## SQLAlcHemy 
SQAlALchemy is a python sql toolkit. It is an ORM that  generates the SQL statements from python functions and facilitates access to the database from within the flask app. 
## Postgresql
PostgreSQL is the relational database management system used for create the SQL database for this project.
## JWT web token 
Json web tokens are created using the flask_jwt_extended package. It is also used to extract user information from JWTs for user authentication. 
## Bcrypt
bcrytp is a password hashing function used to encrypt the passwords of users in the app.
## Psycopg2
psycopg2 is the database driver that works with SQLalchemy to send and receive the sql statements from to the database.

# R8 
### Describe your projects models in terms of the relationships they have with each other

## Technician and Client model:

The project has 2 user types, Technician and Client. The Technician and Client model's are used to store their data. Technician users have admin rights and Client users have restricted rights (they can only view their own data) This distinction is created by adding a string 'technician' or 'client' along with the id when creating the JWT on login. Permissions are granted using 2 decorators. One to validate technician users and another to validate technician users or client who's id correspond with a dynamic route's integer.

The client model's  entity technician_id is the foreign key for technician. The technician-client relation  back_populates to each other and is deleted across either table when a linked entry is removed from the database.

The client entity for the technician model is displayed as a list of fields as coded in the TechnicianSchema. This returns a nested list of the all client's linked to the technician.
The client to technician relation is not required when inputting data. 

## Client_instrument model:

The client_instrument model requires model_id and client_id foreign keys at minimum to create an instance. This is validated using marshmallow when a post request is made. If this validation is successful but the foreign key entered does not exist an IntegrityError is caught with the foreign key constraint and column returned so the client knows which foreign key was not found. This logic is used to check all foreign key entities on data being posted to the app. Foreign keys are also all restricted to 100,000 characters long (it is highly unlikely that a database will exceed this size for it's given use case. 

Model, Client, Finish and colour entities are returned as nested schemas for their respective table entries. 

## Country, type, colour and finish models:

These all function in the same way and exist to normalise data to be added to other models. They all back populate to their linked tables and delete across all tables when the entity is removed. 
The colour, type and finish schemas do not include the related models as this functionality is not required. Though country does return a nested list of related makes.

## Make model:
The make model requires a name to create an entity, the country foreign key is optional.

## Model model:
The model model requires the type and make foreign key ids in order to successfully create an entity. Type, make, manufacture_country and client_instruments all back populate to model entities on their related models.

# R9
### Discuss the database relations to be implemented in your application

As shown on the ERD project contains 9 models, these are -

- Technician model
- Client model
- Client_instrument model
- Country model
- Colour model
- Finish model
- Make model
- Model model
- Type model

## Technician model:
Technicians have the following relationship -
One to many with Clients - A technician can have many clients.

## Client model:
Clients have the following relationships - 
Many to one with Technician. 
One to many with Client_instrument model - one client can have many client_instruments

## Client_instrument model
The Client_instrument model acts as a join table, connecting models to clients while also including other specific data about the instrument. This data is primarily normalised with models that link only to the client_instrument model.

Client_instrument models have the following relationships 
- Many to one with models (many client_instruments can have the same model)
- Many to one with clients (many client_instruments can belong to one client)
- Many to one with finishes (many client_instruments can have the same finish)
- Many to one with colour (many client_instruments can have the same colour)

## Models model 
The Model model contains information for different piano models. While models could have join tables for the possible finishes and colours that the manufacturer makes available, this functionality is redundant for the scope of the app and is therefore left out.
 	
Model models have the following relationships -
- One to many with client_instruments (one model can be many client_instruments)
- Many to one with type (many models can have one type)
- Many to one with make (many models can belong to the same make)
- Many to one with countries (many models can be manufactured in the same country)

## Make model 
The make model contains the name and country of each piano maker.

Make models have the following relationships - 
Many to one with country (many makes can be headquartered in the same country)
One to many with models (one make builds many different models) 

## Type model 
The type model normalises Grand or Upright piano types and makes it possible for non-standard types to be added as necessary (harpsichords and square grands for example).

Type model has the following relationship - 
One to many with models (one type can the case for many models)

## Colour model
The colour model normalises colour options for individual client_instruments. 

Colour model has the following relationship - 
One to many with client_instruments (one colour can be found on many client_instruments)

## Finish model 
The finish model normalises the different finish coatings found on pianos for the client_instrument model.

Finish model has the following relationship - 
One to many with client_instrument (one finish can be found on many client_instruments)

## Country model 
The country model contains a list of countries used by the make model to assign a headquarter location for the maker and the model model to assign a country of manufacture for the model. Many makes have multiple factory locations around the world and all their instruments are not necessarily made in the same place. 

Country model has the following relationships - 
One to many with makes (one country can belong to many makes)
one to many with models (one country can have many makes built in it)

# R10
### Describe the way tasks are allocated and tracked in your project
The project tasks were managed with a Trello board. The board was broken up into lists containing cards for each main component of the app development. Some cards contained information for what was required for the task. 

As the project progressed, error handling list was added for these tasks and as CRUD functionality was developed, more cards were added to the Controller list.