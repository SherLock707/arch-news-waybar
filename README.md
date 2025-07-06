# Arch News Waybar Module

A custom Waybar module that displays recent Arch Linux news from the official RSS feed with customizable styling and colors.

![Screenshot](https://github.com/user-attachments/assets/2113298e-cce2-427a-a0bb-6af9d0d9e819)

## Features

- 📰 Fetches latest Arch Linux news from official RSS feed
- ⏰ Configurable time period (default: 7 days)
- 🎨 Customizable colors via command line arguments
- 🖱️ Click to open Arch Linux news page
- 📊 Shows count of recent news items
- 💡 Detailed tooltip with news headlines and dates
- 🔄 Auto-refresh every hour
- ⚡ Lightweight and efficient, written in Bash

## Dependencies

- `curl`
- `xmlstarlet`
- `jq`

## Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/SherLock707/arch-news-waybar.git
    cd arch-news-waybar
    ```

2.  Make sure you have the required dependencies installed. On Arch Linux, you can install them with:
    ```bash
    sudo pacman -S curl xmlstarlet jq
    ```

3.  Copy the module to your Waybar config directory:
    ```bash
    mkdir -p ~/.config/waybar/custom_modules
    cp arch_news ~/.config/waybar/custom_modules/
    chmod +x ~/.config/waybar/custom_modules/arch_news
    ```

## Configuration

### Waybar Config

Add this to your `~/.config/waybar/config.json`:

```json
{
  "custom/arch_news": {
    "format": "{}",
    "return-type": "json",
    "exec": "~/.config/waybar/custom_modules/arch_news 14",
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
./arch_news

# Show news from last 14 days
./arch_news 14

# Show news from last 30 days
./arch_news 30
```

### With Custom Colors

```bash
# Custom colors for active and inactive states
./arch_news 14 --active-color "#ff6b6b" --inactive-color "#4ecdc4"

# Using hex colors without quotes
./arch_news 7 --active-color ff6b6b --inactive-color 4ec4
```

### Command Line Arguments

- `days` (positional): Number of days to look back for news (default: 7)
- `--active-color`: Color when there are recent news items (default: #a6e3a1)
- `--inactive-color`: Color when there are no recent news items (default: system theme)
- `--help`: Show help message

## Example Outputs

### JSON Output Format

```json
{
  "text": " 3",
  "tooltip": "


",
  "class": "arch_news_active",
  "percentage": 30,
  "color": "#a6e3a1"
}
```

### Tooltip Format

The tooltip shows recent news with dates:
```



```

## Customization

### Changing the Icon

Edit the `arch_news` script and change the icon in the `tooltip` variable:

```bash
# Change the icon in the following line
tooltip=$(echo "$news_items_json" | jq -r --arg color "$active_color" '
    map("\uf061 <span color=\"\($color)\">\(.title) (\(.pubDate | parse_rfc822_date))</span>") | .[0:3] | join("\n\n")
')
```

### Adjusting Refresh Interval

Modify the `interval` in your Waybar config:

```json
"interval": 1800  // 30 minutes
"interval": 7200  // 2 hours
```

### Custom RSS Feed

You can modify the RSS URL in the script:

```bash
rss_url="https://archlinux.org/feeds/news/"
```

## Troubleshooting

### Common Issues

1. **Module not showing**: Check if the script path is correct and the script is executable.
2. **No news displayed**: Verify internet connection and RSS feed accessibility. Also check if `curl`, `xmlstarlet`, and `jq` are installed.
3. **Styling not applied**: Ensure CSS classes match between the script and your stylesheet.

### Debug Mode

Run the script directly to see output:

```bash
~/.config/waybar/custom_modules/arch_news 7
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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

SherLock707 (@SherLock707)

## Acknowledgments

- Arch Linux team for maintaining the news RSS feed
- Waybar developers for the excellent status bar
- Community contributors

---

⭐ If you find this module useful, please consider starring the repository!
