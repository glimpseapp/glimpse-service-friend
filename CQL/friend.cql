CREATE KEYSPACE Friend WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };

CREATE TABLE friend.friend_relation(
  user_id TEXT,
  friend_id TEXT,
  friend_since timestamp,

  PRIMARY KEY (user_id, friend_since)
) WITH CLUSTERING ORDER BY (friend_since DESC);

CREATE TABLE friend.request_by_sender_id (
  sender_id TEXT,
  request_id TEXT,
  receiver_id TEXT,

  PRIMARY KEY ((sender_id), request_id)
) WITH CLUSTERING ORDER BY (request_id DESC);

CREATE TABLE friend.request_by_receiver_id (
  receiver_id TEXT,
  request_id TEXT,
  sender_id TEXT,

  PRIMARY KEY ((receiver_id), request_id)
) WITH CLUSTERING ORDER BY (request_id DESC);

