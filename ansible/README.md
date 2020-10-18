# rowmate deployment


Create a `all` file under `/group_vars` and replace the `xxx`

```yml
db_name: 'xxx'
app_name: 'xxx'
client_id: 'xxx'
client_key: 'xxx'
app_domain: 'xxx'
api_domain: 'xxx'
admin_email: 'xxx'
jwt_secret: 'xxx'
reset_secret: 'xxx'
db_password: 'xxx'
db_url_string: 'xxx'
dbserver_password: 'xxx'
webserver_password: 'xxx'
appserver_password: 'xxx'
apiserver_password: 'xxx'
db_private_address: 'xxx'
app_private_address: 'xxx'
api_private_address: 'xxx'
general_password_salt: 'xxx'
smtp_username: 'xxx'
smtp_password: 'xxx'
smtp_server: 'xxx'
smtp_port: 'xxx'
smtp_tls: 'xxx'
smtp_ssl: 'xxx'
```


### Inventory

Create a `hosts` file under `/inventory` and replace the ip addresses

```ìni
[webserver]
127.0.0.1 ansible_user=root

[apiserver]
127.0.0.1 ansible_user=root

[appserver]
127.0.0.1 ansible_user=root

[dbserver]
127.0.0.1 ansible_user=root
```
