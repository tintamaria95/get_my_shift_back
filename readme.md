## Python App to automatically book climbing session with Dausport
inspired by Lucas M.

### Requirements

```console
conda install pip
conda create -n dausport
conda activate dausport
pip install Flask SQLAlchemy
```

*Tips: Navigate to host:port/protected to have a webpage describing the app API.*
(I didn't create a requirement.txt bc I'd first like to migrate to linux env later for convenient Docker dev)

It's necessary to create a file **/src/env.py** to store the ids of the main user and the port for the application.
It should contain a dictionnary -> AuthID = {'mail': str, 'password': str}, and the number ofthe port -> PORT: int

### Main files description (src)

- app.py: Flask application description
- dauphineAPI.py: Functions for website scraping
- db_function.py: Functions for Database manipulation (Add/Update/Remove Users/ Booked Climbing days)
- db_models.py: SQLAlchemy models
- main.py: Function to call that read the database and make the bookings for each user. (Can be called with CRON job for total automatisation)
- utils.py: Different useful functions to format dates, etc.
