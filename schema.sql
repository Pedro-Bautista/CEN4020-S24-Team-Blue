CREATE TABLE IF NOT EXISTS auth (
    user_id TEXT,
    username TEXT,
    password_hash TEXT,
    permissions_group TEXT,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS users (
    user_id TEXT,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    university TEXT,
    major TEXT,
    bio TEXT,
    experience TEXT CHECK ( length(experience)<=100),
    education TEXT CHECK ( length(education)<=512),
    language_pref TEXT,
    email_pref TEXT,
    sms_pref TEXT,
    targeted_adv_pref TEXT,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT,
    owner_user_id TEXT,
    title TEXT,
    desc TEXT,
    employer TEXT,
    location TEXT,
    salary REAL,
    PRIMARY KEY (job_id)
);


CREATE TABLE IF NOT EXISTS connections (
    sender_user_id TEXT,
    recipient_user_id TEXT,
    status TEXT DEFAULT 'PENDING',
    FOREIGN KEY (sender_user_id) REFERENCES users(user_id),
    FOREIGN KEY (recipient_user_id) REFERENCES users(user_id),
    PRIMARY KEY (sender_user_id, recipient_user_id)
);

