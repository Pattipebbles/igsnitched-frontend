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
from pydantic import BaseModel
from datetime import datetime
from typing import List
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
