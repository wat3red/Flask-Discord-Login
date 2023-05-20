# Flask-Discord-Login

Flask-Discord-Login is a web application that demonstrates the implementation of a login system using Discord accounts. This project showcases how to integrate Discord's authentication system into Flask-based web applications, allowing users to securely log in using their Discord credentials.

## Features

- Discord OAuth2 integration for login functionality.
- Seamless authentication flow with Discord accounts.
- Sample code and implementation guide for easy integration into your Flask projects.

## Installation

### Make sure you have Python 3.10.2 installed (all tests and development was done with it) https://www.python.org/downloads/release/python-3102/

1. Clone the repository:

   ```shell
   git clone https://github.com/wat3red/Flask-Discord-Login.git
2. Navigate to the project directory:

   ```shell
   cd Flask-Discord-Login

4. Install the required dependencies:
   ```shell
    pip install -r requirements.txt

5. Set up your Discord application:

Create a new Discord application on the [Discord Developer Portal](https://discord.com/developers/applications/). 
Configure the redirect URI for your application to http://localhost:5000/callback (or your desired callback URL). For tests, you may set Redirects to http://127.0.0.1:5000/callback

6. Fill the config.json file:
Replace the DISCORD_CLIENT_ID and DISCORD_CLIENT_SECRET placeholders in config.json with your Discord application's client ID and client secret, respectively. For tests, you may set DISCORD_REDIRECT_URI to http://127.0.0.1:5000/callback

> Note: Redirects on the Discord Developer Portal and DISCORD_REDIRECT_URI in config.json must be the same.

4. Start the app:

      ``` python
      python app.py
     
Open your web browser and navigate to http://localhost:5000 to see the Flask-Discord-Login application in action.

## Usage
Follow the provided implementation guide and sample code to integrate Flask-Discord-Login into your own Flask-based web applications.
Customize the application as per your requirements and build upon the provided functionality.
## Contributing
Contributions to Flask-Discord-Login are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository. 

`I am just learning how to develop web applications, so I would like to hear all the criticism towards my code.`

## License
MIT License

Feel free to modify and customize the content according to your project's specific details and requirements.
