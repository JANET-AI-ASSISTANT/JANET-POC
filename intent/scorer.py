import re


class IntentScorer:
    def __init__(self, threshold=30):
        self.threshold = threshold

        # Define patterns
        self.question_words = ['what', 'when', 'where', 'who', 'why', 'how', 'can', 'will', 'is', 'are', 'do', 'does']
        self.command_verbs = ['set', 'turn', 'remind', 'check', 'get', 'tell', 'show', 'play', 'stop', 'start', 'send']
        self.task_keywords = ['alarm', 'timer', 'weather', 'time', 'temperature', 'calendar', 'email', 'reminder', 'lights']

    def score_utterance(self, text):
        """
        Score an utterance to determine if it's directed at JANET
        Returns: (score, should_respond, details)
        """
        text_lower = text.lower().strip()
        score = 0
        details = []

        # 1. "Janet" mentioned (+50)
        if 'janet' in text_lower:
            score += 50
            details.append("'janet' mentioned: +50")

        # 2. Question format (+25)
        words = text_lower.split()
        if len(words) > 0 and words[0] in self.question_words:
            score += 25
            details.append(f"question word '{words[0]}': +25")

        # 3. Command format (+25)
        if len(words) > 0 and words[0] in self.command_verbs:
            score += 25
            details.append(f"command verb '{words[0]}': +25")

        # 4. Task keywords (+15)
        for keyword in self.task_keywords:
            if keyword in text_lower:
                score += 15
                details.append(f"task keyword '{keyword}': +15")
                break  # Only count once

        # 5. Second-person pronouns (+10)
        if re.search(r'\byou\b', text_lower):
            score += 10
            details.append("second-person 'you': +10")

        should_respond = score >= self.threshold

        return score, should_respond, details

    def should_respond(self, text):
        """Simple check - returns True if should respond"""
        score, should_respond, _ = self.score_utterance(text)
        return should_respond