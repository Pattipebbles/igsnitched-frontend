"""
FastAPI backend for IGsnitched with a Test Brad Activity mode.

This module defines a simple FastAPI application that exposes endpoints for
tracking Instagram users and for generating simulated "Brad activity". The test
mode allows the frontend to demonstrate how reports look without calling the
Instagram API or scraping real data. It returns randomized follow/unfollow
changes along with a sarcastic Brad Mode commentary.

To run this server locally you can execute:

```
uvicorn backend.main:app --reload --port 8000
```

Your Vercel deployment should be configured to run this FastAPI app as the
backend service. When integrating with the frontend, make sure the base URL
matches where this API is hosted (for example, the same origin if deployed
together).
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import random

app = FastAPI(title="IGsnitched Backend")


class TrackRequest(BaseModel):
    """Represents a request to track a single Instagram username."""

    username: str


def generate_commentary(new_follows: List[str], unfollows: List[str]) -> str:
    """Create a sassy Brad Mode commentary based on new follows and unfollows.

    This function assembles a witty comment describing the detected activity.
    """
    remarks = []
    if new_follows:
        if len(new_follows) == 1:
            remarks.append(f"He's now following {new_follows[0]}. Someone's feeling adventurous.")
        else:
            nf = ", ".join(new_follows)
            remarks.append(f"He's now following {nf}. Guess the DMs were empty.")
    if unfollows:
        if len(unfollows) == 1:
            remarks.append(f"He unfollowed {unfollows[0]}. Pretending to be loyal now?")
        else:
            uf = ", ".join(unfollows)
            remarks.append(f"He unfollowed {uf}. Spring cleaning his feed, huh?")
    if not remarks:
        remarks.append("No new follows or unfollows. Brad must be asleep or plotting.")
    return " ".join(remarks)


def create_pdf(data: Dict[str, Any]) -> str:
    """Generate a simple PDF report summarizing the tracking data.

    This uses reportlab.platypus to build a one-page PDF with the key
    information from a tracking report. The resulting PDF is stored in a
    temporary file and the filename is returned.
    """
    # Prepare a temporary file to hold the PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
    styles = getSampleStyleSheet()
    story: List[Any] = []
    # Title
    story.append(Paragraph("IGsnitched Activity Report", styles["Title"]))
    story.append(Spacer(1, 12))
    # Add report fields
    story.append(Paragraph(f"Timestamp: {data.get('timestamp', '')}", styles["Normal"]))
    story.append(Paragraph(f"Username: {data.get('username', '')}", styles["Normal"]))
    story.append(Paragraph(f"Total Following: {data.get('total_following', '')}", styles["Normal"]))
    new_follows = data.get("new_follows", [])
    unfollows = data.get("unfollows", [])
    story.append(Paragraph(f"New Follows: {', '.join(new_follows) if new_follows else 'None'}", styles["Normal"]))
    story.append(Paragraph(f"Unfollows: {', '.join(unfollows) if unfollows else 'None'}", styles["Normal"]))
    commentary = data.get("commentary", "")
    story.append(Spacer(1, 12))
    story.append(Paragraph("Brad Mode Commentary:", styles["Heading2"]))
    story.append(Paragraph(commentary, styles["Italic"]))
    # Build the PDF
    doc.build(story)
    return temp_file.name


@app.post("/track")
async def track_user(req: TrackRequest):
    """Placeholder endpoint for real Instagram tracking.

    Currently this endpoint is a stub. In a full implementation, it would
    authenticate and fetch the target user's follower data, compare with
    snapshots stored in your database, and return the differences. For now it
    simply raises an error to indicate it's not implemented yet.
    """
    raise HTTPException(status_code=501, detail="Real tracking functionality is not yet implemented.")


@app.get("/track/test")
async def track_test_mode() -> dict:
    """Simulate follower changes for demonstration purposes.

    Generates a report with random new follows and unfollows pulled from sample
    lists. This allows the frontend to display realistic-looking reports and
    Brad Mode commentary without hitting Instagram or requiring a real user.
    """
    # Predefined lists of potential accounts to follow/unfollow in test mode
    sample_new_follows = [
        "kaykay_underscore",
        "fitnessbaddie24",
        "thirsttrapqueen",
        "gymbro69",
        "mysterymua",
        "chefchaos"
    ]
    sample_unfollows = [
        "his_ex_gf",
        "nice_girl_101",
        "churchgirl97",
        "studybuddy",
        "workwife",
        "hometownbestie"
    ]
    # Randomly select a subset of each list to simulate changes
    num_new = random.randint(0, max(1, len(sample_new_follows) // 2))
    num_unf = random.randint(0, max(1, len(sample_unfollows) // 2))
    new_follows = random.sample(sample_new_follows, k=num_new) if num_new else []
    unfollows = random.sample(sample_unfollows, k=num_unf) if num_unf else []
    # Simulate a follower count around 400 with small variance
    total_following = 400 + random.randint(-20, 20)
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": "test_user",
        "new_follows": new_follows,
        "unfollows": unfollows,
        "total_following": total_following,
        "commentary": generate_commentary(new_follows, unfollows),
    }
    return report


@app.get("/activity-history/{username}")
async def activity_history(username: str) -> Dict[str, Any]:
    """Return a simulated history of activity snapshots for a user.

    Since we don't yet persist data to a database, this endpoint generates
    a list of random snapshots similar to the test mode. Each snapshot
    includes a timestamp, lists of new follows and unfollows, total following,
    and a commentary string. In a future implementation, this would query
    the database for stored snapshots for the given user.

    Args:
        username: The Instagram handle to fetch history for.

    Returns:
        A dictionary containing the username and a list of history records.
    """
    history = []
    # We'll generate between 3 and 7 historical snapshots
    num_snapshots = random.randint(3, 7)
    for _ in range(num_snapshots):
        # Randomly determine new follows and unfollows using the same samples
        sample_new_follows = [
            "kaykay_underscore",
            "fitnessbaddie24",
            "thirsttrapqueen",
            "gymbro69",
            "mysterymua",
            "chefchaos",
        ]
        sample_unfollows = [
            "his_ex_gf",
            "nice_girl_101",
            "churchgirl97",
            "studybuddy",
            "workwife",
            "hometownbestie",
        ]
        num_new = random.randint(0, max(1, len(sample_new_follows) // 2))
        num_unf = random.randint(0, max(1, len(sample_unfollows) // 2))
        new_follows = random.sample(sample_new_follows, k=num_new) if num_new else []
        unfollows = random.sample(sample_unfollows, k=num_unf) if num_unf else []
        total_following = 400 + random.randint(-20, 20)
        history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "new_follows": new_follows,
            "unfollows": unfollows,
            "total_following": total_following,
            "commentary": generate_commentary(new_follows, unfollows),
        })
    return {"username": username, "history": history}


@app.get("/report/test/pdf")
async def report_test_pdf() -> FileResponse:
    """Generate and return a PDF report for a test tracking session.

    This endpoint calls the test tracking mode to generate sample data, then
    creates a PDF summarizing that data using reportlab. The PDF is returned
    as a downloadable file response.

    Returns:
        fastapi.responses.FileResponse: The generated PDF file.
    """
    data = await track_test_mode()
    pdf_path = create_pdf(data)
    # Provide a user-friendly filename in the response
    return FileResponse(path=pdf_path, media_type="application/pdf", filename="igsnitched_report.pdf")
