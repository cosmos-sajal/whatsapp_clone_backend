# whatsapp_clone_backend

#### API Documentation
- https://documenter.getpostman.com/view/14221347/TVzVibak

#### How to do error logging using Sentry?
- Go to http://sentry.io/
- Register an account.
- Create a project under that account (choose the framework, in our case it's Django).
- Add the below at the top of your settings.py
```
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
```
- Now add this in your secrets.py. This will be provided when you will be creating the project on sentry.
```
sentry_sdk.init(
    dsn="dsn_link",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
```
- Now to rebuild the project, do `docker-compose build && docker-compose up`.
- Try hitting any API by adding print(1/0) as the first line of a view.
- You will receive a 500 in your response.
- Check sentry. You should be seeing something like below, if yes then you are done.

