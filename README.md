# Arch News Waybar Module

A custom Waybar module that displays recent Arch Linux news from the official RSS feed with customizable styling and colors.

![Screenshot](screenshots/arch-news-waybar.png)

## Features

- 📰 Fetches latest Arch Linux news from official RSS feed
- ⏰ Configurable time period (default: 7 days)
- 🎨 Customizable colors via command line arguments
- 🖱️ Click to open Arch Linux news page
- 📊 Shows count of recent news items
- 💡 Detailed tooltip with news headlines and dates
- 🔄 Auto-refresh every hour
- ⚡ Lightweight and efficient

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/arch-news-waybar.git
cd arch-news-waybar
```

2. Create a Python virtual environment (recommended):
```bash
python -m venv ~/.venv
source ~/.venv/bin/activate
pip install feedparser
```

3. Copy the module to your Waybar config directory:
```bash
mkdir -p ~/.config/waybar/custom_modules
cp arch_news.py ~/.config/waybar/custom_modules/
chmod +x ~/.config/waybar/custom_modules/arch_news.py
```

## Configuration

### Waybar Config

Add this to your `~/.config/waybar/config.json`:

```json
{
  "custom/arch_news": {
    "format": "{}",
    "return-type": "json",
    "exec": "~/.venv/bin/python ~/.config/waybar/custom_modules/arch_news.py 14",
    "tooltip": true,
    "interval": 3600,
    "on-click": "xdg-open https://archlinux.org/news/"
  }
}
```

Add `"custom/arch_news"` to your modules list:

```json
{
  "modules-left": [
    "custom/arch_news"
  ]
}
```

### Waybar Styling

Add this to your `~/.config/waybar/style.css`:

```css
#custom-arch_news {
    color: @main-fg;
    background: alpha(@main-bg, 0.7);
    opacity: 1;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 6px;
    padding-right: 6px;
    border: 0.5px solid @main-fg;
    border-bottom: 3px;
    border-style: solid;
    border-color: @main-fg;
    border-radius: 4px;
}

#custom-arch_news.arch_news_active {
    color: #ff6b6b;
    border-color: #ff6b6b;
}

#custom-arch_news.arch_news_inactive {
    color: #4ecdc4;
    border-color: #4ecdc4;
}

#custom-arch_news.arch-news-error {
    color: #ff5555;
    border-color: #ff5555;
}
```

## Usage

### Basic Usage

```bash
# Show news from last 7 days (default)
python arch_news.py

# Show news from last 14 days
python arch_news.py 14

# Show news from last 30 days
python arch_news.py 30
```

### With Custom Colors

```bash
# Custom colors for active and inactive states
python arch_news.py 14 --active-color "#ff6b6b" --inactive-color "#4ecdc4"

# Using hex colors without quotes
python arch_news.py 7 --active-color ff6b6b --inactive-color 4ecdc4

# Using named colors
python arch_news.py 14 --active-color red --inactive-color green
```

### Command Line Arguments

- `days` (positional): Number of days to look back for news (default: 7)
- `--active-color`: Color when there are recent news items (default: system theme)
- `--inactive-color`: Color when there are no recent news items (default: system theme)
- `--help`: Show help message

## Example Outputs

### JSON Output Format

```json
{
  "text": " 3",
  "tooltip": " Critical update for systemd\n Package signing key rotation\n New kernel release 6.7.1",
  "class": "arch_news_active",
  "percentage": 30
}
```

### Tooltip Format

The tooltip shows recent news with dates:
```
 Critical update for systemd (2024-01-15 14:30)

 Package signing key rotation (2024-01-14 09:15)

 New kernel release 6.7.1 (2024-01-13 16:45)
```

## Customization

### Changing the Icon

Edit the `get_waybar_output()` method in `arch_news.py`:

```python
text = f"📰 {count}"  # Use newspaper emoji
text = f"🔔 {count}"  # Use bell emoji
text = f"📢 {count}"  # Use megaphone emoji
```

### Adjusting Refresh Interval

Modify the `interval` in your Waybar config:

```json
"interval": 1800  // 30 minutes
"interval": 7200  // 2 hours
```

### Custom RSS Feed

You can modify the RSS URL in the script:

```python
self.rss_url = "https://archlinux.org/feeds/news/"
```

## Troubleshooting

### Common Issues

1. **Module not showing**: Check if the Python path is correct and the virtual environment is accessible
2. **No news displayed**: Verify internet connection and RSS feed accessibility
3. **Styling not applied**: Ensure CSS classes match between the script and your stylesheet

### Debug Mode

Run the script directly to see output:

```bash
python ~/.config/waybar/custom_modules/arch_news.py 7
```

### Logs

Check Waybar logs for errors:

```bash
waybar -l debug
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test them
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## Screenshots

### Light Theme
![Light Theme](screenshots/light-theme.png)

### Dark Theme
![Dark Theme](screenshots/dark-theme.png)

### Active State (with news)
![Active State](screenshots/active-state.png)

### Inactive State (no recent news)
![Inactive State](screenshots/inactive-state.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Dependencies

- Python 3.6+
- feedparser
- Waybar

## Author

Your Name (@yourusername)

## Acknowledgments

- Arch Linux team for maintaining the news RSS feed
- Waybar developers for the excellent status bar
- Community contributors

---

⭐ If you find this module useful, please consider starring the repository!