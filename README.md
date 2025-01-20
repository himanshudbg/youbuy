# YouBuy E-commerce Platform

YouBuy is a modern e-commerce platform built with Django, designed to provide a seamless shopping experience with features like product filtering, cart management, and secure checkout.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Key Features Explained](#key-features-explained)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Product Browsing:** Filter products by category and price.
- **Cart Management:** Add, update, and remove items from the cart.
- **User Authentication:** Secure login and registration.
- **Responsive Design:** Mobile-friendly interface.
- **Order Management:** Address input and order placement.

## Tech Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** SQLite (default Django DB)
- **Icons:** Font Awesome
- **Fonts:** Rubik Mono One, Poppins

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/youbuy.git
   cd youbuy
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install django
   pip install Pillow  # For image handling
   ```

4. **Apply migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

## Key Features

### Product Management

- **Categories:** Products are categorized into Shoes, Smartphones, Clothes, and Watches.
- **Details:** Each product includes a name, price, description, and image.
- **Filtering:** Products can be filtered by category and price range.

### Shopping Cart

- **Add to Cart:** Users can add products to their cart.
- **Quantity Management:** Adjust quantities directly in the cart.
- **Cart Total:** Real-time calculation of the cart total.
- **Remove Items:** Option to remove items from the cart.

### User Authentication

- **Registration:** User registration with validation.
- **Login/Logout:** Secure login and logout functionality.
- **Protected Routes:** Cart and checkout routes are protected.

### Checkout Process

- **Address Collection:** Collect and validate user address information.
- **Order Summary:** Display a summary of the order before placement.
- **Mobile Validation:** Validate mobile numbers during address input.

## Contributing

1. **Fork the repository**
2. **Create your feature branch:** `git checkout -b feature/AmazingFeature`
3. **Commit your changes:** `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch:** `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Bootstrap:** For responsive design components.
- **Font Awesome:** For icons.
- **Google Fonts:** For typography.
