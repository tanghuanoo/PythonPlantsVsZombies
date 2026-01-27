"""
API 路由定义
"""

from flask import Blueprint, request, jsonify
from .database import Database

api = Blueprint('api', __name__)
db = Database()


@api.route('/health', methods=['GET'])
def health():
    """健康检查接口"""
    return jsonify({'status': 'ok'})


@api.route('/login', methods=['POST'])
def login():
    """
    登录/注册接口
    请求体: {"name": "张三", "employee_id": "E001"}
    返回: {"player_id": 1, "name": "张三", "employee_id": "E001"}
    """
    try:
        data = request.get_json()
        name = data.get('name')
        employee_id = data.get('employee_id')

        if not name or not employee_id:
            return jsonify({'error': '姓名和工号不能为空'}), 400

        player_id = db.get_or_create_player(name, employee_id)

        return jsonify({
            'player_id': player_id,
            'name': name,
            'employee_id': employee_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/submit_score', methods=['POST'])
def submit_score():
    """
    提交成绩接口
    请求体: {
        "player_id": 1,
        "score": 1500,
        "game_duration": 120000,
        "zombie_details": [
            {"zombie_type": "Zombie", "count": 10},
            {"zombie_type": "ConeheadZombie", "count": 5}
        ]
    }
    返回: {"game_record_id": 1, "rank": 5}
    """
    try:
        data = request.get_json()
        player_id = data.get('player_id')
        score = data.get('score')
        game_duration = data.get('game_duration')
        zombie_details = data.get('zombie_details', [])

        if not player_id or score is None or game_duration is None:
            return jsonify({'error': '缺少必要参数'}), 400

        game_record_id, rank = db.add_game_record(
            player_id, score, game_duration, zombie_details
        )

        return jsonify({
            'game_record_id': game_record_id,
            'rank': rank
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/leaderboard', methods=['GET'])
def leaderboard():
    """
    排行榜接口
    查询参数: limit (可选, 默认10)
    返回: {"leaderboard": [...]}
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        leaderboard_data = db.get_leaderboard(limit)

        return jsonify({
            'leaderboard': leaderboard_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/player_history', methods=['GET'])
def player_history():
    """
    玩家历史记录接口
    查询参数: player_id, limit (可选, 默认10)
    返回: {"history": [...]}
    """
    try:
        player_id = request.args.get('player_id', type=int)
        limit = request.args.get('limit', 10, type=int)

        if not player_id:
            return jsonify({'error': '缺少 player_id 参数'}), 400

        history_data = db.get_player_history(player_id, limit)

        return jsonify({
            'history': history_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
