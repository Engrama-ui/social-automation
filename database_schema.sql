-- Social Media Automation System Database Schema

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE social_accounts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    platform VARCHAR(50) NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    last_sync TIMESTAMP,
    UNIQUE(user_id, platform)
);

CREATE TABLE scheduled_posts (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES social_accounts(id),
    content TEXT NOT NULL,
    media_urls TEXT[],
    scheduled_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE engagements (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES scheduled_posts(id),
    likes INT DEFAULT 0,
    comments INT DEFAULT 0,
    shares INT DEFAULT 0,
    sentiment_score FLOAT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hashtags (
    id SERIAL PRIMARY KEY,
    tag VARCHAR(255) UNIQUE NOT NULL,
    popularity_score FLOAT,
    last_analyzed TIMESTAMP
);

CREATE TABLE post_hashtags (
    post_id INT REFERENCES scheduled_posts(id),
    hashtag_id INT REFERENCES hashtags(id),
    PRIMARY KEY (post_id, hashtag_id)
);

CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES social_accounts(id),
    metric_date DATE NOT NULL,
    followers INT,
    impressions INT,
    reach INT,
    engagement_rate FLOAT,
    UNIQUE(account_id, metric_date)
);

CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    timezone VARCHAR(50) DEFAULT 'Europe/Rome',
    language VARCHAR(10) DEFAULT 'it',
    email_notifications BOOLEAN DEFAULT true,
    engagement_alerts BOOLEAN DEFAULT true,
    weekly_reports BOOLEAN DEFAULT false,
    optimization_tips BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);