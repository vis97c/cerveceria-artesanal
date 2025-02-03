# La cerveceria artesanal

Proyecto de POO

```bash
# Start app
flask --app app run
```

## Setup

[Secret session key](https://stackoverflow.com/a/73818941/3304008)

Create a .env file with the "SECRET_KEY"

```bash
# Install packages
pip install -r requirements.txt
# Get secret session key (once)
python -c 'import secrets; print(secrets.token_hex())'
```
