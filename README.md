# last-fm-visualization

Software to visualize Last.FM data. Built with Python.

# Requirements

This project uses Python 3 and requires Redis to store all data.

This project also requires a Last.FM API key. To get one, simply go to the Last.FM api website and create a new application. Create an `apiKey.py` file in the main directory with `apiKey` and `apiSecret` variables. Here's an example:

    apiKey    = "YOUR_API_KEY_HERE"
    apiSecret = "YOUR_API_SECRET_HERE"

The project will include this file throughout to make requests as needed.
Make sure to add this file to your `.gitignore` file if you do make contributions to this repo. Again, please **do not** include this file in any commits you make to this repo or any others, as your API key would be compromised.
