# 🎯 Reddit User Persona Generator

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production-brightgreen.svg)

*Transform Reddit profiles into comprehensive user personas with AI-powered analysis*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples) • [API Setup](#-api-setup)

</div>

---

## 🌟 Overview

Reddit User Persona Generator is a powerful Python application that analyzes Reddit user profiles and creates detailed user personas. It scrapes posts and comments, then uses advanced pattern analysis to generate comprehensive personality profiles with evidence-based citations.

## ✨ Features

### 🔍 **Smart Data Collection**
- Extracts posts and comments from any public Reddit user
- Collects user metadata (karma, account age, activity patterns)
- Handles rate limiting and API restrictions gracefully
- Supports both single users and batch processing

### 🧠 **Advanced Analysis**
- **Demographics**: Age, location, occupation, education level
- **Behavioral Patterns**: Online habits, interests, communication style
- **Personality Traits**: Values, motivations, social interactions
- **Goals & Frustrations**: Aspirations, pain points, challenges

### 📊 **Evidence-Based Insights**
- Every characteristic backed by specific Reddit posts/comments
- Direct citations with URLs for verification
- Confidence scoring for demographic predictions
- Structured output format for easy parsing

### ⚙️ **Flexible Configuration**
- Configurable limits for posts and comments
- Custom output directories
- Verbose logging for debugging
- Batch processing for multiple users

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Reddit API credentials
- Active internet connection

### Quick Setup

1. **Clone or Download the Project**
   ```bash
   git clone https://github.com/anixet-14/Reddit-User-Persona-Generator.git
   cd Reddit-User-Persona-Generator
   ```

2. **Install Dependencies**
   ```bash
   pip install praw openai anthropic google-genai
   ```

3. **Set up Environment Variables**
   Create a `.env` file in the project root:
   ```env
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=PersonaGenerator/1.0
   ```

## 📖 Usage

### Basic Commands

#### Single User Analysis
```bash
python main.py "https://www.reddit.com/user/username/"
```

#### Quick Analysis (Faster)
```bash
python main.py username --max-posts 20 --max-comments 50
```

#### Detailed Analysis
```bash
python main.py username --max-posts 200 --max-comments 500 --verbose
```

### Advanced Usage

#### Batch Processing
Create `usernames.txt`:
```
kojied
Hungry-Move-6603
another_username
```

Run batch analysis:
```bash
python main.py usernames.txt --batch --output-dir ./results
```

#### Custom Configuration
```bash
python main.py username \
  --max-posts 100 \
  --max-comments 200 \
  --output-dir ./personas \
  --verbose
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--batch` | Process multiple users from file | Single user |
| `--max-posts N` | Maximum posts to analyze | 100 |
| `--max-comments N` | Maximum comments to analyze | 200 |
| `--output-dir DIR` | Output directory for personas | `./personas` |
| `--verbose` | Enable detailed logging | Disabled |

## 💡 Examples

### Example Output Structure
```
========================================
USER PERSONA: kojied
========================================

Generated on: 2025-07-13 20:52:28
Account created: 2020-01-02
Link karma: 217
Comment karma: 1821
Posts analyzed: 8
Comments analyzed: 12

========================================
DEMOGRAPHICS
========================================
Age: Young Adult (20-25) (based on language patterns)
Location: NYC (inferred from activity patterns)
Occupation: Software Developer (based on content analysis)
Education: College-educated (inferred from communication style)
Archetype: Long-term Reddit user

========================================
BEHAVIORS & HABITS
========================================
• Engages across diverse communities and topics
  Citations:
    - Post: https://reddit.com/r/newyorkcity/...
      "I feel violated by intern season"
    - Post: https://reddit.com/r/AskReddit/...
      "H1B holders, what are your thoughts..."

• Shows strong interest in technology
  Citations:
    - Comment: https://reddit.com/r/programming/...
      "I've been using Python for 3 years..."
...
```

### Sample Use Cases

1. **UX Research**: Understanding user demographics for product design
2. **Market Research**: Analyzing target audience characteristics
3. **Content Strategy**: Tailoring content to user interests and behaviors
4. **Community Management**: Better understanding of community members

## 🔧 API Setup

### Reddit API Setup
1. Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose "script" as the application type
4. Fill in the form:
   - **Name**: Your app name
   - **Description**: Brief description
   - **Redirect URI**: `http://localhost:8080`
5. Note your **Client ID** (under the app name) and **Client Secret**

### Environment Variables
```bash
export REDDIT_CLIENT_ID="your_client_id_here"
export REDDIT_CLIENT_SECRET="your_client_secret_here"
export REDDIT_USER_AGENT="PersonaGenerator/1.0"
```

## ⚡ Performance

### Execution Times
- **Quick Analysis** (5-10 posts/comments): 30-60 seconds
- **Standard Analysis** (100 posts/200 comments): 3-8 minutes
- **Large Analysis** (500+ posts/comments): 10-20 minutes

### Optimization Tips
- Use smaller limits for faster testing
- Enable verbose logging to monitor progress
- Consider batch processing for multiple users
- Reddit API rate limiting is the main bottleneck

## 🛡️ Privacy & Ethics

- ✅ Only processes public Reddit data
- ✅ Respects Reddit's API terms of service
- ✅ Includes proper rate limiting
- ✅ No permanent data storage
- ✅ Generates analysis files only

## 📁 Project Structure

```
reddit-persona-generator/
├── main.py                 # Main application entry point
├── config.py              # Configuration and logging setup
├── reddit_scraper.py      # Reddit API integration
├── persona_generator.py   # Pattern-based persona analysis
├── utils.py               # Utility functions
├── README.md              # This file
├── requirements.txt       # Python dependencies
└── personas/             # Generated persona files
```

## 🔍 Technical Details

### Core Technologies
- **PRAW**: Python Reddit API Wrapper for data collection
- **Pattern Analysis**: Advanced text analysis for insights
- **Rate Limiting**: Respectful API usage with built-in delays
- **Error Handling**: Graceful handling of edge cases

### Analysis Methodology
1. **Text Extraction**: Collects all posts and comments
2. **Pattern Matching**: Identifies demographic indicators
3. **Behavioral Analysis**: Analyzes communication patterns
4. **Citation Mapping**: Links insights to source content
5. **Structured Output**: Formats results for readability

## 🚦 Troubleshooting

### Common Issues

#### "API key not valid" Error
```bash
# Check your environment variables
echo $REDDIT_CLIENT_ID
echo $REDDIT_CLIENT_SECRET
```

#### "User not found" Error
- Verify the username exists and is public
- Check if the user has been suspended or deleted

#### Slow Performance
- Reduce `--max-posts` and `--max-comments` values
- Use `--verbose` to monitor progress
- Reddit API rate limiting causes delays

### Getting Help
- Check the verbose logs for detailed error messages
- Ensure all environment variables are set correctly
- Verify Reddit API credentials are valid

## 📊 Limitations

- Only works with public Reddit profiles
- Subject to Reddit API rate limits
- Analysis quality depends on available user data
- Requires active internet connection
- Pattern-based analysis may have accuracy limitations

## 🎯 Future Enhancements

- [ ] Web interface for easier usage
- [ ] Export formats (JSON, CSV, PDF)
- [ ] Advanced visualization dashboards
- [ ] Integration with other social platforms
- [ ] Machine learning model improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Reddit API for providing access to public data
- PRAW library for excellent Reddit integration
- The open-source community for inspiration and tools

---

<div align="center">

**Made with ❤️ for better understanding of online communities**

[Report Bug](mailto:support@example.com) • [Request Feature](mailto:support@example.com) • [Documentation](README.md)

</div>
