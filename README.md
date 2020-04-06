# Blog-api Django rest framework

## Api functionality overview:

```
{
    "Register": "/api/auth/register/",
    "Login and obtain token": "/api/auth/token/",
    "Refresh token": "/api/auth/token/refresh/",
    "Post list": "api/posts/",
    "Post Create": "api/post/",
    "Post Delete, Update, Retrieve": "api/post/pk/",
    "Post like": "api/post/pk/like/",
    "Post unlike": "api/post/pk/unlike/",
    "Post like analitics": "api/post/pk/start/end/",
    "User activity": "api/user/pk/"
}
```

### Api authorization

"Register": "/api/auth/register/" - accept POST request with following data in json format:

```
{
    "username": "your_username",
    "email": "your_email",
    "password": "your_paswword"
}
```

"Login and obtain token": "/api/auth/token/" - accept POST request with following data in json format and return access and refresh tokens:

```
{
    "username": "your_username",
    "password": "your_paswword"
}
```

"Refresh token": "/api/auth/token/refresh/" - after token expired need refresh token, accept POST request with following data in json format:
{
"refresh": "your_refresh_token"
}

## Important

After get accses to token need add token in every request header:

```
Authorization:Bearer your_token
```

### Api routes

"Post list": "api/posts/" - accept GET request and return post list
"Post Create": "api/post/" - accept POST request with following data in json format:

```
{
    "title": "post_title",
    "body": "post_body"
}
```

and return :

```
{
    "id": post_id,
    "author": author_id,
    "title": "post_title",
    "body": "post_body",
    "created_at": "date",
    "likes": like_counter,
    "unlikes": unlike_counter
}
```

"Post Delete, Update, Retrieve": "api/post/pk/" - accept PUT(same json format like in "Post Create": "api/post/"), DELETE requests if you post author else only GET.

```
    pk - primary key(id)
```

"Post like": "api/post/pk/like/" - accept POST request and nothing return.
"Post unlike": "api/post/pk/unlike/" - accept POST request and nothing return.
"Post like analitics": "api/post/pk/start/end/" - accept GET request and return like information about post between two date(exclude end date), date format is YYYY-MM-DD and start date must be lower then end date. Request return data in json format:

```
[
    {
        "date": "2020-04-06",
        "likes": 1
    },
    {
        "date": "2020-04-05",
        "likes": 1
    }
]
```

"User activity": "api/user/pk/" - accept GET request and return information about user activity:

```
{
    "id": 1,
    "last_login": "2020-04-06T14:51:00.691962",
    "last_request": "2020-04-06T15:07:08.515599"
}
```

## Installation

1. Clone this repo or download zip file and extract.
2. Go to project folder run command and install all dependencies:

```
pip install -r requirements.txt
```

3. Final step make migrations, migrate and run server.
