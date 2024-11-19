from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging

app=Flask(__name__)

# Initialize Firebase Admin SDK
cred=credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def send_notification(token, title, body):
    """
    Send a push notification using Firebase Cloud Messaging.

    Args:
        token (str): The device's FCM registration token.
        title (str): Title of the notification.
        body (str): Body of the notification.
    """
    try:
        message=messaging.Message(
            notification=messaging.Notification(
                title=title, body=body, ), token=token, )
        response=messaging.send(message)
        return response
    except Exception as e:
        return f"Error sending notification: {e}"


@app.route('/')
def hello_world():
    return 'Hello!'


@app.route("/send_notification", methods=["POST"])
def send_notification_route():
    data=request.json
    token=data.get("token")
    title=data.get("title")
    body=data.get("body")

    if not token or not title or not body:
        return jsonify({"error":"Token, title, and body are required"}), 400

    response=send_notification(token, title, body)
    return jsonify({"response":response})


if __name__ == '__main__':
    app.run()
