import subprocess
import json

def get_app_reviews(app_id,reviews_count):
    result = subprocess.run(
        ['node', 'getReviews.js', app_id, str(reviews_count)],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)[:reviews_count]
