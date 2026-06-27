import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.utils.config_loader import env

class EmailAlert:
    def __init__(self):
        self.user = env("EMAIL_USER")
        self.password = env("EMAIL_APP_PASSWORD")
        self.to = env("EMAIL_TO", self.user)
        self.enabled = bool(self.user and self.password and self.to)

    def render(self, jobs):
        rows = ""
        for j in jobs:
            rows += f"""
            <tr>
              <td><b>{j.title}</b><br><small>{j.employer}</small></td>
              <td>{j.location}</td>
              <td>{j.score}/100<br>{j.priority}</td>
              <td>{', '.join(j.matched_keywords[:8])}</td>
              <td><a href="{j.url}">Open</a></td>
            </tr>
            """
        return f"""
        <html><body>
        <h2>Hydrology Job Alerts</h2>
        <p>New jobs matching your hydrology profile:</p>
        <table border="1" cellpadding="6" cellspacing="0">
          <tr><th>Job</th><th>Location</th><th>Score</th><th>Why matched</th><th>Link</th></tr>
          {rows}
        </table>
        <p>Please review each job and edit AI drafts before submitting.</p>
        </body></html>
        """

    def send(self, jobs):
        if not self.enabled or not jobs:
            print("Email skipped: missing EMAIL_USER/EMAIL_APP_PASSWORD/EMAIL_TO or no jobs")
            return
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Hydrology Jobs: {len(jobs)} new matches"
        msg["From"] = self.user
        msg["To"] = self.to
        msg.attach(MIMEText(self.render(jobs), "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.user, self.password)
            server.sendmail(self.user, self.to, msg.as_string())
