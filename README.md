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


---

## Installation

### Prerequisites
- Python 3.8+
- Django 4.0+

### Setup Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Jimesh-patel/ExpenseTracker
   cd ExpenseTracker
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
 

---

## Project Structure
```
ExpenseTracker/
│
├── ExpenseTracker/        # Main project folder
│   ├── settings.py        # Django project settings
│   ├── urls.py            # URL configurations
│   └── wsgi.py            # WSGI entry point
│
├── firstapp/              # Expense tracking app
│   ├── models.py          # Expense and settlement models
│   ├── views.py           # Expense and settlement handling views
│   └── urls.py         # Expense-related templates
│
├── static/                # Static files (CSS, JS, images)
└── templates/             # Shared templates
```
