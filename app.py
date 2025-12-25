"""
Flask Web Application
Provides a simple UI for querying the RAG retrieval system
"""

from flask import Flask, request, render_template_string, jsonify
from retrieve import retrieve, RetrieverError
import config

app = Flask(__name__)

# HTML Template with improved styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant Reviews RAG Retrieval</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #c33;
        }
        
        .info {
            background: #e3f2fd;
            color: #1565c0;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #1565c0;
        }
        
        .results-header {
            margin-top: 30px;
            margin-bottom: 20px;
        }
        
        .results-header h2 {
            color: #333;
            font-size: 24px;
            margin-bottom: 5px;
        }
        
        .results-count {
            color: #666;
            font-size: 14px;
        }
        
        .result-card {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .result-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid #dee2e6;
        }
        
        .result-id {
            font-weight: 600;
            color: #667eea;
            font-size: 14px;
        }
        
        .result-score {
            display: inline-block;
            padding: 5px 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }
        
        .result-text {
            color: #333;
            line-height: 1.6;
            font-size: 15px;
        }
        
        .no-results {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        
        .example-queries {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
        }
        
        .example-queries h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 18px;
        }
        
        .example-queries ul {
            list-style: none;
        }
        
        .example-queries li {
            padding: 8px 0;
            color: #666;
        }
        
        .example-queries li:before {
            content: "→ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍽️ Restaurant Reviews RAG System</h1>
        <p class="subtitle">Search through restaurant reviews using semantic similarity</p>
        
        <form method="post" class="search-box">
            <input 
                type="text" 
                name="query" 
                placeholder="e.g., What do people say about the ice cream?" 
                value="{{ query if query else '' }}"
                autofocus
            >

            <button type="submit">Search</button>
        </form>
        
        {% if error %}
        <div class="error">
            <strong>Error:</strong> {{ error }}
        </div>
        {% endif %}
        
        {% if query and not error %}
            {% if results %}
            <div class="results-header">
                <h2>Search Results</h2>
                <p class="results-count">Found {{ results|length }} relevant review(s) for: <strong>"{{ query }}"</strong></p>
            </div>
            
            {% for r in results %}
            <div class="result-card">
                <div class="result-header">
                    <span class="result-id">{{ r.id }}</span>
                    <span class="result-score">Score: {{ r.score }}</span>
                </div>
                <div class="result-text">{{ r.text }}</div>
            </div>
            {% endfor %}
            
            {% else %}
            <div class="no-results">
                <h3>No results found</h3>
                <p>Try a different query or adjust the similarity threshold</p>
            </div>
            {% endif %}
        {% endif %}
        
        {% if not query %}
        <div class="example-queries">
            <h3>💡 Example Queries</h3>
            <ul>
                <li>What do people think about the ice cream?</li>
                <li>How is the service?</li>
                <li>What are people saying about the pizza?</li>
                <li>Any mentions of the atmosphere?</li>
            </ul>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route for the web interface
    """
    query = None
    results = None
    error = None
    top_k = None
    threshold = None
    
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        top_k = int(request.form.get("top_k", 5))
        threshold = float(request.form.get("threshold", 0.5))
        
        if not query:
            error = "Please enter a search query"
        else:
            try:
                results = retrieve(query, top_k=top_k, threshold=threshold)
            except RetrieverError as e:
                error = str(e)
            except Exception as e:
                error = f"An unexpected error occurred: {e}"
    
    return render_template_string(
        HTML_TEMPLATE,
        query=query,
        results=results,
        error=error,
        top_k=top_k,
        threshold=threshold
    )

@app.route("/api/search", methods=["POST"])
def api_search():
    """
    API endpoint for programmatic access
    """
    data = request.get_json()
    
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' parameter"}), 400
    
    query = data["query"].strip()
    
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400
    
    try:
        top_k = data.get("top_k", config.TOP_K)
        threshold = data.get("threshold", config.SIMILARITY_THRESHOLD)
        
        results = retrieve(query, top_k=top_k, threshold=threshold)
        
        return jsonify({
            "query": query,
            "results": results,
            "count": len(results)
        })
    
    except RetrieverError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@app.route("/health")
def health():
    """
    Health check endpoint
    """
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 Starting Flask Application")
    print("="*50)
    print(f"📊 Collection: {config.COLLECTION_NAME}")
    print(f"🔍 Top-K: {config.TOP_K}")
    print(f"📏 Threshold: {config.SIMILARITY_THRESHOLD}")
    print("="*50 + "\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)