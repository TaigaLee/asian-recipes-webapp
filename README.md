# asian-recipes-webapp

## Recipe data table

![recipes](https://i.imgur.com/s4quKd1.png)

Name = CharField() <br/>
Origin = CharField() <br/>
Ingredients = TextField() <br/>
Instructions = TextField() <br/>
(maybe) Time created = DateField()/TimeField()

## Users data table

![users](https://i.imgur.com/jtoHImQ.png)

Username = CharField() <br/>
email = CharField() <br/>
Password = CharField() <br/>

# Routes

/recipes <br/>
/users/login <br/>
/users/register <br/>
/users/logout <br/>
/recipes/ (POST) <br/>
/recipes/update (update) <br/>
/recipes (delete)
