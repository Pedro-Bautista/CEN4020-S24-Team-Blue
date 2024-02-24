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
    language_pref TEXT,
    email_pref TEXT,
    sms_pref TEXT,
    targeted_adv_pref TEXT
);

CREATE TABLE IF NOT EXISTS connections (
    connections_index_id TEXT PRIMARY KEY,
    connector_id TEXT,
    connectee_id TEXT,
    pending TEXT
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

CREATE TABLE IF NOT EXISTS friends (
    user1_id TEXT,
    user2_id TEXT,
    FOREIGN KEY (user1_id) REFERENCES users(user_id),
    FOREIGN KEY (user2_id) REFERENCES users(user_id),
    PRIMARY KEY (user1, user2)
);

CREATE TABLE IF NOT EXISTS friend_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_user_id TEXT,
    receiever_id TEXT,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (sender_user_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_user_id) REFERENCES users(user_id)
);

