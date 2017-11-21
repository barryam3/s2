# s2

Version 2 of the Cross Products set selection site.

## Contributing
Do `npm run lint` before committing.

## Development server

1. Start the back-end server. From the `api` directory do  
```
export FLASK_APP=index.py
flask run
```
2. Run `npm start` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Build & Deploy

Assuming you are hosting at mysite.com/s2/ with apache...  
1. Run `nmp run build` to build the project.  
2. Copy the contents of `dist` directly into `/s2/`
3. Copy `api` to `/s2/api
4. Copy `.htaccess` to `/s2/`

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).  
I have not made any tests yet.

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).
Before running the tests make sure you are serving the app via `ng serve`.  
I have not made any tests yet.
