#!/usr/bin/env python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0')
