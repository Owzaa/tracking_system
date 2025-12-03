# Scaffold Manager Django Project

## Project Overview

This project implements a Django application for managing scaffold components. It features a `ScaffoldComponent` model with various attributes like asset code, name, category, weight, condition, site, inspection dates, and usage status. The application provides full CRUD (Create, Read, Update, Delete) functionality through a web interface, including a list view with filtering and pagination, and detailed views for individual components.

Key features include:
- **ScaffoldComponent Model**: Defines the structure and validations for scaffold components.
- **CRUD Operations**: Views, forms, and templates for managing components.
- **List View Enhancements**: Filtering by search query, site, category, condition, and in-use status; pagination; and summary counts by site and condition.
- **Robust Forms**: Custom validation logic for `weight_kg`, `length_mm`, and `next_inspection` dates.
- **Azure Deployment Ready**: Automated settings switching for production environment when deployed to Azure App Service.

## Setup Steps

To get this project up and running locally, follow these steps:

1.  **Clone the Repository (if applicable):**
    ```bash
    git clone <your-repo-link>
    cd <your-repo-name>
    ```

2.  **Create and Activate a Python Virtual Environment:**
    ```bash
    python -m venv env
    # On Windows:
    .\env\Scripts\activate
    # On macOS/Linux:
    source env/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install Django
    ```
    *(Note: If you plan to use WhiteNoise for static files in production, also `pip install whitenoise`)*

4.  **Apply Database Migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser (for Admin access):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin user.

6.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

7.  **Access the Application:**
    Open your web browser and navigate to:
    -   [http://127.0.0.1:8000/assets/](http://127.0.0.1:8000/assets/) (for the Scaffold Component list)
    -   [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (for the Django Admin panel)

## Folder Structure

The project follows a standard Django project/app layout:

```
.
├── manage.py
├── scaffold_manager/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   └── base.html
└── workorders/
    ├── __init__.py
    ├── migrations/
    ├── models.py
    ├── forms.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    └── templates/
        └── workorders/
            ├── scaffold_component_list.html
            ├── scaffold_component_form.html
            ├── scaffold_component_detail.html
            └── scaffold_component_confirm_delete.html
```

## Azure Auto-Production Settings Switch

This project is configured to automatically switch to production settings when deployed to Azure App Service.

### How it Works:

1.  A flag `AUTO_PROD_ON_AZURE` is set to `True` in `scaffold_manager/settings/base.py`.
2.  The `scaffold_manager/settings/__init__.py` file detects if the application is running on Azure by checking for the presence of Azure-specific environment variables (e.g., `WEBSITE_SITE_NAME` or `WEBSITE_INSTANCE_ID`) or a custom environment variable `AZURE_DEPLOYMENT` set to "1".
3.  If `AUTO_PROD_ON_AZURE` is `True` and an Azure environment is detected, `settings/prod.py` is loaded. Otherwise, `settings/dev.py` is loaded.

### Configuration on Azure App Service:

To enable production settings on Azure, you need to configure the following environment variables in your Azure App Service Configuration:

*   **`AZURE_DEPLOYMENT`**: Set to `1`. This is the custom variable used for detection.
*   **`SECRET_KEY`**: Provide a strong, unique secret key for your production environment.
    Example: `SECRET_KEY = your_very_long_and_secret_key`
*   **`ALLOWED_HOSTS`**: A comma-separated list of hostnames that your Django app can serve. This *must* include your Azure App Service domain (e.g., `myapp.azurewebsites.net`).
    Example: `ALLOWED_HOSTS = myapp.azurewebsites.net,www.myapp.com`

### Production Settings Expectations:

When `settings/prod.py` is active:
*   `DEBUG = False`
*   `ALLOWED_HOSTS` is configured from the environment variable.
*   `SECRET_KEY` is loaded from the environment variable.
*   `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` for enhanced security over HTTPS.
*   `STATIC_ROOT` is set to `BASE_DIR / 'staticfiles'` for static file collection. You may need to configure a static file server (e.g., WhiteNoise) or Azure's built-in static file handling.

### Quick Check for Production Mode on Azure:

After deploying to Azure and configuring the environment variables:
1.  Open your Azure App Service URL (e.g., `https://myapp.azurewebsites.net/assets/`).
2.  Attempt to trigger an action that would normally display Django's debug information (e.g., access a non-existent URL). If `DEBUG = False` is active, you should see a generic "Page Not Found" error page, not Django's detailed debug page.

## Running Tests

To run the unit tests for the `workorders` app:

```bash
python manage.py test workorders
```

## Commit Hygiene

Meaningful commit messages have been used to track changes, such as "Add model and validations" or "Implement list filters and pagination".

## License

(Add your license information here, e.g., MIT, Apache 2.0, etc.)
