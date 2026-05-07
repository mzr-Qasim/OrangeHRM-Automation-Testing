import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()


class JiraClient:

    def __init__(self):

        self.base_url = os.getenv("JIRA_BASE_URL")
        self.email = os.getenv("JIRA_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")
        self.project_key = os.getenv("JIRA_PROJECT_KEY")

        if not all([self.base_url, self.email, self.api_token, self.project_key]):
            raise ValueError("Missing Jira environment variables")

        self.auth = HTTPBasicAuth(self.email, self.api_token)

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def attach_screenshot(self, issue_key, file_path):

        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/attachments"

        headers = {
            "X-Atlassian-Token": "no-check"
        }

        try:
            with open(file_path, "rb") as file:

                requests.post(
                    url,
                    headers=headers,
                    auth=self.auth,
                    files={"file": file},
                    timeout=10
                )

        except Exception as e:
            print("⚠️ Screenshot upload failed:", e)

    def create_bug(self, summary, description, screenshot_path=None):

        url = f"{self.base_url}/rest/api/3/issue"

        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "issuetype": {"name": "Bug"},
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": str(description)
                                }
                            ]
                        }
                    ]
                }
            }
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                auth=self.auth,
                timeout=10
            )

            if response.status_code in [200, 201]:

                issue_key = response.json().get("key")
                print(f"✅ Jira Bug Created: {issue_key}")

                if screenshot_path:
                    self.attach_screenshot(issue_key, screenshot_path)

                return issue_key

            print("❌ Jira Failed:", response.text)

        except Exception as e:
            print("⚠️ Jira connection failed:", str(e))

        return None