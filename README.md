# ProjectKR-SW

To start running this application, you need Python installed on your computer.

First, download all the required packages:

    pip install -r requirements.txt

If you prefer to display the results in the terminal instead of creating a playlist, you can skip the optional steps below.

# (OPTIONAL) Creating a Spotify Playlist
If you want the results displayed in a Spotify playlist, you'll need to create an account on Spotify's

    https://developer.spotify.com/

# (OPTIONAL)
Once you've registered, go to the dashboard and create an app to obtain your `CLIENT_ID` and `CLIENT_SECRET`. Store these, along with your `REDIRECT_URI` and `SKIP_SPOTIFY=0`, in a local `.env` file in the main directory. Your .env file should look like this:

    CLIENT_ID=9c1ab41...
    CLIENT_SECRET=d236ee4...
    REDIRECT_URI=YOUR_REDIRECT_URI
    SKIP_SPOTIFY=0

# Running the Application
To run the application, simply use the following command:

    python .src/main.py
    
When the application finishes, you will either receive a Spotify playlist on your account or see the results displayed in the terminal.
