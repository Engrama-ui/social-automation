# Social Media Automation System Documentation

## Overview
A comprehensive system for automating social media tasks including:
- Content scheduling
- Engagement tracking
- Hashtag optimization
- Performance analytics
- Multi-platform integration

## API Endpoints

### Content Scheduling
- `POST /api/content` - Schedule a new post
- `GET /api/content/{account_id}` - Get scheduled posts
- `DELETE /api/content/{post_id}` - Cancel a scheduled post

### Engagement Tracking
- `GET /api/engagement/post/{post_id}` - Get post engagement
- `GET /api/engagement/account/{account_id}/recent` - Get recent engagements
- `GET /api/engagement/account/{account_id}/summary` - Get engagement summary

### Hashtag Optimization
- `GET /api/hashtags/research/{hashtag}` - Research a hashtag
- `GET /api/hashtags/performance/{hashtag_id}` - Get hashtag performance
- `POST /api/hashtags/suggestions` - Get hashtag suggestions
- `GET /api/hashtags/trending` - Get trending hashtags

### Platform Integration
- `POST /api/platforms/connect` - Connect a social account
- `POST /api/platforms/{account_id}/post` - Post content
- `GET /api/platforms/{account_id}/insights` - Get account insights

## Setup Instructions

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Set up database:
```bash
python init_db.py
```

3. Run the server:
```bash
uvicorn main:app --reload
```

## Monitoring
The system includes a monitoring service that checks:
- Service availability
- CPU usage
- Memory usage
- Response times

Run the monitor with:
```bash
python monitoring/monitor.py
```