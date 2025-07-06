from flask import Flask, request, jsonify
from flask_cors import CORS
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import google.generativeai as genai
import os

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app)  # Enables CORS for all domains on all routes

# --- API Keys and Email ---
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
GEMINI_API_KEY = "AIzaSyCRB9CdMbwwszySZ6ZOFl9R_GSgviLcaqU"
FROM_EMAIL = "samhitayamsani@gmail.com"

# --- Configure Gemini ---
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# --- Agents and Tasks ---
class Task:
    def __init__(self, input):
        self.input = input

class Agent:
    def run(self, task: Task):
        raise NotImplementedError

class FriendlyEmailAgent(Agent):
    def run(self, task: Task):
        response = gemini_model.generate_content([f"Write a FRIENDLY SALES email for: {task.input}"])
        return response.text

class FormalEmailAgent(Agent):
    def run(self, task: Task):
        response = gemini_model.generate_content([f"Write a FORMAL SALES email for: {task.input}"])
        return response.text

class EmpatheticEmailAgent(Agent):
    def run(self, task: Task):
        response = gemini_model.generate_content([f"Write an EMPATHETIC SALES email for: {task.input}"])
        return response.text

class EvaluatorAgent(Agent):
    def run(self, task: Task):
        emails = task.input
        prompt = "Select the best sales email for tone, clarity, and persuasiveness. Reply with only the number (1, 2, or 3):\n"
        for idx, email in enumerate(emails):
            prompt += f"\nEmail {idx+1}:\n{email}\n"
        response = gemini_model.generate_content([prompt])
        return response.text.strip()

class SendEmailAgent(Agent):
    def run(self, task: Task):
        recipient, subject, body = task.input
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=recipient,
            subject=subject,
            plain_text_content=body
        )
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            return f"✅ Email sent! Status Code: {response.status_code}"
        except Exception as e:
            return f"❌ Error sending email: {e}"

# --- API Endpoint ---
@app.route("/send-email", methods=["POST"])
def handle_send_email():
    data = request.get_json()
    user_prompt = data.get("prompt")
    recipient_email = data.get("email")

    if not user_prompt or not recipient_email:
        return jsonify({"error": "Missing input fields"}), 400

    # Instantiate agents
    friendly_agent = FriendlyEmailAgent()
    formal_agent = FormalEmailAgent()
    empathetic_agent = EmpatheticEmailAgent()
    evaluator_agent = EvaluatorAgent()
    sender_agent = SendEmailAgent()

    # Generate emails
    email_1 = friendly_agent.run(Task(user_prompt))
    email_2 = formal_agent.run(Task(user_prompt))
    email_3 = empathetic_agent.run(Task(user_prompt))

    # Evaluate
    best_index = evaluator_agent.run(Task([email_1, email_2, email_3]))
    try:
        best_email = [email_1, email_2, email_3][int(best_index) - 1]
    except:
        return jsonify({"error": "Invalid evaluation output: " + best_index}), 500

    # Send Email
    result = sender_agent.run(Task([recipient_email, "Introducing Our New Product Line", best_email]))
    return jsonify({"message": result})

# --- Run Flask Server ---
if __name__ == "__main__":
    app.run(debug=True)
