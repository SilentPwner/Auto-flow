from flask import Blueprint, jsonify, request
# from app.core.security import token_required, admin_required
# from app.services import user_service # سيتم إنشاؤه لاحقًا

bp = Blueprint('users_api', __name__, url_prefix='/api/v1/users')

@bp.route('/', methods=['GET'])
# @token_required
# @admin_required
def get_users():
    """
    (M4) - الحصول على قائمة بجميع المستخدمين. يتطلب صلاحيات المدير.
    """
    # page = request.args.get('page', 1, type=int)
    # per_page = request.args.get('per_page', 10, type=int)
    # users = user_service.get_all_users(page, per_page)
    return jsonify({"message": "Placeholder for getting all users"})

@bp.route('/<int:user_id>', methods=['GET'])
# @token_required
# @admin_required
def get_user(user_id):
    """
    (M4) - الحصول على تفاصيل مستخدم معين.
    """
    # user = user_service.get_user_by_id(user_id)
    return jsonify({"message": f"Placeholder for getting user {user_id}"})

@bp.route('/<int:user_id>', methods=['PUT'])
# @token_required
# @admin_required
def update_user(user_id):
    """
    (M4) - تحديث بيانات مستخدم (مثال: تغيير خطته أو جعله مديرًا).
    """
    # data = request.get_json()
    # updated_user = user_service.update_user(user_id, data)
    return jsonify({"message": f"Placeholder for updating user {user_id}"})