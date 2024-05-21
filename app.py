from flask import Flask, request, render_template, redirect, url_for, jsonify
import re

app = Flask(__name__)

lexicon = {
    'react': {
        'keywords': [
            'useState', 'useEffect', 'useContext', 'useReducer', 'useRef', 'useMemo', 'useCallback', 'useImperativeHandle', 'useLayoutEffect',
            'createElement', 'Fragment', 'Component', 'PureComponent', 'useState', 'useEffect', 'useContext', 'useReducer', 'useRef', 'useMemo',
            'useCallback', 'useImperativeHandle', 'useLayoutEffect', 'createContext', 'forwardRef', 'memo', 'Suspense', 'lazy', 'import', 'export',
            'default', 'return'
        ],
        'digits': r'\d+',
        'identifier': r'[a-zA-Z_$][a-zA-Z0-9_$]*',
        'symbols': r'[\[\]\{\}\(\)=+\-*/%,;.]'
    },
    'javascript': {
        'keywords': [
            'var', 'let', 'const', 'function', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return',
            'try', 'catch', 'finally', 'throw', 'class', 'extends', 'import', 'export', 'new', 'this', 'super', 'null', 'undefined', 'true', 'false', 'console'
        ],
        'digits': r'\d+',
        'identifier': r'[a-zA-Z_$][a-zA-Z0-9_$]*',
        'symbols': r'[\[\]\{\}\(\)=+\-*/%,;.]'
    },
    'sql': {
        'keywords': [
            'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'IN', 'LIKE', 'BETWEEN', 'ORDER BY', 'GROUP BY', 'HAVING', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN',
            'FULL JOIN', 'ON', 'DISTINCT', 'AS', 'INSERT INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE FROM', 'CREATE TABLE', 'ALTER TABLE', 'DROP TABLE',
            'PRIMARY KEY', 'FOREIGN KEY', 'REFERENCES', 'UNIQUE', 'INDEX', 'COUNT', 'SUM', 'AVG', 'MAX', 'MIN'
        ],
        'digits': r'\d+',
        'identifier': r'[a-zA-Z_$][a-zA-Z0-9_$]*',
        'symbols': r'[\[\]\{\}\(\)=+\-*/%,;.]'
    }

}

def analyze_code(code):
    tokens = []
    lines = code.split('\n')
    counts = {
        'PR': 0,
        'ID': 0,
        'CAD': 0,
        'NUM': 0,
        'SIMB': 0,
        'TIPO': 0,
        'react': 0,
        'javascript': 0,
        'sql': 0,
        'ERROR': 0
    }
    
    for line in lines:
        for word in line.split():
            token = {
                'value': word,
                'PR': '',
                'ID': '',
                'CAD': '',
                'NUM': '',
                'SIMB': '',
                'TIPO': '',
                'react': '',
                'javascript': '',
                'sql': '',
                'ERROR': ''
            }
            is_valid = False
            is_symbol = False

            for lang in lexicon:
                if word in lexicon[lang]['keywords']:
                    token['PR'] = 'X'
                    token[lang] = 'X'
                    is_valid = True
                    counts['PR'] += 1
                    counts[lang] += 1
                if re.fullmatch(lexicon[lang]['digits'], word):
                    token['NUM'] = 'X'
                    is_valid = True
                    counts['NUM'] += 1
                if re.fullmatch(lexicon[lang]['identifier'], word):
                    token['ID'] = 'X'
                    is_valid = True
                    counts['ID'] += 1
                if re.fullmatch(lexicon[lang]['symbols'], word):
                    token['SIMB'] = 'X'
                    is_valid = True
                    counts['SIMB'] += 1
                    is_symbol = True

            if token['PR']:
                token['TIPO'] = 'Palabra Reservada'
            elif token['ID']:
                token['TIPO'] = 'Identificador'
            elif token['NUM']:
                token['TIPO'] = 'Número'
            elif token['SIMB']:
                token['TIPO'] = 'Símbolo'
            else:
                token['ERROR'] = 'X'
                token['TIPO'] = 'Error'
                counts['ERROR'] += 1
            
            tokens.append(token)
    tokens.append(counts)
    
    return tokens


@app.route('/')
def index():
    return render_template('index.html', results=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form.get('code')
    
    if not code:
        return jsonify({"error": "Please provide code"}), 400
    
    results = analyze_code(code)
    return render_template('index.html', results=results, code=code)

@app.route('/clear_results', methods=['POST'])
def clear_results():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)