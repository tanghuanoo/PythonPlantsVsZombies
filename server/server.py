"""
Flask 服务器主程序
"""

from flask import Flask
from flask_cors import CORS
from .api import api
from . import config

def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__)

    # 启用 CORS 支持跨域请求
    CORS(app)

    # 注册 API 蓝图
    app.register_blueprint(api, url_prefix='/api')

    return app


def main():
    """启动服务器"""
    app = create_app()

    print(f'Starting server on {config.HOST}:{config.PORT}')
    print(f'Access the server at http://{config.HOST}:{config.PORT}')
    print('Press Ctrl+C to stop the server')

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )


if __name__ == '__main__':
    main()
