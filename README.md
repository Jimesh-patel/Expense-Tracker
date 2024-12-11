# Expense Tracker

## Live Demo
Check out the live version of the Expense Tracker: [Expense Tracker](https://jimesh.pythonanywhere.com/)

---

## Overview
The Expense Tracker is a fully functional, real-time web application built using **Python** and **Django**. It simplifies expense management, allowing users to keep track of their individual and group expenses effectively. Designed with a focus on collaboration, it ensures that all user activities (like splitting expenses and settlements) are synchronized across linked accounts in real time.

### Key Features

1. **User Authentication**
   - Secure user login and registration using Django's built-in authentication system.
   - Password hashing and data encryption to ensure data security.

2. **Add Friends by Email**
   - Users can connect with others by adding them as friends using their email IDs.
   - Mutual linking of friend accounts for a seamless experience.

3. **Create Groups and Add Members**
   - Form groups for events, trips, or shared expenses.
   - Add multiple members to a group effortlessly.

4. **Add Expenses**
   - Record expenses manually for individual users or groups.
   - Automatically split expenses among group members based on predefined ratios or equal shares.
   - Real-time updates in linked user accounts.

5. **Settlement and Clearing Records**
   - Settle up with friends or group members directly within the app.
   - Automatically adjust balances and update records for all linked accounts.

### Unique Selling Points
- **Real-Time Synchronization**: All activities, such as splitting expenses or clearing dues, are immediately reflected in linked accounts.
- **User-Centric Design**: Intuitive UI/UX ensures ease of use for both individual and group expense management.
- **Scalability**: Designed to handle large user bases and multiple concurrent operations seamlessly.

---

## Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- SQLite3 (default) or any other preferred database

### Setup Steps
1. **Clone the Repository**
   ```bash
   git clone <repository-link>
   cd expense-tracker
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

---

## Project Structure
```
expense-tracker/
│
├── expense_tracker/       # Main project folder
│   ├── settings.py        # Django project settings
│   ├── urls.py            # URL configurations
│   └── wsgi.py            # WSGI entry point
│
├── users/                 # User management app
│   ├── models.py          # User and friend models
│   ├── views.py           # User authentication and friend management views
│   └── templates/         # User-related templates
│
├── groups/                # Group management app
│   ├── models.py          # Group and member models
│   ├── views.py           # Group creation and management views
│   └── templates/         # Group-related templates
│
├── expenses/              # Expense tracking app
│   ├── models.py          # Expense and settlement models
│   ├── views.py           # Expense and settlement handling views
│   └── templates/         # Expense-related templates
│
├── static/                # Static files (CSS, JS, images)
├── templates/             # Shared templates
└── requirements.txt       # List of dependencies
```

---

## Key Models
### User Model
Handles user information and relationships with friends.
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
```

### Group Model
Defines group details and member associations.
```python
class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

### Expense Model
Tracks expenses and splits.
```python
class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    split_details = models.JSONField()
```

---

## Future Enhancements
- **Graphical Analysis**: Add charts for expense summaries.
- **Notifications**: Notify users about dues or settlements.
- **Mobile App**: Extend functionality to Android and iOS platforms.

---

## Contributions
Feel free to fork the repository and submit pull requests for enhancements or bug fixes. For major changes, please open an issue to discuss the proposal first.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
