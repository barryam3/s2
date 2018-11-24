# s2
Version 2 of the Cross Products set selection / song suggestions web app.

## Running the App
Start both the GUI and API in separate terminals. Then, go to `localhost:4200` to view the GUI. The API is reachable at `localhost:5000`, and the app will automatically send requests there.

## Contributing
1. After testing locally, do a deploy to your personal locker to test on athena.
2. Create a PR for all changes. Include a link to them live on athena.
3. After merging, deploy changes to the crossp locker.

## Build & Deploy
*Be sure you have built the GUI first.*
1. Do `./deploy.sh` to send to your `web_scripts/s2`. You can view your version of the site at `yourkerb.scripts.mit.edu/s2`.
2. Do `./deploy.sh prod` when you're ready to make your changes live.
