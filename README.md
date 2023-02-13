# Reto guane 2023

### Requirements
Please, before reviewing this repository, read the document:  [Requirements Analysis and Identification](https://drive.google.com/file/d/17BHS-bfhtBEK3pTc85Rn06C1r0jI89nR/view?usp=sharing "Requirements Analysis and Identification") in order to familiarize yourself with the context of the problem and the scope defined for this challenge.

### Architecture
This source code implements the following architecture:
![](http://diegolatorre116.github.io/reto_guane/arquitectura.png)

### Database
The relational model of the built database is shown below:
![](http://diegolatorre116.github.io/reto_guane/db.png)

Considerations:
- The “project_collaborator” table represents the intermediate table of the many-to-many relationship between “project” and “collaborator”. Although the primary key of this table corresponds to the combination of both foreign keys (project_id, collaborator_id), due to configuration issues with the ORM used (Tortoise-ORM), the table was generated with its own primary key. However, a uniqueness constraint has been established to avoid duplicative registrations using the combination of both foreign keys."
- The "department" table was created thinking of differentiating the four departments present in Guane Enterprises: Operation, Development, Data Science and Product.
- The "job" table refers to the different positions that each department has. For example, Backend Developer, FrontEnd Developer, Data Scientist etc.

### Deploy using Docker
To deploy this project using docker make sure you have cloned this repository
```bash
$ git clone https://github.com/diegolatorre116/reto_guane_2023
```
and installed Docker.
Now move to the project root directory
```bash
$ mv reto_guane_2023
```
Unless otherwise stated, all the commands should be executed from the project root directory denoted as ~/.
```bash
$ docker compose up --build
```
The docker-compose.yml is configured to create an image of the application named *web* and a an image of PostgreSQL v14 named *db*. To see the application working visit the URI 0.0.0.0:8020/docs and you  will be able to start sending HTTP requests to the application via this nice interactive documentation view, brought to us automatically thanks to FastAPI integration with OpenAPI:

![](http://diegolatorre116.github.io/reto_guane/documentacion.png)

To get started, use the endpoint: /api/generate_data/

![](http://diegolatorre116.github.io/reto_guane/endpoint.png)

You should receive as a response from the api: "Done". We have created our first department :department_store: and first user :mage: in the database with the following information:
```markdown
**Department:**
name: Development
description: Software_Development
id: 1
```
```markdown
**User:**
username: guane
password: ironparadise16
role: C-LEVEL
email: guane@example.com
deparment_id: 1
```
This user will have access to all functionalities of the application.
Now, go to the button located in the upper right called "Authorize" and  authenticate with the user that we have just created in the database. Once you have authenticated, you will be able to use all endpoints of the api.

### Next steps
The next step to be executed in the current project is the construction of unit tests for the source code. All the endpoints have been implemented and have been checked for compliance with the items proposed in the functional and non-functional requirements identification phase. However, it is necessary to test the application to ensure that the component works correctly and as expected, therefore, the initial assembly has been left for the performance of such tests.
