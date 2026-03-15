import json
import logging
import os
import socket
import threading
import urllib.error
import urllib.request
import uuid

logger = logging.getLogger(__name__)

_bb_config = None


def _load_bluebubbles_config():
    """從 openclaw-personal .env 讀取 BlueBubbles 設定。"""
    global _bb_config
    if _bb_config is not None:
        return _bb_config

    for env_path in ('/host_home/.openclaw/.env', '/host_home/.openclaw-personal/.env'):
        if os.path.exists(env_path):
            break
    config = {}
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        logger.warning('BlueBubbles .env not found (tried ~/.openclaw and ~/.openclaw-personal)')
        return None

    url = config.get('BLUEBUBBLES_URL')
    password = config.get('BLUEBUBBLES_PASSWORD')
    if not url or not password:
        logger.warning('BLUEBUBBLES_URL or BLUEBUBBLES_PASSWORD not found in %s', env_path)
        return None

    _bb_config = {'url': url, 'password': password}
    return _bb_config


def _send_imessage(recipient, message):
    """透過 BlueBubbles API 發送 iMessage。"""
    config = _load_bluebubbles_config()
    if not config:
        logger.error('BlueBubbles not configured, skipping notification')
        return False

    chat_guid = f'iMessage;-;{recipient}'
    temp_guid = f'temp-{uuid.uuid4()}'

    payload = json.dumps({
        'chatGuid': chat_guid,
        'message': message,
        'method': 'apple-script',
        'tempGuid': temp_guid,
    }).encode('utf-8')

    url = f"{config['url']}/api/v1/message/text?password={config['password']}"
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return 200 <= resp.status < 300
    except urllib.error.HTTPError as e:
        # apple-script method 常回 500，但訊息實際已送出
        if e.code == 500:
            logger.info('BlueBubbles returned 500 (apple-script method, message likely sent)')
            return True
        logger.error('BlueBubbles HTTP error: %d', e.code)
        return False
    except urllib.error.URLError as e:
        # Timeout — apple-script method 常見，訊息通常已送出
        if isinstance(e.reason, socket.timeout) or 'timed out' in str(e.reason):
            logger.info('BlueBubbles timeout (apple-script method, message likely sent)')
            return True
        logger.error('BlueBubbles URL error: %s', e.reason)
        return False
    except socket.timeout:
        # socket.timeout 可能不經 URLError 直接拋出
        logger.info('BlueBubbles timeout (apple-script method, message likely sent)')
        return True
    except Exception as e:
        logger.error('Failed to send iMessage: %s', e)
        return False


def notify_task_result(task_name, status, duration_secs, trigger_type, stderr=None):
    """任務執行完畢後發送 iMessage 通知（背景執行緒）。"""
    recipient = os.environ.get('IMESSAGE_NOTIFY_RECIPIENT')
    if not recipient:
        return

    status_icon = {'success': '\u2705', 'failed': '\u274c', 'timeout': '\u23f0'}.get(status, '\u2753')
    trigger = '排程' if trigger_type == 'scheduled' else '手動'

    msg = f'{status_icon} [{trigger}] {task_name}\n狀態: {status} | 耗時: {duration_secs:.1f}s'

    if status != 'success' and stderr:
        short_err = stderr[:200].strip()
        if short_err:
            msg += f'\n\n錯誤:\n{short_err}'

    # 背景送出，不阻塞任務流程
    t = threading.Thread(target=_send_imessage, args=(recipient, msg), daemon=True)
    t.start()
