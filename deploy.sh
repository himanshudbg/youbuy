   #!/bin/bash

   # Activate the virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Apply migrations
   python manage.py migrate

   # Collect static files (if needed)
   python manage.py collectstatic --noinput

   # Start the Django development server
   python manage.py runserver
