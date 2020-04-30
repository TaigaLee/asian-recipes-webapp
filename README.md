# asian-recipes-webapp

Name = CharField()
Origin = CharField()
Ingredients = TextField()
Instructions = TextField()
(maybe) Time created = DateField()/TimeField()

## Users data table

![users](https://i.imgur.com/jtoHImQ.png)

Username = CharField()
email = CharField()
Password = CharField()

# Routes

/recipes
/users/login
/users/register
/users/logout
/recipes/ (POST)
/recipes/update (update)
/recipes (delete)
