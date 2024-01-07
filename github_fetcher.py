import os
import requests
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

TOKEN_GH = os.getenv("TOKEN_GH")


class Fetcher:
    def __init__(self, usernames):
        self.usernames = usernames

    def get_graphql_query(self, from_date: str, to_date: str, username: str):
        return {
            "query": """
              query userInfo($LOGIN: String!, $FROM: DateTime!, $TO: DateTime!) {
                user(login: $LOGIN) {
                  name
                  contributionsCollection(from: $FROM, to: $TO) {
                    contributionCalendar {
                      weeks {
                        contributionDays {
                          contributionCount
                          date
                        }
                      }
                    }
                  }
                }
              }
            """,
            "variables": {
                "LOGIN": username,
                "FROM": from_date,
                "TO": to_date,
            },
        }

    def fetch(self, graphql_query):
        headers = {
            "Authorization": f"Bearer {TOKEN_GH}",
        }
        response = requests.post('https://api.github.com/graphql', headers=headers, json=graphql_query)
        return response.json()

    def fetch_contributions_for_user(self, username):
        from_date = datetime(2024, 1, 1).isoformat()
        now = datetime.utcnow()
        to_date = now.isoformat()

        try:
            graphql_query = self.get_graphql_query(from_date, to_date, username)
            api_response = self.fetch(graphql_query)

            if api_response.get("data", {}).get("user") is None:
                return f"Can't fetch any contribution for {username}. Please check the username 😬"
            else:
                user_data = {
                    "today_contribution": 0,
                    "current_streak": 0,
                    "longest_streak": 0,
                    "total_contribution": 0,
                    "name": api_response["data"]["user"]["name"],
                    "github_link": f"https://github.com/{username}"
                }

                weeks = api_response["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]

                streak_count = 0
                longest_streak = 0
                total_contribution = 0

                for week in weeks:
                    for contribution_day in week["contributionDays"]:
                        contribution_day["date"] = datetime.fromisoformat(contribution_day["date"]).day
                        if contribution_day["date"] == now.day:
                            user_data["today_contribution"] = contribution_day["contributionCount"]

                        total_contribution += contribution_day["contributionCount"]

                        if contribution_day["contributionCount"] > 0:
                            streak_count += 1
                            longest_streak = max(longest_streak, streak_count)
                        else:
                            streak_count = 0

                user_data["current_streak"] = streak_count
                user_data["longest_streak"] = longest_streak
                user_data["total_contribution"] = total_contribution

                return user_data

        except Exception as error:
            print(f'Error for {username}: {error}')
            return str(error)

    def fetch_contributions_for_users(self):
        results = []
        for username in self.usernames:
            results.append(self.fetch_contributions_for_user(username))
        return results

# Usage example
usernames_list = ["aliseyedi01", "egbalwaldmann","masabbasi","zahra-hjri"]
fetcher = Fetcher(usernames_list)
results = fetcher.fetch_contributions_for_users()


# Usage example
if __name__ == '__main__':
    usernames_list = ["aliseyedi01", "egbalwaldmann", "masabbasi", "zahra-hjri"]
    fetcher = Fetcher(usernames_list)
    results = fetcher.fetch_contributions_for_users()
    print(results)