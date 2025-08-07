# Django E-Commerce Project

This is a Django-based e-commerce project designed to manage an online store. The project includes features for both an admin panel and a customer panel, allowing for product management and customer interactions.

## Project Structure

```
django_ecommerce
├── manage.py
├── ecommerce_project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates
│   └── store
│       ├── base.html
│       ├── product_list.html
│       └── product_detail.html
└── README.md
```

## Features

- **Product Management**: Admins can add, edit, and delete products. Each product includes details such as name, price, description, image, and stock quantity.
- **Customer Interaction**: Customers can browse products, view details, and check availability.
- **Stock Management**: The system checks stock levels to inform customers whether products are available for purchase.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd django_ecommerce
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations to set up the database:
   ```
   python manage.py migrate
   ```

4. Create a superuser to access the admin panel:
   ```
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/` and the admin panel at `http://127.0.0.1:8000/admin/`.

## License

This project is licensed under the MIT License.