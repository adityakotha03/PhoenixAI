import requests

class FetchURLContent:
  """Fetch a URL and return raw HTML or extracted readable text."""
  def __init__(self, url):
    self.url = url
    self.html_content = None
    self.error_message = None
    self.max_charecters = 1000

  def run(self):
    try:
      response = requests.get(self.url)
      if response.status_code == 200:
          if len(response.text) <= self.max_charecters:
              self.html_content = response.text
          else:
              self.html_content = response.text[:self.max_charecters]
      else:
          self.error_message = f"Failed to fetch content, status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        self.error_message = f"An error occurred: {e}"

    result = {
        "url": self.url,
        "content": self.html_content,
        "error": self.error_message
    }
    return result

  @staticmethod
  def get_description():
      return "Fetch a URL and return raw HTML or extracted readable text."

  @staticmethod
  def get_definition() -> dict:
      description = {
          "type": "function",
          "function": {
              "name": "FetchURLContent",
              "description": "Fetch a URL via HTTP GET and return the raw HTML as text. If the request fails, return an error message.",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "url": {
                          "type": "string",
                          "description": "The fully-qualified URL to fetch (must start with http:// or https://)."
                      }
                  },
                  "required": ["url"]
              }
          }
      }
      return description
