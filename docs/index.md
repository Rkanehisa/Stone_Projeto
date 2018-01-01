This page contains the documentation of the package Stone API.

#Instalation

pip install -r requirements.txt

```
This API was tested using Python 3.5 and Python 3.6
```

# Running it in localhost

```
python manage.py
```


## User Model

Example of user table on the database:

* 'id :: int'
* 'username :: str'
* 'password ::str'**
* 'limit :: float'
* 'user_limit :: float'
* 'cards :: foreing key to card table'

** The password column saves the password encrypted 



## How to register a User.

A user only needs an `user_name` and a `password`.

```
curl -H "Content-Type: application/json" -X POST -d '{"username":"username", "password":"something"}' http:/localhost:5000/register
```

It returns a JSON with the new user data. The user model also contains the wallet.


```
{
    "id": 1,
    "username": "username",
    "password": "$6$rounds=656000$W61u9GeoEcEZrtzE$EBS6S0M7qbCBsvW9RwYHPBr0XDwye2NCB/uGVTdLytf4TFuImDuyPGmxESfJw0QhWtagLjaktGe/e0yFWQfZG1",
    "limit": 0,
    "user limit": ,
    "spent_limit": 0
}
```

If the user already exists it will return:

```
{
    "Message": "user already exists"
}
```

## Authenticating users

Some operations like `GET`, `POST`, `DEL`, `PATCH` may require some form of authentication. After registering a user it's always good to get his `JWT_token`.

```
curl -H "Content-Type: application/json" -X POST -d '{}' http://localhost:5000/auth
```

gives us:

```
{
  "message": "Error while authorizing, you must include and Authorization Header."
}
```

-------

```
curl -H "Content-Type: application/json" -X POST -d '{"username":"username", "password":"user_password"}' http:/localhost:5000/auth
```

```
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTI0MjkxMzgsImlhdCI6MTUxMjQyODgzOCwibmJmIjoxNTEyNDI4ODM4LCJpZGVudGl0eSI6MX0.RS2yl6fS70KRA5KGpjqf9yDMBW3Gsn8XPQd5cnQJ33Q"
}
```

## Card Model

Example of card table on the database:

* 'id :: int'
* 'name :: str'
* 'number :: str'
* 'ccv :: str'
* 'due_date :: datetime'**
* 'expiration_date :: datetime'**
* 'limit :: float'
* 'spent_limit :: float'
* 'user_id :: foreign key to user table'

** The datatime format is Year/Month/Day

### POST

```
$ export ACCESS="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTI0MjkxMzgsImlhdCI6MTUxMjQyODgzOCwibmJmIjoxNTEyNDI4ODM4LCJpZGVudGl0eSI6MX0.RS2yl6fS70KRA5KGpjqf9yDMBW3Gsn8XPQd5cnQJ33Q"

$ curl -H "Authorization: Bearer $ACCESS" http://localhost:5000/card/0000 0000 0000 0000
{
    "username":"username",
    "name": "User Name",
    "number": "0000 0000 0000 0000",
    "ccv": "000",
    "due_date": "2018/12/31",
    "expiration_date": "2023/12/31",
    "limit": 5000.0
}
```


If the card already exists it will return:

```
{
    {"Message": "Card already exists"}
}
```

A card must belong to a user, if the user does not exists it will return the following error message:

```
{
    {"Message": "User does not exists"}
}
```

### PATCH

You can alter the limit of your wallet at any time, the new limit must be less or equal the sum of the limits from all cards:

```
curl -H "Content-Type: application/json" -X POST -d '{  "user_limit": 2000.0}' http:/localhost:5000/user/<username>/edit
```

```
{
    "id": 1,
    "username": "username",
    "password": "$6$rounds=656000$W61u9GeoEcEZrtzE$EBS6S0M7qbCBsvW9RwYHPBr0XDwye2NCB/uGVTdLytf4TFuImDuyPGmxESfJw0QhWtagLjaktGe/e0yFWQfZG1",
    "limit": 2000,
    "user limit": 2000,
    "spent_limit": 0
}
```

###DEL

You can delete a user at any time. Delete a user will also delete it's cards.

```
curl -H "Content-Type: application/json" -X DEL http:/localhost:5000/user/<username>
```

You can also delete a card from a user.

```
curl -H "Content-Type: application/json" -X DEL http:/localhost:5000/card/<number>
```

###Payment

To release credit for a payment you must use the method

```
curl -H "Content-Type: application/json" -X POST -d '{"user_id":1, "value": 500.0}' http:/localhost:5000/user/<username>/edit
```

The payment value must be less or equal the maximum limit in one card...

```
{
"message": "payment exceeds cards limits"
}
```

and must be less or equal the maximum limit defined by the user

```
{
"message": "payment exceeds user limit"
}
```

###Notes

This repo also contains an example database the 2 users, "Teste" and "Teste2" and two cards "6666 6666 6666 6666" and "6666 6666 6666 6667"