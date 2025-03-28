import sympy
from flask import render_template, request, flash, redirect, url_for, jsonify, session
from app import app, db
from models import Problem, Feedback, WaitlistEntry
from utils.math_solver import solve_problem
import logging

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    """Endpoint to solve math problems"""
    problem_text = request.form.get('problem_text')
    problem_type = request.form.get('problem_type', 'general')
    
    if not problem_text:
        flash('Please enter a math problem to solve', 'danger')
        return redirect(url_for('index'))
    
    try:
        # Create a problem entry in the database
        problem = Problem(
            problem_text=problem_text,
            problem_type=problem_type,
            status='pending'
        )
        
        # If user is logged in, associate the problem with them
        if 'user_id' in session:
            problem.user_id = session['user_id']
        
        db.session.add(problem)
        db.session.commit()
        
        # Solve the problem using the math solver utility
        solution = solve_problem(problem_text, problem_type)
        
        # Update the problem entry with the solution
        problem.solution = solution
        problem.status = 'solved'
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'problem_id': problem.id,
            'solution': solution
        })
    
    except Exception as e:
        logging.error(f"Error solving problem: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"Unable to solve the problem: {str(e)}"
        }), 500

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form route"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if not all([name, email, message]):
            flash('Please fill in all required fields', 'danger')
            return redirect(url_for('contact'))
        
        try:
            feedback = Feedback(name=name, email=email, message=message)
            db.session.add(feedback)
            db.session.commit()
            flash('Your message has been sent! We will get back to you soon.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            logging.error(f"Error submitting feedback: {str(e)}")
            flash('There was an error sending your message. Please try again.', 'danger')
    
    return render_template('contact.html')

@app.route('/join_waitlist', methods=['POST'])
def join_waitlist():
    """Endpoint to join the waitlist"""
    email = request.form.get('email')
    
    if not email:
        flash('Please enter a valid email address', 'danger')
        return redirect(url_for('index'))
    
    try:
        # Check if email already exists
        existing_entry = WaitlistEntry.query.filter_by(email=email).first()
        if existing_entry:
            flash('This email is already on our waitlist!', 'info')
            return redirect(url_for('index'))
        
        # Add new waitlist entry
        waitlist_entry = WaitlistEntry(email=email)
        db.session.add(waitlist_entry)
        db.session.commit()
        
        flash('You have been added to our waitlist! We will notify you when Calcbot AI launches.', 'success')
        return redirect(url_for('index'))
    
    except Exception as e:
        logging.error(f"Error adding to waitlist: {str(e)}")
        flash('There was an error adding you to the waitlist. Please try again.', 'danger')
        return redirect(url_for('index'))

@app.route('/examples')
def examples():
    """Endpoint to get example problems and solutions"""
    examples = [
        {
            'problem': 'Solve for x: 2x + 3 = 7',
            'solution': 'x = 2',
            'type': 'algebra'
        },
        {
            'problem': 'Find the derivative of f(x) = x^2 + 3x - 2',
            'solution': 'f\'(x) = 2x + 3',
            'type': 'calculus'
        },
        {
            'problem': 'Find the area of a circle with radius 5',
            'solution': 'A = 25π ≈ 78.54',
            'type': 'geometry'
        },
        {
            'problem': 'Solve the system of equations: 3x + 2y = 12, x - y = 1',
            'solution': 'x = 3, y = 2',
            'type': 'algebra'
        },
    ]
    return jsonify(examples)

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500
