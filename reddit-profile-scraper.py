import requests
from bs4 import BeautifulSoup
import json
import time
import argparse
import os
from datetime import datetime

class RedditProfileScraper:
    def __init__(self, username):
        self.username = username
        self.base_url = f"https://old.reddit.com/user/{username}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.comments = []
        self.posts = []
        
    def scrape_comments(self, pages=5):
        """Scrape user comments from multiple pages"""
        print(f"Scraping comments for user: {self.username}")
        url = f"{self.base_url}/comments"
        after = None
        
        for page in range(pages):
            print(f"Scraping comments page {page+1}/{pages}")
            params = {"after": after} if after else {}
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find all comment entries
                comment_divs = soup.find_all("div", class_="thing", attrs={"data-type": "comment"})
                
                if not comment_divs:
                    print("No more comments found or page structure has changed")
                    break
                
                for comment in comment_divs:
                    try:
                        # Extract comment data
                        comment_data = {
                            "body": comment.find("div", class_="md").get_text().strip(),
                            "subreddit": comment.find("a", class_="subreddit").get_text().strip(),
                            "score": comment.find("span", class_="score").get_text().strip() if comment.find("span", class_="score") else "hidden",
                            "permalink": comment.find("a", class_="bylink").get("href") if comment.find("a", class_="bylink") else "",
                            "timestamp": comment.find("time")["datetime"] if comment.find("time") else "",
                            "context": comment.find("a", class_="bylink").get("href") if comment.find("a", class_="bylink") else ""
                        }
                        self.comments.append(comment_data)
                    except Exception as e:
                        print(f"Error parsing a comment: {e}")
                
                # Find "next page" link
                next_button = soup.find("span", class_="next-button")
                if next_button and next_button.find("a"):
                    after = next_button.find("a").get("href").split("after=")[1].split("&")[0]
                else:
                    print("No more pages available")
                    break
                
                # Respect Reddit's rate limits
                time.sleep(2)
                
            except Exception as e:
                print(f"Error scraping comments page {page+1}: {e}")
                break
        
        print(f"Successfully scraped {len(self.comments)} comments")
        
    def scrape_posts(self, pages=5):
        """Scrape user submissions from multiple pages"""
        print(f"Scraping posts for user: {self.username}")
        url = f"{self.base_url}/submitted"
        after = None
        
        for page in range(pages):
            print(f"Scraping posts page {page+1}/{pages}")
            params = {"after": after} if after else {}
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find all submission entries
                post_divs = soup.find_all("div", class_="thing", attrs={"data-type": "link"})
                
                if not post_divs:
                    print("No more posts found or page structure has changed")
                    break
                
                for post in post_divs:
                    try:
                        # Extract post data
                        post_data = {
                            "title": post.find("a", class_="title").get_text().strip(),
                            "subreddit": post.find("a", class_="subreddit").get_text().strip(),
                            "score": post.find("div", class_="score").get_text().strip() if post.find("div", class_="score") else "hidden",
                            "permalink": post.find("a", class_="comments").get("href") if post.find("a", class_="comments") else "",
                            "timestamp": post.find("time")["datetime"] if post.find("time") else "",
                            "num_comments": post.find("a", class_="comments").get_text().strip() if post.find("a", class_="comments") else "0"
                        }
                        
                        # Try to get post content if it's a self post
                        if "self." in post.get("data-domain", ""):
                            post_url = post.find("a", class_="title").get("href")
                            if post_url.startswith("/r/"):
                                try:
                                    post_response = requests.get(f"https://old.reddit.com{post_url}", headers=self.headers)
                                    post_soup = BeautifulSoup(post_response.text, "html.parser")
                                    post_body = post_soup.find("div", class_="usertext-body")
                                    if post_body:
                                        post_data["body"] = post_body.find("div", class_="md").get_text().strip()
                                    else:
                                        post_data["body"] = "[No content found]"
                                    time.sleep(1)  # Respect rate limits
                                except Exception as e:
                                    post_data["body"] = f"[Error fetching content: {e}]"
                            else:
                                post_data["body"] = "[External link]"
                        else:
                            post_data["body"] = "[External link]"
                            post_data["external_url"] = post.find("a", class_="title").get("href")
                        
                        self.posts.append(post_data)
                    except Exception as e:
                        print(f"Error parsing a post: {e}")
                
                # Find "next page" link
                next_button = soup.find("span", class_="next-button")
                if next_button and next_button.find("a"):
                    after = next_button.find("a").get("href").split("after=")[1].split("&")[0]
                else:
                    print("No more pages available")
                    break
                
                # Respect Reddit's rate limits
                time.sleep(2)
                
            except Exception as e:
                print(f"Error scraping posts page {page+1}: {e}")
                break
        
        print(f"Successfully scraped {len(self.posts)} posts")
    
    def save_to_json(self, output_dir="output"):
        """Save scraped data to JSON files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save comments
        comments_file = os.path.join(output_dir, f"{self.username}_comments_{timestamp}.json")
        with open(comments_file, "w", encoding="utf-8") as f:
            json.dump(self.comments, f, indent=4, ensure_ascii=False)
        print(f"Comments saved to {comments_file}")
        
        # Save posts
        posts_file = os.path.join(output_dir, f"{self.username}_posts_{timestamp}.json")
        with open(posts_file, "w", encoding="utf-8") as f:
            json.dump(self.posts, f, indent=4, ensure_ascii=False)
        print(f"Posts saved to {posts_file}")
        
        # Save combined data
        combined_file = os.path.join(output_dir, f"{self.username}_profile_{timestamp}.json")
        with open(combined_file, "w", encoding="utf-8") as f:
            json.dump({
                "username": self.username,
                "scrape_time": datetime.now().isoformat(),
                "comment_count": len(self.comments),
                "post_count": len(self.posts),
                "comments": self.comments,
                "posts": self.posts
            }, f, indent=4, ensure_ascii=False)
        print(f"Combined data saved to {combined_file}")
        
        return combined_file

def main():
    parser = argparse.ArgumentParser(description="Scrape a Reddit user's profile")
    parser.add_argument("username", help="Reddit username to scrape")
    parser.add_argument("--comments", type=int, default=5, help="Number of comment pages to scrape (default: 5)")
    parser.add_argument("--posts", type=int, default=5, help="Number of post pages to scrape (default: 5)")
    parser.add_argument("--output", default="output", help="Output directory for JSON files (default: 'output')")
    parser.add_argument("--skip-comments", action="store_true", help="Skip scraping comments")
    parser.add_argument("--skip-posts", action="store_true", help="Skip scraping posts")
    
    args = parser.parse_args()
    
    scraper = RedditProfileScraper(args.username)
    
    if not args.skip_comments:
        scraper.scrape_comments(pages=args.comments)
    
    if not args.skip_posts:
        scraper.scrape_posts(pages=args.posts)
    
    output_file = scraper.save_to_json(output_dir=args.output)
    print(f"Scraping completed. Data saved to {output_file}")

if __name__ == "__main__":
    main()
