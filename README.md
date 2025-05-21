# NetFix

## Home Service Provider Platform

NetFix is a web application that connects homeowners with service providers for various home maintenance and repair needs. The platform allows customers to find, book, and review service providers, while enabling companies to list their services and manage customer requests.

![NetFix Logo](static/css/logo.png)

## Purpose

NetFix aims to simplify the process of finding reliable home service providers by creating a centralized platform where:

- Customers can discover services based on their needs
- Service providers can showcase their expertise and availability
- Both parties can communicate and coordinate service appointments efficiently

## Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- Git

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://learn.zone01kisumu.ke/git/weakinyi/netfix.git
cd netfix
```

2. **Create and activate a virtual environment**

For Linux/macOS:
```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

For Windows:
```bash
python -m venv myvenv
myvenv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up the database**

```bash
python manage.py migrate
```

5. **Create a superuser (admin)**

```bash
python manage.py createsuperuser
```

6. **Configure environment variables (optional)**

For production environments, create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Usage

### Starting the Development Server

```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

### Basic Navigation

- **Home Page**: Overview of available services
- **Services**: Browse and search for specific services
- **Registration**: Sign up as a customer or service provider
- **Profile**: Manage your account and service requests
- **Admin Panel**: Accessible at `/admin/` for site administrators

### Key Features

#### For Customers
- Browse services by category
- Request services with specific requirements
- Track service request status
- View service provider profiles and ratings

#### For Service Providers
- Create company profiles
- List available services with pricing
- Manage service requests
- Communicate with customers

#### For Administrators
- Manage users and service providers
- Monitor service requests
- Handle disputes and issues
- Generate reports on platform usage

## Testing

### Running Tests for Individual Apps

```bash
# Test the main app
python manage.py test main

# Test the services app
python manage.py test services

# Test the users app
python manage.py test users
```

### Running the Complete Test Suite

```bash
python manage.py test
```

### Interpreting Test Results

- Tests that pass will be marked with a `.`
- Tests that fail will be marked with an `F`
- Tests that raise errors will be marked with an `E`

A summary will be displayed at the end showing:
- Number of tests run
- Number of failures
- Number of errors
- Time taken to run the tests

### Test Coverage (optional)

To check test coverage:

```bash
coverage run --source='.' manage.py test
coverage report
```

## Contributing

We welcome contributions to NetFix! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the code style guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- [**Wendy Akinyi**](https://github.com/Wendy-Tabitha)

## Acknowledgments

- Django framework and community
- All contributors who have helped shape this project
- Our users for their valuable feedback
