bot_template = """
<div style="
    background-color: #f7f9fc;
    color: #343a40;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
    max-width: 80%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
">
    <strong>🤖 Bot:</strong>
    <p>{message}</p>
</div>
"""

user_template = """
<div style="
    background-color: #d1e7dd;
    color: #0f5132;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
    margin-left: auto;
    max-width: 80%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
">
    <strong>👤 You:</strong>
    <p>{message}</p>
</div>
"""

css_template = """
<style>
    body {
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f8f9fa;
    }

    .stChatContainer {
        display: flex;
        flex-direction: column;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .stChatInput {
        margin-top: 20px;
    }
</style>
"""
