from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pytesseract
from PIL import Image
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database.medicine_db import create_medicine_connection
from database.user_db import create_user_connection
from database.order_db import create_order_connection

auth = Blueprint('auth', __name__)

# Admin credentials
ADMIN_EMAIL = "adminpharmcare@gmail.com"
ADMIN_PASSWORD = "admin@pharmcare"

@auth.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user is the admin
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user_role'] = 'admin'
            session['user_email'] = email
            flash('Welcome, Admin!', 'success')
            return redirect(url_for('auth.admin_dashboard'))

        # Otherwise, check for regular user credentials
        conn = create_user_connection()
        cursor = conn.cursor()
        try:
            # Fetch user by email
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[4], password):  # Password is in the 4th column
                session['user_id'] = user[0]  # Store user ID in session
                session['user_name'] = user[1]  # Store user name in session
                session['user_role'] = 'user'
                flash('Login successful!', 'success')
                return redirect(url_for('auth.user_dashboard'))
            else:
                flash('Invalid email or password.', 'danger')
        except sqlite3.Error as e:
            flash(f"An error occurred: {e}", 'danger')
        finally:
            conn.close()

    return render_template('login.html')

@auth.route('/admin/dashboard')
def admin_dashboard():
    """Render the admin dashboard."""
    if session.get('user_role') != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('admin_dashboard.html')

@auth.route('/admin/update-stock', methods=['GET', 'POST'])
def update_stock():
    """Handle updating or adding new medicines."""
    success_message = None  # Initialize success message
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        availability = request.form['availability']
        picture = request.files['picture']

        # Save the picture if provided
        picture_path = None
        if picture:
            picture_path = f'static/images/{picture.filename}'
            picture.save(picture_path)

        conn = create_medicine_connection()  # Use the correct connection
        cursor = conn.cursor()
        try:
            # Check if the medicine already exists
            cursor.execute('SELECT * FROM medicines WHERE name = ?', (name,))
            medicine = cursor.fetchone()

            if medicine:
                # Update existing medicine
                cursor.execute('''
                    UPDATE medicines
                    SET description = ?, picture = ?, price = ?, availability = ?
                    WHERE name = ?
                ''', (description, picture_path or medicine[3], price, availability, name))
                success_message = 'Medicine updated successfully!'
            else:
                # Add new medicine
                cursor.execute('''
                    INSERT INTO medicines (name, description, picture, price, availability)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, description, picture_path, price, availability))
                success_message = 'New medicine added successfully!'

            conn.commit()
        except sqlite3.Error as e:
            success_message = f"An error occurred: {e}"
        finally:
            conn.close()

    return render_template('update_stock.html', success_message=success_message)

@auth.route('/admin/view_stocks', methods=['GET', 'POST'])
def view_stocks():
    """Search and view medicines for both admin and user."""
    conn = create_medicine_connection()
    cursor = conn.cursor()
    medicines = []
    search_query = None

    try:
        if request.method == 'POST':
            # Get the search query from the form
            search_query = request.form['search_query']
            # Fetch medicines matching the search query
            cursor.execute('''
                SELECT id, name, description, picture, price, availability
                FROM medicines
                WHERE name LIKE ?
            ''', (f"%{search_query}%",))
        else:
            # Fetch all medicines if no search query is provided
            cursor.execute('SELECT id, name, description, picture, price, availability FROM medicines')

        medicines = cursor.fetchall()
        print("Fetched Medicines:", medicines)  # Debugging line
    except sqlite3.Error as e:
        flash(f"An error occurred: {e}", 'danger')
    finally:
        conn.close()

    # Pass medicines and search_query to the template
    return render_template('view_stocks.html', medicines=medicines, search_query=search_query)

@auth.route('/view-orders', methods=['GET', 'POST'])
def view_orders():
    """View and update orders."""
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('Unauthorized access! Only admins can view and update orders.', 'danger')
        return redirect(url_for('auth.login'))

    conn = create_order_connection()
    cursor = conn.cursor()
    orders = []

    try:
        # Fetch all orders with customer name and phone
        cursor.execute('''
            SELECT o.id, o.full_name, o.phone, o.medicine_name, o.quantity, o.total_price, o.order_date, o.status
            FROM orders o
            ORDER BY o.order_date DESC
        ''')
        orders = cursor.fetchall()

        # Debugging: Print the fetched orders
        print("Fetched Orders for Admin:", orders)

        # Handle status update
        if request.method == 'POST':
            order_id = request.form['order_id']
            new_status = request.form['status']

            # Update the order status
            cursor.execute('''
                UPDATE orders
                SET status = ?
                WHERE id = ?
            ''', (new_status, order_id))
            conn.commit()
            flash('Order status updated successfully!', 'success')
            return redirect(url_for('auth.view_orders'))
    except sqlite3.Error as e:
        flash(f"An error occurred while fetching or updating orders: {e}", 'danger')
    finally:
        conn.close()

    return render_template('view_orders.html', orders=orders)

@auth.route('/user/dashboard')
def user_dashboard():
    """Render the user dashboard."""
    if session.get('user_role') != 'user':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('auth.login'))

    # Retrieve extracted data from the session
    extracted_data = session.pop('extracted_data', None)

    return render_template('user_dashboard.html', extracted_data=extracted_data)

@auth.route('/user/search-medicine', methods=['GET', 'POST'])
def search_medicine():
    """Search and view medicines for both admin and user."""
    conn = create_medicine_connection()
    cursor = conn.cursor()
    medicines = []
    search_query = None

    try:
        if request.method == 'POST':
            # Get the search query from the form
            search_query = request.form['search_query']
            # Fetch medicines matching the search query
            cursor.execute('''
                SELECT id, name, description, picture, price, availability
                FROM medicines
                WHERE name LIKE ?
            ''', (f"%{search_query}%",))
        else:
            # Fetch all medicines if no search query is provided
            cursor.execute('SELECT id, name, description, picture, price, availability FROM medicines')

        medicines = cursor.fetchall()
        print("Fetched Medicines:", medicines)  # Debugging line
    except sqlite3.Error as e:
        flash(f"An error occurred: {e}", 'danger')
    finally:
        conn.close()

    # Pass medicines and search_query to the template
    return render_template('search_medicine.html', medicines=medicines, search_query=search_query)

import requests  # For making HTTP requests to FastAPI


@auth.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    """Add a medicine to the cart."""
    if 'cart' not in session:
        session['cart'] = []  # Initialize the cart if it doesn't exist

    medicine_id = request.form['medicine_id']

    # Prevent duplicate entries
    if medicine_id not in session['cart']:
        session['cart'].append(medicine_id)
        session.modified = True  # Mark the session as modified
        flash('Medicine added to cart!', 'success')
    else:
        flash('Medicine is already in your cart.', 'info')

    # Redirect to the cart page so the user can see their cart
    return redirect(url_for('auth.cart'))

@auth.route('/cart', methods=['GET', 'POST'])
def cart():
    """Display the cart page and handle order placement."""
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty.', 'info')
        return render_template('cart.html', medicines=[])

    conn = create_medicine_connection()
    cursor = conn.cursor()
    medicines = []

    try:
        placeholders = ', '.join(['?'] * len(session['cart']))
        query = f'''
        SELECT id, name, description, picture, price, availability
        FROM medicines
        WHERE id IN ({placeholders})
        '''
        cursor.execute(query, [int(mid) for mid in session['cart']])
        medicines = cursor.fetchall()
    except sqlite3.Error as e:
        flash(f"An error occurred while fetching cart items: {e}", 'danger')
    finally:
        conn.close()

    # Handle order placement
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            flash('You must be logged in to place an order.', 'danger')
            return redirect(url_for('auth.login'))

        # Fetch user details
        conn = create_user_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT full_name, phone FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        full_name, phone = user[0], user[1]
        conn.close()

        conn = create_order_connection()
        cursor = conn.cursor()

        try:
            for medicine in medicines:
                medicine_id = medicine[0]
                medicine_name = medicine[1]
                price = medicine[4]
                # Get quantity from form, default to 1 if not provided
                quantity = int(request.form.get(f'quantity_{medicine_id}', 1))
                total_price = float(price) * quantity

                cursor.execute('''
                    INSERT INTO orders (user_id, medicine_id, medicine_name, full_name, phone, quantity, total_price, order_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), 'Pending')
                ''', (user_id, medicine_id, medicine_name, full_name, phone, quantity, total_price))

            conn.commit()
            flash('Order placed successfully!', 'success')
            session.pop('cart', None)  # Clear the cart after placing the order
        except sqlite3.Error as e:
            flash(f"An error occurred while placing the order: {e}", 'danger')
        finally:
            conn.close()

        return redirect(url_for('auth.track_order'))

    return render_template('cart.html', medicines=medicines)

@auth.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    medicine_id = str(request.form['medicine_id'])
    if 'cart' in session and medicine_id in session['cart']:
        session['cart'].remove(medicine_id)
        session.modified = True
        flash('Item removed from cart.', 'info')
    return redirect(url_for('auth.cart'))


@auth.route('/track-order')
def track_order():
    """Track the user's orders."""
    if 'user_id' not in session:
        flash('You must be logged in to track your orders.', 'danger')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = create_order_connection()
    cursor = conn.cursor()
    orders = []

    try:
        # Fetch all orders for the logged-in user
        cursor.execute('''
            SELECT id, medicine_name, quantity, total_price, order_date, status
            FROM orders
            WHERE user_id = ?
            ORDER BY order_date DESC
        ''', (user_id,))
        orders = cursor.fetchall()

        # Debugging: Print the fetched orders
        print("Fetched Orders for User:", orders)
    except sqlite3.Error as e:
        flash(f"An error occurred while fetching orders: {e}", 'danger')
    finally:
        conn.close()

    return render_template('track_order.html', orders=orders)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        full_name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = create_user_connection()
        cursor = conn.cursor()
        try:
            # Insert new user into the database
            cursor.execute('''
                INSERT INTO users (full_name, email, phone, password)
                VALUES (?, ?, ?, ?)
            ''', (full_name, email, phone, hashed_password))
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Email already registered. Please use a different email.', 'danger')
        except sqlite3.Error as e:
            flash(f"An error occurred: {e}", 'danger')
        finally:
            conn.close()

    return render_template('register.html')

@auth.route('/logout')
def logout():
    """Log the user out and clear the session."""
    session.clear()  # Clear the session
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact Us page."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Here you could add logic to store the message or send an email
        flash('Thank you for contacting us! We will get back to you soon.', 'success')
        return redirect(url_for('auth.contact'))
    return render_template('contact.html')