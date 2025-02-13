from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
import os
import time

# 获取当前文件的绝对路径目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file(os.path.join(CURRENT_DIR, 'index.html'))

@app.route('/<path:path>')
def serve_static(path):
    try:
        # 检查是否是 API 请求
        if path.startswith('api/'):
            return jsonify({"error": "API endpoint not found"}), 404
            
        file_path = os.path.join(CURRENT_DIR, path)
        if os.path.exists(file_path):
            return send_file(file_path)
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chart/generate', methods=['POST'])
def generate_chart():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
            
        # 验证数据
        if len(data.get('labels', [])) < 2:
            return jsonify({"error": "At least 2 data points required"}), 400
            
        return jsonify({
            "success": True,
            "message": "Chart data received successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/_vercel/speed-insights/vitals', methods=['POST'])
def collect_vitals():
    try:
        data = request.get_json()
        # 这里可以添加数据处理逻辑
        print("Performance Data:", data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"服务器运行目录: {CURRENT_DIR}")
    app.run(host='0.0.0.0', port=5000, debug=True)
