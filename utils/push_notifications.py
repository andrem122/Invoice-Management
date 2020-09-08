import asyncio, os
from django.conf import settings
from itertools import starmap
from aioapns import APNs, NotificationRequest


async def send_push_notification(device_token, badge, alert = {}):
    apns_key_client = APNs(
        key=os.path.join(settings.BASE_DIR, 'logged_in_assets', 'AuthKey_X44S38MRBS.p8'),
        key_id=settings.IOS_KEY_ID, # Key ID
        team_id=settings.IOS_TEAM_ID, # Team ID
        topic=settings.IOS_APP_BUNDLE_ID,  # Bundle ID
        use_sandbox=True,
    )
    request = NotificationRequest(
        device_token=device_token,
        message = {
            "aps": {
                "alert": {
                    "title": alert["title"],
                    "body": alert["body"],
                    "selectedIndex": alert["selected_index"]
                },
                "badge": badge,
            }
        },
    )
    await apns_key_client.send_notification(request)
