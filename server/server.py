"""
Flask 服务器主程序
"""

import os
import webbrowser
import threading
from flask import Flask, send_from_directory
from flask_cors import CORS
from .api import api
from . import config

def create_app():
    """创建 Flask 应用"""
    # 获取静态文件目录路径
    static_folder = os.path.join(os.path.dirname(__file__), 'static')

    app = Flask(__name__, static_folder=static_folder)

    # 启用 CORS 支持跨域请求
    CORS(app)

    # 注册 API 蓝图
    app.register_blueprint(api, url_prefix='/api')

    # 根路由返回排行榜页面
    @app.route('/')
    def index():
        return send_from_directory(static_folder, 'index.html')

    return app


def main():
    """启动服务器"""
    app = create_app()

    # 构造访问地址
    url = f'http://localhost:{config.PORT}'

    print(f'Starting server on {config.HOST}:{config.PORT}')
    print(f'Access the server at {url}')
    print('Press Ctrl+C to stop the server')

    # 只在非 reloader 主进程中打开浏览器（避免 debug 模式下打开多个标签页）
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        def open_browser():
            print(f'Opening browser at {url}')
            webbrowser.open(url)

        # 使用定时器在1.5秒后打开浏览器
        timer = threading.Timer(1.5, open_browser)
        timer.daemon = True
        timer.start()

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )


if __name__ == '__main__':
    main()
