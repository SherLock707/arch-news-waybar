#!/usr/bin/env python3

import json
import sys
import argparse
from datetime import datetime, timedelta
import feedparser

class ArchNewsModule:
    def __init__(self, days=7, active_color=None, inactive_color=None):
        self.days = days
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.rss_url = "https://archlinux.org/feeds/news/"
        self.news_data = {"count": 0, "headlines": []}

    def fetch_news(self):
        try:
            headers = {'User-Agent': 'Waybar-ArchNews/1.0'}
            feed = feedparser.parse(self.rss_url)

            if feed.bozo:
                return {"count": 0, "headlines": ["Error: Failed to parse RSS feed"]}

            cutoff_date = datetime.now() - timedelta(days=self.days)
            recent_news = []

            for entry in feed.entries:
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])
                else:
                    continue

                if pub_date >= cutoff_date:
                    recent_news.append({
                        'title': entry.title,
                        'date': pub_date.strftime('%Y-%m-%d %H:%M'),
                        'link': getattr(entry, 'link', '')
                    })

            recent_news.sort(key=lambda x: x['date'], reverse=True)

            return {
                "count": len(recent_news),
                "headlines": recent_news
            }

        except Exception as e:
            return {"count": 0, "headlines": [f"Error: {str(e)}"]}

    def normalize_color(self, color):
        """Normalize color input to a hex color format"""
        if not color:
            return None
        
        # Remove # if present
        color = color.lstrip('#')
        
        # Handle named colors
        named_colors = {
            'red': 'ff0000',
            'green': '00ff00',
            'blue': '0000ff',
            'yellow': 'ffff00',
            'orange': 'ffa500',
            'purple': '800080',
            'pink': 'ffc0cb',
            'cyan': '00ffff',
            'white': 'ffffff',
            'black': '000000',
            'gray': '808080',
            'grey': '808080'
        }
        
        if color.lower() in named_colors:
            color = named_colors[color.lower()]
        
        # Validate hex color (3 or 6 characters)
        if len(color) == 3:
            color = ''.join([c*2 for c in color])  # Convert abc to aabbcc
        
        if len(color) == 6 and all(c in '0123456789abcdefABCDEF' for c in color):
            return f"#{color}"
        
        return None

    def get_waybar_output(self):
        self.news_data = self.fetch_news()

        if self.news_data["headlines"]:
            if isinstance(self.news_data["headlines"][0], dict):
                tooltip = "\n\n".join(
                    f" {item['title']} ({item['date']})"
                    for item in self.news_data["headlines"]
                )
            else:
                tooltip = "\n".join(self.news_data["headlines"])
        else:
            tooltip = f"No Arch Linux news in the last {self.days} days"

        count = self.news_data["count"]
        text = f" {count}"
        css_class = "arch_news_active" if count > 0 else "arch_news_inactive"

        output = {
            "text": text,
            "tooltip": tooltip,
            "class": css_class,
            "percentage": min(count * 10, 100)
        }

        # Add custom colors if provided
        if count > 0 and self.active_color:
            normalized_color = self.normalize_color(self.active_color)
            if normalized_color:
                output["color"] = normalized_color
        elif count == 0 and self.inactive_color:
            normalized_color = self.normalize_color(self.inactive_color)
            if normalized_color:
                output["color"] = normalized_color

        return output

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Waybar module for Arch Linux news',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s                              # Show news from last 7 days
  %(prog)s 14                           # Show news from last 14 days
  %(prog)s 7 --active-color red         # Use red color for active state
  %(prog)s 14 --active-color ff6b6b --inactive-color 4ecdc4
        '''
    )
    
    parser.add_argument(
        'days',
        type=int,
        nargs='?',
        default=7,
        help='Number of days to look back for news (default: 7)'
    )
    
    parser.add_argument(
        '--active-color',
        type=str,
        help='Color to use when there are recent news items (hex color, named color, or color code)'
    )
    
    parser.add_argument(
        '--inactive-color',
        type=str,
        help='Color to use when there are no recent news items (hex color, named color, or color code)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Arch News Waybar Module 1.0'
    )
    
    return parser.parse_args()

def main():
    try:
        args = parse_arguments()
        
        # Validate days parameter
        if args.days <= 0:
            print(json.dumps({
                "text": " ✗",
                "tooltip": "Error: Days must be a positive number",
                "class": "arch-news-error"
            }))
            sys.exit(1)
        
        module = ArchNewsModule(
            days=args.days,
            active_color=args.active_color,
            inactive_color=args.inactive_color
        )
        
        output = module.get_waybar_output()
        print(json.dumps(output))
        sys.stdout.flush()
        
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        error_output = {
            "text": " ✗",
            "tooltip": f"Error: {str(e)}",
            "class": "arch-news-error"
        }
        print(json.dumps(error_output))
        sys.exit(1)

if __name__ == "__main__":
    main()