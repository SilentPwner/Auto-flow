from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services import ai_service

bp = Blueprint('content_api', __name__)

@bp.route('/generate-template-content', methods=['POST'])
@login_required
def generate_from_template():
    data = request.get_json()
    template_type = data.get('template_type')
    context = data.get('context')

    if not template_type or not context:
        return jsonify({'error': 'Template type and context are required'}), 400
    
    try:
        # هنا يتم استدعاء طبقة الخدمات (العقل المدبر)
        generated_text = ai_service.generate_content_from_smart_template(template_type, context)
        # TODO: Log usage for the user's plan
        return jsonify({'generated_text': generated_text})
    except Exception as e:
        # Log the error properly in a real app
        print(e)
        return jsonify({'error': 'An error occurred while generating content.'}), 500