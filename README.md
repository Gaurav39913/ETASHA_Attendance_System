# Flask User Authentication System

This project is a user authentication system built with Flask, featuring an admin control panel. It includes session management, password hashing, and a modular structure for easy maintenance and scalability.

## Features

- User registration and login
- Password reset functionality
- Admin dashboard for user management
- Session management for user authentication
- Password hashing for secure storage
- Modular structure with blueprints for authentication and admin functionalities

## Project Structure

```
flask-auth-system
├── app
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── models.py
│   ├── admin
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   ├── templates
│   │   ├── auth
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   └── reset_password.html
│   │   ├── admin
│   │   │   └── dashboard.html
│   │   └── base.html
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       └── scripts.js
│   └── main
│       ├── __init__.py
│       ├── routes.py
│       └── forms.py
├── migrations
├── tests
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_admin.py
│   └── test_main.py
├── .env
├── config.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-auth-system
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Set up the environment variables in the `.env` file.

6. Run the application:
   ```
   flask run
   ```

## Usage

- Navigate to `/auth/login` to log in.
- Navigate to `/auth/register` to create a new account.
- Admins can access the dashboard at `/admin/dashboard` to manage users.

## Testing

Run the tests using:
```
pytest
```

## License

This project is licensed under the MIT License.
