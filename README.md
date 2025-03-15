# Reddit Profile Scraper

A Python-based web scraper that allows you to extract comments and posts from Reddit user profiles using the old Reddit interface, without requiring API access.

## Overview

This tool provides a straightforward way to scrape public Reddit user profiles by navigating to their comment and submission pages and extracting the available information. It uses web scraping techniques with BeautifulSoup rather than the official Reddit API, making it useful for situations where API access is limited or unavailable.

## Features

- Scrape user comments across multiple pages
- Scrape user submissions/posts across multiple pages
- Extract full content from self-posts
- Command-line interface with customizable parameters
- Structured JSON output with timestamps
- Rate limiting to avoid being blocked
- Comprehensive error handling

## Installation

1. Clone this repository:
```bash
git clone https://github.com/MrDLTE/reddit-profile-scraper.git
cd reddit-profile-scraper
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python reddit_profile_scraper.py USERNAME
```

This will scrape 5 pages of comments and 5 pages of posts from the specified Reddit user and save the results to JSON files in the `output` directory.

### Advanced Options

```bash
# Scrape 10 pages of comments and posts
python reddit_profile_scraper.py USERNAME --comments 10 --posts 10

# Skip scraping comments, only get posts
python reddit_profile_scraper.py USERNAME --skip-comments

# Skip scraping posts, only get comments
python reddit_profile_scraper.py USERNAME --skip-posts

# Change output directory
python reddit_profile_scraper.py USERNAME --output my_data_folder
```

## Output

The script generates three JSON files in the output directory:

1. `{username}_comments_{timestamp}.json` - Contains all scraped comments
2. `{username}_posts_{timestamp}.json` - Contains all scraped posts
3. `{username}_profile_{timestamp}.json` - Contains the combined data

Each file includes detailed information such as content, timestamps, subreddits, scores, and permalinks.

## Example Output Structure

```json
{
  "username": "exampleuser",
  "scrape_time": "2025-03-15T12:00:00.123456",
  "comment_count": 50,
  "post_count": 10,
  "comments": [
    {
      "body": "This is a comment",
      "subreddit": "AskReddit",
      "score": "5",
      "permalink": "/r/AskReddit/comments/...",
      "timestamp": "2025-03-01T10:15:30+00:00"
    },
    ...
  ],
  "posts": [
    {
      "title": "This is a post title",
      "subreddit": "Python",
      "score": "42",
      "permalink": "/r/Python/comments/...",
      "timestamp": "2025-02-15T08:30:00+00:00",
      "num_comments": "7 comments",
      "body": "This is the content of the post"
    },
    ...
  ]
}
```

## Important Considerations

- **Legal and Ethical Usage**: This tool should only be used to scrape publicly available data. Always respect user privacy and Reddit's terms of service.
- **Rate Limiting**: The script includes deliberate delays between requests to respect Reddit's servers. Aggressive scraping may result in your IP being temporarily blocked.
- **Reliability**: As this uses web scraping rather than the official API, it may break if Reddit changes its page structure. Use the official Reddit API for more reliable access.

## Known Limitations

- Cannot access private profiles or age-restricted content
- May not capture all data if a user has a very large number of comments or posts
- Does not handle Reddit's infinite scroll interface, only traditional pagination
- External link posts don't include the actual content from the linked site

## Requirements

- Python 3.1+
- requests
- beautifulsoup4

## Disclaimer

This tool is provided for educational purposes only. The developer is not responsible for any misuse of this tool or violations of Reddit's terms of service.
