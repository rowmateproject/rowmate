# rowmate private API


### Prerequisits


Create a dotenv file in to root foler

```env
APP_NAME="<default_app_name>"
DATABASE_URL="mongodb://localhost:27017"
JWT_SECRET="<your_json_webtoken_secret_here>"
RESET_SECRET="<your_password_reset_secret_here>"
ADMIN_EMAIL="<your_admin_mail_address>"
FRONTEND_URL="<your_frontend_url_here>"
SMTP_USERNAME="<your_smtp_mail_address>"
SMTP_PASSWORD="<your_smtp_password_address>"
SMTP_SERVER="<your_smtp_server"
SMTP_PORT=<your_smtp_port>
SMTP_TLS="false"
SMTP_SSL="true"
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
pip3 install -r requirements.txt --use-feature=2020-resolver
```


### Run

```bash
uvicorn asgi:app --reload
```


### Usage


Register a user account

```bash
curl -H "Content-Type: application/json" -X POST -d '{"name": "John Doe", "email": "me@example.com", "password": "test123"}' http://localhost:8000/auth/register
```


Login to a user account

```bash
curl -H "Content-Type: multipart/form-data" -F "username=me@example.com" -F "password=test123" -X POST http://localhost:8000/auth/jwt/login
```


Request password reset token

```bash
curl -H "Content-Type: application/json" -d '{"email": "me@example.com"}'  -X POST http://localhost:8000/auth/forgot-password
```


Reset password with token

```bash
curl -H "Content-Type: application/json" -d '{"token": "<reset_token>", "password": "demo123"}' -X POST http://localhost:8000/auth/reset-password
```


Return users information

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -X GET http://localhost:8000/users/me
```


Refresh users token

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -X GET http://localhost:8000/auth/jwt/refresh
```


Call a protected route

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -X GET http://localhost:8000/protected
```
