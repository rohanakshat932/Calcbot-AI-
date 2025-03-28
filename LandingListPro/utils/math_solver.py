import sympy as sp
import numpy as np
import re
import logging
from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, solve, diff, integrate, simplify, expand, factor, limit

def solve_problem(problem_text, problem_type='general'):
    """
    Solve a mathematical problem using SymPy
    
    Args:
        problem_text (str): The math problem text
        problem_type (str): Type of problem (algebra, calculus, geometry, etc.)
        
    Returns:
        str: Solution to the problem
    """
    logging.debug(f"Solving {problem_type} problem: {problem_text}")
    
    try:
        # Clean up the input
        problem_text = problem_text.strip().lower()
        
        # Detect problem type from text if not specified or general
        if problem_type == 'general':
            problem_type = detect_problem_type(problem_text)
        
        # Solve based on problem type
        if 'solve' in problem_text and ('equation' in problem_text or '=' in problem_text):
            return solve_equation(problem_text)
            
        elif 'derivative' in problem_text or 'differentiate' in problem_text:
            return find_derivative(problem_text)
            
        elif 'integrate' in problem_text or 'integral' in problem_text:
            return find_integral(problem_text)
            
        elif 'simplify' in problem_text:
            return simplify_expression(problem_text)
            
        elif 'factor' in problem_text:
            return factor_expression(problem_text)
            
        elif 'expand' in problem_text:
            return expand_expression(problem_text)
            
        elif 'limit' in problem_text:
            return find_limit(problem_text)
            
        elif 'area' in problem_text and ('circle' in problem_text or 'square' in problem_text or 'triangle' in problem_text):
            return calculate_area(problem_text)
            
        elif 'volume' in problem_text:
            return calculate_volume(problem_text)
            
        else:
            # Default fallback - try to parse and evaluate
            return general_math_solution(problem_text)
            
    except Exception as e:
        logging.error(f"Error solving problem: {str(e)}")
        return f"I couldn't solve this problem. Error: {str(e)}"

def detect_problem_type(problem_text):
    """Detect the type of math problem from the text"""
    if any(term in problem_text for term in ['derivative', 'differentiate', 'slope']):
        return 'calculus'
    elif any(term in problem_text for term in ['integrate', 'integral', 'antiderivative']):
        return 'calculus'
    elif any(term in problem_text for term in ['solve', 'equation', 'find x', '=']):
        return 'algebra'
    elif any(term in problem_text for term in ['simplify', 'expand', 'factor']):
        return 'algebra'
    elif any(term in problem_text for term in ['limit', 'approaches']):
        return 'calculus'
    elif any(term in problem_text for term in ['area', 'perimeter', 'circle', 'triangle', 'square']):
        return 'geometry'
    elif any(term in problem_text for term in ['volume', 'surface area', 'sphere', 'cylinder', 'cube']):
        return 'geometry'
    else:
        return 'general'

def solve_equation(problem_text):
    """Solve an algebraic equation"""
    # Extract the equation from text
    equation_match = re.search(r'([^=]+=[^=]+)', problem_text)
    if equation_match:
        eq_str = equation_match.group(1)
        # Split by equals sign
        sides = eq_str.split('=')
        if len(sides) == 2:
            left, right = sides
            # Find the variable - default to x if not specified
            var_match = re.search(r'solve for ([a-z])', problem_text)
            var = var_match.group(1) if var_match else 'x'
            
            # Create the symbol and equation
            x = sp.symbols(var)
            equation = sp.Eq(sp.sympify(left), sp.sympify(right))
            solution = sp.solve(equation, x)
            
            if len(solution) == 1:
                return f"{var} = {solution[0]}"
            else:
                return f"{var} = {', '.join(str(sol) for sol in solution)}"
    
    # Fallback for more complex parsing
    try:
        # Try to extract variable
        var_match = re.search(r'solve for ([a-z])', problem_text)
        var = var_match.group(1) if var_match else 'x'
        x = sp.symbols(var)
        
        # Extract the equation by looking for patterns
        equation_str = re.sub(r'solve for [a-z]:', '', problem_text)
        equation_str = re.sub(r'solve for [a-z]', '', equation_str)
        equation_str = re.sub(r'solve', '', equation_str)
        
        # Now find an equation with equals sign
        equation_match = re.search(r'([^=]+=[^=]+)', equation_str)
        if equation_match:
            eq_str = equation_match.group(1)
            sides = eq_str.split('=')
            if len(sides) == 2:
                left, right = sides
                equation = sp.Eq(sp.sympify(left), sp.sympify(right))
                solution = sp.solve(equation, x)
                
                if len(solution) == 1:
                    return f"{var} = {solution[0]}"
                else:
                    return f"{var} = {', '.join(str(sol) for sol in solution)}"
    except Exception as e:
        logging.error(f"Error parsing equation: {str(e)}")
    
    return "I couldn't parse the equation properly. Please format it as 'solve for x: ax + b = c'"

def find_derivative(problem_text):
    """Find the derivative of a function"""
    # Extract the function
    function_match = re.search(r'f\(x\)\s*=\s*([^\s,]+)', problem_text)
    if not function_match:
        function_match = re.search(r'derivative of ([^,\.]+)', problem_text)
    
    if function_match:
        func_str = function_match.group(1)
        x = sp.symbols('x')
        try:
            func = sp.sympify(func_str)
            derivative = sp.diff(func, x)
            return f"f'(x) = {derivative}"
        except Exception as e:
            logging.error(f"Error finding derivative: {str(e)}")
    
    return "I couldn't identify the function to differentiate. Please format it as 'find the derivative of f(x) = ...'"

def find_integral(problem_text):
    """Find the integral of a function"""
    # Extract the function
    function_match = re.search(r'integral of ([^,\.]+)', problem_text)
    if not function_match:
        function_match = re.search(r'integrate ([^,\.]+)', problem_text)
    
    if function_match:
        func_str = function_match.group(1)
        x = sp.symbols('x')
        try:
            func = sp.sympify(func_str)
            integral = sp.integrate(func, x)
            return f"∫{func_str} dx = {integral} + C"
        except Exception as e:
            logging.error(f"Error finding integral: {str(e)}")
    
    return "I couldn't identify the function to integrate. Please format it as 'find the integral of ...' or 'integrate ...'"

def simplify_expression(problem_text):
    """Simplify a mathematical expression"""
    # Extract the expression
    expr_match = re.search(r'simplify ([^,\.]+)', problem_text)
    
    if expr_match:
        expr_str = expr_match.group(1)
        try:
            expr = sp.sympify(expr_str)
            simplified = sp.simplify(expr)
            return f"Simplified: {simplified}"
        except Exception as e:
            logging.error(f"Error simplifying expression: {str(e)}")
    
    return "I couldn't identify the expression to simplify. Please format it as 'simplify ...'"

def factor_expression(problem_text):
    """Factor a mathematical expression"""
    # Extract the expression
    expr_match = re.search(r'factor ([^,\.]+)', problem_text)
    
    if expr_match:
        expr_str = expr_match.group(1)
        try:
            expr = sp.sympify(expr_str)
            factored = sp.factor(expr)
            return f"Factored: {factored}"
        except Exception as e:
            logging.error(f"Error factoring expression: {str(e)}")
    
    return "I couldn't identify the expression to factor. Please format it as 'factor ...'"

def expand_expression(problem_text):
    """Expand a mathematical expression"""
    # Extract the expression
    expr_match = re.search(r'expand ([^,\.]+)', problem_text)
    
    if expr_match:
        expr_str = expr_match.group(1)
        try:
            expr = sp.sympify(expr_str)
            expanded = sp.expand(expr)
            return f"Expanded: {expanded}"
        except Exception as e:
            logging.error(f"Error expanding expression: {str(e)}")
    
    return "I couldn't identify the expression to expand. Please format it as 'expand ...'"

def find_limit(problem_text):
    """Find the limit of a function"""
    # Check for limit notation
    limit_match = re.search(r'limit of ([^as]+) as ([a-z]) approaches ([^\s,\.]+)', problem_text)
    
    if limit_match:
        func_str = limit_match.group(1)
        var = limit_match.group(2)
        point = limit_match.group(3)
        
        try:
            func = sp.sympify(func_str)
            var_sym = sp.symbols(var)
            point_val = sp.sympify(point)
            
            limit_val = sp.limit(func, var_sym, point_val)
            return f"lim({func_str}) as {var}→{point} = {limit_val}"
        except Exception as e:
            logging.error(f"Error finding limit: {str(e)}")
    
    return "I couldn't identify the limit problem. Please format it as 'limit of [expression] as [variable] approaches [value]'"

def calculate_area(problem_text):
    """Calculate area of geometric shapes"""
    # Check for circle
    circle_match = re.search(r'area of (a|the) circle with radius ([0-9.]+)', problem_text)
    if circle_match:
        radius = float(circle_match.group(2))
        area = np.pi * radius**2
        return f"Area of circle with radius {radius} = {radius}²π ≈ {area:.2f} square units"
    
    # Check for rectangle
    rect_match = re.search(r'area of (a|the) rectangle with (length|width) ([0-9.]+) and (length|width) ([0-9.]+)', problem_text)
    if rect_match:
        dim1 = float(rect_match.group(3))
        dim2 = float(rect_match.group(5))
        area = dim1 * dim2
        return f"Area of rectangle with dimensions {dim1} × {dim2} = {area} square units"
    
    # Check for triangle
    triangle_match = re.search(r'area of (a|the) triangle with base ([0-9.]+) and height ([0-9.]+)', problem_text)
    if triangle_match:
        base = float(triangle_match.group(2))
        height = float(triangle_match.group(3))
        area = 0.5 * base * height
        return f"Area of triangle with base {base} and height {height} = {area} square units"
    
    return "I couldn't identify the geometric shape to calculate the area. Please specify the shape and its dimensions."

def calculate_volume(problem_text):
    """Calculate volume of 3D shapes"""
    # Check for sphere
    sphere_match = re.search(r'volume of (a|the) sphere with radius ([0-9.]+)', problem_text)
    if sphere_match:
        radius = float(sphere_match.group(2))
        volume = (4/3) * np.pi * radius**3
        return f"Volume of sphere with radius {radius} = (4/3)π·{radius}³ ≈ {volume:.2f} cubic units"
    
    # Check for cube
    cube_match = re.search(r'volume of (a|the) cube with side ([0-9.]+)', problem_text)
    if cube_match:
        side = float(cube_match.group(2))
        volume = side**3
        return f"Volume of cube with side {side} = {volume} cubic units"
    
    # Check for cylinder
    cylinder_match = re.search(r'volume of (a|the) cylinder with radius ([0-9.]+) and height ([0-9.]+)', problem_text)
    if cylinder_match:
        radius = float(cylinder_match.group(2))
        height = float(cylinder_match.group(3))
        volume = np.pi * radius**2 * height
        return f"Volume of cylinder with radius {radius} and height {height} = π·{radius}²·{height} ≈ {volume:.2f} cubic units"
    
    return "I couldn't identify the 3D shape to calculate the volume. Please specify the shape and its dimensions."

def general_math_solution(problem_text):
    """General fallback math problem solver"""
    # Try to identify mathematical expressions or equations
    try:
        # Clean up the text
        cleaned_text = re.sub(r'(find|calculate|compute|what is|solve)', '', problem_text)
        cleaned_text = cleaned_text.strip()
        
        # Check if this is a basic arithmetic operation
        if all(c in "0123456789.+-*/^() " for c in cleaned_text):
            result = sp.sympify(cleaned_text)
            return f"Result: {result}"
            
        # Check for equations
        if '=' in cleaned_text:
            return solve_equation(problem_text)
            
        # Just try to evaluate as an expression
        expr = sp.sympify(cleaned_text)
        result = expr
        
        return f"Result: {result}"
        
    except Exception as e:
        logging.error(f"Error in general math solution: {str(e)}")
        return "I couldn't determine how to solve this problem. Please try reformulating it or specifying the type of math problem."
