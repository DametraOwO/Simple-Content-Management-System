# Custom MVC CMS Framework

A custom Content Management System built with a custom MVC framework using Flask.

## Features

- User Authentication (Login/Register)
- Content Management
- Event Calendar
- User Dashboard
- Settings Management
- Responsive Design
- Custom MVC Architecture

## Project Structure

```
.
├── core/                    # Core framework components
│   ├── controllers/        # Controllers
│   ├── models/            # Models
│   ├── views/             # Views
│   ├── config/            # Configuration
│   ├── database/          # Database setup
│   └── utils/             # Utility functions
├── static/                 # Static files (CSS, JS, images)
├── templates/             # HTML templates
├── instance/              # Instance-specific files
├── requirements.txt       # Python dependencies
└── run.py                # Application entry point
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
python run.py
```

## Usage

1. Register a new account at `/register`
2. Log in at `/login`
3. Access the dashboard at `/`
4. Manage content at `/content`
5. View calendar at `/calendar`
6. Update settings at `/settings`

## Development

- The application uses a custom MVC framework
- Models are defined in `core/models/`
- Controllers are defined in `core/controllers/`
- Views are stored in `templates/`
- Static files are in `static/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 