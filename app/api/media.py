from flask import Blueprint, jsonify, request
# from app.core.security import token_required
# from app.services import media_service

bp = Blueprint('media_api', __name__, url_prefix='/api/v1/media')

@bp.route('/generate-video-script', methods=['POST'])
# @token_required
def generate_video_script():
    """
    (M13) - توليد نص فيديو مع لوحة قصة.
    """
    # script_type = request.get_json().get('script_type') # e.g., 'tiktok', 'youtube'
    # topic = request.get_json().get('topic')
    # script = media_service.create_video_script(script_type, topic)
    return jsonify({"message": "Placeholder for generating video script"})

@bp.route('/text-to-speech', methods=['POST'])
# @token_required
def convert_text_to_speech():
    """
    (M14) - تحويل نص إلى ملف صوتي.
    """
    # text = request.get_json().get('text')
    # voice_id = request.get_json().get('voice_id')
    # audio_url = media_service.create_voiceover(text, voice_id)
    return jsonify({"message": "Placeholder for converting text to speech"})