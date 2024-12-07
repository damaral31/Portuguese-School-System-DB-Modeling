# <font size="65">Portuguese-School-System-DB-Modeling</font>

Trabalho realizado por:

* Afonso Coelho (FCUP_IACD:202305085)
* Diogo Amaral (FCUP_IACD:202305187) 
* Miguel Carvalho (FCUP_IACD:202305229)

<div style="padding: 10px;padding-left:5%">
<img src="img/Cienciasporto.png" style="float:left; height:75px;width:200px">
<img src="img/Feuporto.png" style="float:left ; height:75px; padding-left:20px;width:200px">
</div>

<div style="clear:both;"></div>

******


## About
This repository serves as the workspace for an assignment within the scope of the "Bases de Dados" *(Database)* course in the Artificial Intelligence and Data Science degree at FCUP/FEUP

## Assignment
The assignment starts with the modeling of a database for the Portuguese School System, namely students enrolled in the 2017/2018.
The dataset does have some peculiarities, such as:

* Schools that don't have belong to a grouping;
* Classes that don't belong to a school;
* Nullable fields (especially regarding the classes);
* And more...

Then, we were tasked with creating 10 questions regarding the database, and writing `sqlite3` queries as their answer.

Finally we were to create a web application based on Flask and Jinja2, to display various information regarding the database, adding additional functionality if wanted (such as a `Search` page, for example).

## Database
The dataset provided to us is a `.xlsx` file, containing the following columns:

* Academic year
* DGEEC entity code
* Entity
* DGEEC school code
* School
* Network
* DGEEC grouping code
* Grouping
* DGEEC headquarters school code
* Headquarters school
* NUTS II (2013)
* NUTS III (2013)
* NUTS II (2002)
* NUTS III (2002)
* District
* Municipality
* Nature
* Typology
* Orientation
* Level of education
* Study cycle
* Offer
* Organization
* Grade level
* Course
* Gender
* Number of enrolled students

**Please note that the name of the columns found in [AlunosMatriculados17.xlsx](\app\AlunosMatriculados17.xlsx) is written in Portuguese; Here we translated them to english for better understanding**


<div style="padding: 10px; text-align:center;">
<img src="img/Relacional.svg" style="height:1000px;width:1000px">
</div>
