CREATE TABLE IF NOT EXISTS auth (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    password_hash TEXT,
    permissions_group TEXT
);

CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    university TEXT,
    major TEXT,
    language_pref TEXT,
    email_pref TEXT,
    sms_pref TEXT,
    targeted_adv_pref TEXT
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    owner_user_id TEXT,
    title TEXT,
    desc TEXT,
    employer TEXT,
    location TEXT,
    salary REAL
);


CREATE TABLE IF NOT EXISTS connections (
    sender_user_id TEXT PRIMARY KEY,
    recipient_user_id TEXT PRIMARY KEY,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (sender_user_id) REFERENCES users(user_id),
    FOREIGN KEY (recipient_user_id) REFERENCES users(user_id)
);

