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
    tier TEXT,
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


CREATE TABLE IF NOT EXISTS applications (
    applied_job_id TEXT,
    applicant_user_id TEXT,
    status TEXT DEFAULT 'PENDING',
    graduation_date TEXT,
    start_working_date TEXT,
    application_paragraph TEXT,
    FOREIGN KEY (applied_job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (applicant_user_id) REFERENCES users(user_id),
    PRIMARY KEY (applied_job_id, applicant_user_id)
);


CREATE TABLE IF NOT EXISTS job_saves (
    saving_user_id TEXT,
    saved_job_id TEXT,
    FOREIGN KEY (saving_user_id) REFERENCES users(user_id),
    FOREIGN KEY (saved_job_id) REFERENCES jobs(job_id),
    PRIMARY KEY (saving_user_id, saved_job_id)
);

CREATE TABLE IF NOT EXISTS chats (
    chat_id TEXT,
    user1 TEXT,
    user2 TEXT, 
    FOREIGN KEY(user1) REFERENCES users(user_id),
    FOREIGN KEY(user2) REFERENCES users(user_id),
    PRIMARY KEY(chat_id, user1, user2)
);

CREATE TABLE IF NOT EXISTS messages (
    chat_id TEXT,
    message_id TEXT,
    content TEXT,
    status TEXT DEFAULT 'UNREAD',
    FOREIGN KEY (chat_id) REFERENCES chats(chat_id),
    PRIMARY KEY (chat_id, message_id)
);