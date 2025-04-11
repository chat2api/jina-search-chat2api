from flask import Flask, request, Response
import json
import requests

app = Flask(__name__)

JINA_API_URL = "https://deepsearch.jina.ai/v1/chat/completions"

@app.route('/v1/models', methods=['GET', 'HEAD'])
def list_models():
	# 将字典转换为 JSON 字符串
	data = {
			'data': [
				{
					'created': 1698785189,
					'id': 'jina-research',
					'owned_by': 'system'
				}
			]
		}
	json_data = json.dumps(data)
	# 创建 Response 对象，设置内容类型为 application/json
	return Response(json_data, mimetype='application/json')

@app.route('/v1/chat/completions', methods=['POST', 'OPTIONS'])
def chat_completions():
    if request.method == 'OPTIONS':
        # Handle preflight CORS request
        headers = {
            'Access-Control-Allow-Origin': 'https://search.jina.ai',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Origin, Referer, User-Agent, DNT',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # 构造Jina API请求参数
    data = request.json
    data['stream'] = True
    data['reasoning_effort'] = 'medium'  # 固定参数

    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://search.jina.ai',
        'Referer': 'https://search.jina.ai/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'DNT': '1',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Ch-Ua': '"Not:A-Brand";v="24", "Chromium";v="134"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }

    # 发送请求到Jina API并流式返回响应
    response = requests.post(
        JINA_API_URL,
        json=data,
        headers=headers,
        stream=True,
        timeout=30
    )

    # 处理响应头
    def generate():
        for line in response.iter_lines():
            if line:
                yield f"{line.decode('utf-8')}\n\n"

    # 设置响应头
    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }

    return Response(generate(), headers=headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True)
