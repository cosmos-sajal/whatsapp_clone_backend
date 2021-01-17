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

![alt text](https://raw.githubusercontent.com/cosmos-sajal/whatsapp_clone_backend/master/reference_images/sentry.png)

#### How to do application logging using Scalyr?
- Go to https://app.scalyr.com/
- Register your account.
- Verify your email.
- Choose setup using docker
- In your terminal run the following command to pull Scalyr's docker image `docker pull scalyr/scalyr-agent-docker-json`. This will pull an image of Scalyr logger in your system.
- While setting up on https://app.scalyr.com/help/install-agent-docker you will be asked to create a `api_key.json` in the root folder of your application. In our case it will be whatsapp_clone_backend root itself.
- Save the following -
```
{ 
  api_key: "your api key"
}
```
at root (i.e. at whatsapp_clone_backend itself)
- Then run the following in your terminal to start the docker scalyr agent
```
docker run -d --name scalyr-docker-agent \
-v /Users/cosmos/projects/whatsapp_clone_backend/api_key.json:/etc/scalyr-agent-2/agent.d/api_key.json \
-v /var/run/docker.sock:/var/scalyr/docker.sock \
-v /var/lib/docker/containers:/var/lib/docker/containers \
scalyr/scalyr-agent-docker-json
```
`Remeber to change /Users/cosmos/projects/whatsapp_clone_backend/api_key.json to your path`
- Now to rebuild the project, do `docker-compose build && docker-compose up`.
- Hit any API, you should be seeing the logs coming up on scalyr, follow below image to see the logs, if this comes, then you are done.
![alt text](https://raw.githubusercontent.com/cosmos-sajal/whatsapp_clone_backend/master/reference_images/scalyr1.png)

- Try to use search functionality of scalyr using the screeshot below.
![alt text](https://raw.githubusercontent.com/cosmos-sajal/whatsapp_clone_backend/master/reference_images/scalyr2.png)
