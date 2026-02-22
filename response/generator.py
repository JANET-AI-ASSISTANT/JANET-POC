import re
import requests
from datetime import datetime
import sys

sys.path.append('..')
import config


class ResponseGenerator:
    def __init__(self, use_llm=True):
        self.use_llm = use_llm
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2:3b"  # or "llama3.2:1b"
        self.timers = {}

        # Test Ollama connection
        if self.use_llm:
            try:
                response = requests.post(
                    self.ollama_url,
                    json={
                        "model": self.model,
                        "prompt": "test",
                        "stream": False
                    },
                    timeout=5
                )
                if response.status_code == 200:
                    print("Ollama connected successfully")
                else:
                    print(f"Warning: Ollama returned status {response.status_code}")
                    self.use_llm = False
            except Exception as e:
                print(f"Warning: Could not connect to Ollama: {e}")
                print("Falling back to rule-based responses")
                self.use_llm = False

    def generate_response(self, text):
        """
        Generate response based on transcript
        Returns: response text string
        """
        text_lower = text.lower().strip()

        # Check if it's a special command that needs real-time data
        # Handle these with direct functions, not LLM

        # Time queries - need real-time
        if self._is_time_query(text_lower):
            return self._get_time_response()

        # Weather queries - need API call
        if self._is_weather_query(text_lower):
            return self._get_weather_response()

        # Timer commands - need to actually set timer
        if self._is_timer_command(text_lower):
            return self._handle_timer(text_lower)

        # For everything else, use LLM if available
        if self.use_llm:
            return self._get_llm_response(text)
        else:
            return self._get_fallback_response(text)

    def _get_llm_response(self, text):
        """Get response from Ollama"""
        try:
            # Build system prompt
            system_prompt = self._build_system_prompt()

            # Full prompt
            full_prompt = f"{system_prompt}\n\nUser: {text}\nJANET:"

            # Call Ollama
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "max_tokens": 150,
                        "stop": ["\nUser:", "\n\n"]
                    }
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                answer = result['response'].strip()

                # Clean up response
                answer = self._clean_llm_response(answer)

                return answer
            else:
                return "I'm having trouble thinking right now. Please try again."

        except requests.exceptions.Timeout:
            return "Sorry, that's taking too long to process. Please try again."
        except Exception as e:
            print(f"LLM error: {e}")
            return "I encountered an error. Please try again."

    def _build_system_prompt(self):
        """Build context-aware system prompt"""
        current_time = datetime.now().strftime("%I:%M %p")
        current_date = datetime.now().strftime("%A, %B %d, %Y")

        prompt = f"""You are JANET, a helpful local AI assistant. You are concise, friendly, and natural.

Current time: {current_time}
Current date: {current_date}

Guidelines:
- Keep responses SHORT (1-3 sentences maximum)
- Be conversational and natural
- Don't explain what you are or apologize
- Don't say "based on my knowledge" or similar disclaimers
- If asked about time/weather, remind user you can check those directly
- For calculations, just give the answer
- Be helpful but brief"""

        # Add timer context if any exist
        if self.timers:
            prompt += f"\n- User has {len(self.timers)} active timer(s)"

        return prompt

    def _clean_llm_response(self, response):
        """Clean up LLM response"""
        # Remove common unwanted patterns
        response = re.sub(r'^(JANET:|Assistant:|AI:)\s*', '', response, flags=re.IGNORECASE)

        # Remove markdown
        response = response.replace('**', '')

        # Remove extra whitespace
        response = ' '.join(response.split())

        # Limit length
        sentences = response.split('. ')
        if len(sentences) > 3:
            response = '. '.join(sentences[:3]) + '.'

        return response.strip()

    def _get_fallback_response(self, text):
        """Rule-based fallback if Ollama not available"""
        text_lower = text.lower()

        # Calculations
        if self._is_calculation(text_lower):
            return self._handle_calculation(text_lower)

        # Greetings
        if self._is_greeting(text_lower):
            return "Hello! How can I help you?"

        # Status
        if 'status' in text_lower or 'what do you have' in text_lower:
            if self.timers:
                return f"You have {len(self.timers)} active timer(s)"
            return "No active tasks right now"

        # Default
        return "I'm not sure how to help with that. Try asking about the time, weather, or setting a timer."

    # === Helper Functions (keep from original) ===

    def _is_time_query(self, text):
        patterns = ['what time', 'current time', 'what is the time', "what's the time"]
        return any(p in text for p in patterns)

    def _get_time_response(self):
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The time is {time_str}"

    def _is_weather_query(self, text):
        return 'weather' in text or 'temperature' in text

    def _get_weather_response(self):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': config.DEFAULT_CITY,
                'appid': config.OPENWEATHER_API_KEY,
                'units': 'metric'
            }

            response = requests.get(url, params=params, timeout=5)
            data = response.json()

            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return f"The weather in {config.DEFAULT_CITY} is {description} with a temperature of {temp:.1f} degrees celsius"
            else:
                return "Sorry, I couldn't fetch the weather right now"

        except Exception as e:
            print(f"Weather error: {e}")
            return "Sorry, I couldn't fetch the weather right now"

    def _is_timer_command(self, text):
        return 'timer' in text and ('set' in text or 'start' in text)

    def _handle_timer(self, text):
        match = re.search(r'(\d+)\s*(minute|second|hour)', text)
        if match:
            value = int(match.group(1))
            unit = match.group(2)

            if unit == 'second':
                seconds = value
            elif unit == 'minute':
                seconds = value * 60
            elif unit == 'hour':
                seconds = value * 3600

            timer_id = len(self.timers) + 1
            self.timers[timer_id] = {
                'duration': seconds,
                'unit': unit,
                'value': value
            }

            return f"Timer set for {value} {unit}{'s' if value > 1 else ''}"
        else:
            return "I couldn't understand the timer duration. Try saying 'set timer for 5 minutes'"

    def _is_calculation(self, text):
        return any(word in text for word in ['plus', 'minus', 'times', 'divided', 'calculate', 'what is'])

    def _handle_calculation(self, text):
        text = text.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/')

        match = re.search(r'(\d+\.?\d*)\s*([\+\-\*\/])\s*(\d+\.?\d*)', text)
        if match:
            try:
                num1 = float(match.group(1))
                op = match.group(2)
                num2 = float(match.group(3))

                if op == '+':
                    result = num1 + num2
                elif op == '-':
                    result = num1 - num2
                elif op == '*':
                    result = num1 * num2
                elif op == '/':
                    if num2 == 0:
                        return "Cannot divide by zero"
                    result = num1 / num2

                return f"The answer is {result}"
            except:
                pass

        return "I couldn't understand that calculation"

    def _is_greeting(self, text):
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        return any(g in text for g in greetings)