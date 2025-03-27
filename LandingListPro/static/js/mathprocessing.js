/**
 * Math processing utility functions for the client-side
 * These functions are for validation and preview purposes only.
 * Actual math solving happens on the server side.
 */

/**
 * Validates if a string contains a well-formed mathematical expression
 * @param {string} expression - The math expression to validate
 * @return {boolean} - True if valid, false otherwise
 */
function isValidMathExpression(expression) {
    // Check for basic syntax errors like mismatched parentheses
    let parenCount = 0;
    for (let char of expression) {
        if (char === '(') parenCount++;
        if (char === ')') parenCount--;
        if (parenCount < 0) return false; // Too many closing parentheses
    }
    if (parenCount !== 0) return false; // Mismatched parentheses
    
    // Check for invalid operator combinations
    if (/[+\-*\/]{2,}/.test(expression)) return false; // Consecutive operators
    
    // Check for division by zero
    if (/\/\s*0/.test(expression)) return false;
    
    return true;
}

/**
 * Formats a raw math expression into a cleaner display version
 * @param {string} expression - Raw math expression
 * @return {string} - Formatted expression for display
 */
function formatMathExpression(expression) {
    // Replace multiplication symbol * with ×
    expression = expression.replace(/\*/g, '×');
    
    // Replace division symbol / with ÷
    expression = expression.replace(/\//g, '÷');
    
    // Format exponents like x^2 into x²
    expression = expression.replace(/\^2/g, '²');
    expression = expression.replace(/\^3/g, '³');
    
    // Format squared and cubed roots
    expression = expression.replace(/sqrt\(/g, '√(');
    expression = expression.replace(/cbrt\(/g, '∛(');
    
    return expression;
}

/**
 * Provides a basic preview of the math problem formatting
 * This is just for immediate feedback before sending to the server
 * @param {string} problemText - The problem text to preview
 * @return {string} - LaTeX formatted problem preview
 */
function generateProblemPreview(problemText) {
    // Basic detection of equation vs expression
    if (problemText.includes('=')) {
        // It's an equation
        return problemText.replace(/(\w+)\^(\d+)/g, '$1^{$2}');
    } else {
        // It's an expression
        return problemText.replace(/(\w+)\^(\d+)/g, '$1^{$2}')
                         .replace(/sqrt\(([^)]+)\)/g, '\\sqrt{$1}')
                         .replace(/cbrt\(([^)]+)\)/g, '\\sqrt[3]{$1}');
    }
}

/**
 * Detects the likely type of math problem from the text
 * @param {string} problemText - The problem text
 * @return {string} - The detected problem type
 */
function detectProblemType(problemText) {
    const text = problemText.toLowerCase();
    
    if (text.includes('derivative') || text.includes('differentiate') || 
        text.includes('slope') || text.match(/f'|f'/)) {
        return 'calculus';
    }
    
    if (text.includes('integrate') || text.includes('integral') || 
        text.includes('antiderivative')) {
        return 'calculus';
    }
    
    if (text.includes('limit') || text.includes('approaches') || 
        text.includes('tends to')) {
        return 'calculus';
    }
    
    if (text.includes('solve') || text.includes('find x') || 
        text.includes('find y') || text.includes('=')) {
        return 'algebra';
    }
    
    if (text.includes('simplify') || text.includes('expand') || 
        text.includes('factor')) {
        return 'algebra';
    }
    
    if (text.includes('area') || text.includes('perimeter') || 
        text.includes('circle') || text.includes('triangle') || 
        text.includes('square')) {
        return 'geometry';
    }
    
    if (text.includes('probability') || text.includes('chance') || 
        text.includes('odds') || text.includes('random')) {
        return 'probability';
    }
    
    // Default
    return 'general';
}

/**
 * Provides suggestions for similar problems based on the current input
 * @param {string} problemText - The current problem text
 * @param {string} problemType - The detected problem type
 * @return {Array} - Array of suggestion objects with text and type
 */
function getSuggestions(problemText, problemType) {
    const suggestions = [];
    
    if (problemType === 'algebra') {
        suggestions.push({
            text: 'Solve for x: 3x + 5 = 20',
            type: 'algebra'
        });
        suggestions.push({
            text: 'Solve the system of equations: 2x + y = 8, x - y = 1',
            type: 'algebra'
        });
    } else if (problemType === 'calculus') {
        suggestions.push({
            text: 'Find the derivative of f(x) = x³ + 2x² - 5x + 3',
            type: 'calculus'
        });
        suggestions.push({
            text: 'Calculate the integral of x²sin(x) dx',
            type: 'calculus'
        });
    } else if (problemType === 'geometry') {
        suggestions.push({
            text: 'Find the area of a circle with radius 6',
            type: 'geometry'
        });
        suggestions.push({
            text: 'Calculate the volume of a sphere with radius 3',
            type: 'geometry'
        });
    }
    
    return suggestions;
}

// Export functions if using modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        isValidMathExpression,
        formatMathExpression,
        generateProblemPreview,
        detectProblemType,
        getSuggestions
    };
}
