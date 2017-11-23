# s2
Version 2 of the Cross Products set selection / song suggestions web app.

## Development server
1. Start the back-end server. From the `api` directory do  
```
export FLASK_APP=serve.py
flask run
```
2. Run `npm start` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Contributing
1. Do `npm run lint` before each commit you make.
2. After testing locally, do a deploy to your personal locker to test on athena.
3. Create a PR for all changes. Include a link to them live on athena.
4. After merging, deploy changes to the crossp locker.

## Build & Deploy
1. Run `nmp run build` to build the project.  
2. Do `./deploy_dev.sh yourkerb` to send to your `web_scripts/s2`. You can view your version of the site at `yourkerb.scripts.mit.edu/s2`.
3. Do `./deploy_prod.sh yourkerb` when you're ready to make your changes live.

## Database Configuration
When testing locally, you should put your MySQL database credentials in environment variables, as specified in `config.py`. In the athena locker, there exists a file `realconfig.py` that has the crossp SQL database credentials which is loaded automatically if present. In the future we should create a tool to initialize a personal database with dummy data for testing.
