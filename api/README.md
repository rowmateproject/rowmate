# rowmate private API


### Prerequisits


Create a dotenv file in to root foler

```env
DATABASE_URL="mongodb://localhost:27017"
JWT_SECRET="<your_json_webtoken_secret_here>"
RESET_SECRET="<your_password_reset_secret_here>"
ADMIN_EMAIL="<your_admin_mail_address>"
```


### Setup

```bash
sudo apt install python3 python3-dev
sudo pip3 install virtualenv
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
```


### Dependencies

```python
pip3 install fastapi
pip3 install uvicorn
pip3 install pydantic
pip3 install python-dotenv
pip3 install fastapi-users
```


### Run

```bash
uvicorn main:app --reload
```


### Usage


Register a user account

```bash
curl -H "Content-Type: application/json" -X POST -d "{'email': 'me@example.com', 'password': 'test123'}" http://localhost:8000/auth/register
```


Login to a user account

```bash
curl -H "Content-Type: multipart/form-data" -X POST http://localhost:8000/auth/jwt/login -F "username=me@example.com" -F "password=test123"
```


Return users information

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -X GET http://localhost:8000/users/me
```


Refresh users token

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -X GET http://localhost:8000/auth/jwt/refresh
```


Return content from a protected route

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -X GET http://localhost:8000/protected
```
