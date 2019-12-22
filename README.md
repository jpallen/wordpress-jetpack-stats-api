# Accessing the Wordpress Jetpack API

Note that the way Wordpress have implemented all of this is to allow a developer (i.e. DataKind) to create a public app (like a stats dashboard), which anyone can connect their Wordpress blog to. In our case, it will not be public, and there will only be one client and one blog, but that's why the process is more complex than it might seem is necessary.

## Create a Wordpress app

You need to create an application on wordpress.com which people will allow to have access to their blog. If you've ever logged in with GitHub, Facebook, etc and seen a screen that said something like 'Service ABC Ltd will get access to your email', then there is an 'app' behind that with the name 'Service ABC Ltd'. It provides a context for the authentication.

I would suggest creating a DataKind Developer Wordpress account to own the app. Or maybe it's an account for XR? Whoever will be maintaining this going forwards I think.

Then logged in as this account, visit https://developer.wordpress.com/apps/ and create an app. You'll need to fill in the following fields:

1. *Name*. Something like 'DataKind Stats Dashboard'
2. *Description*. Not sure if necessary, but I'd just use 'DataKind Stats Dashboard' again if so.
3. *Website URL*. Only for info, so `https://www.datakind.org/`?
4. *Redirect URLs*. This is where the user is sent back to with the data needed to get an API key, after saying yes to allowing the app to access their blog. We'll be running a local script to receive this request later on, so put in `http://datakindauth.localtunnel.me/callback` for now. We'll see how to set this up later.
5. *Javascript Origin*. I don't think this matters for our usage. If it insists on something, put in `https://example.com`.
6. *Type*. Select `Web`.

After creating the app, note down the 'client id' and 'client secret'.

## Set up server to receive authentication request

We'll run a small Python server/app, which is exposed to the public internet. This is what will handle the authentication requests to get an API token for a logged in user.

With the client id and secret from above, run the python script:

```bash
$ python auth_server.py --clientid=CLIENT_ID --clientsecret=CLIENT_SECRET --publicurl http://datakindauth.localtunnel.me
```

Install [localtunnel](https://localtunnel.github.io/www/) and in another terminal, use it to expose the python server to the public internet at `http://datakindauth.localtunnel.me`:

```bash
$ npx localtunnel --port 8976 --subdomain datakindauth
```

## Authenticating and getting an API key.

The client will need to have Jetpack installed on their blog, and it to be connected to wordpress.com. I would recommend that they do this via a single system account on wordpress.com, like `wordpress@rebellion.earth`, or `team@rebellion.earch`.

I would also recommend that they also create an separate DataKind account on their own blog which we will get an API key for. Then it is easier to track and modify the permissions we have.

As part of the auth process, they will need to make sure they are logged into wordpress.com as the system user, and their own blog admin panel as the DataKind user.

Unforunately, we don't have any options on our side to only request permissions for the stats, so it will need to be authorized against account that is limited. I'm a little unclear what options Wordpress provides here.

You can now ask the client (Hannah) to visit `http://datakindauth.localtunnel.me/auth` to kick of the authentication process and get an API key that acts in the context of their account and our app. After this is done, the python process will print out the blog_id and API key. Save these somewhere secure, it's what we'll use to access the stats API.

## Calling the API

An example API call is provided in `stats_api.py`, with the parameters from the auth process above:

```bash
$ python stats_api.py --blogid BLOG_ID --accesstoken ACCESS_TOKEN
```
