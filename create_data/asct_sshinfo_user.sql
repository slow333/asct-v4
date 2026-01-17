-- Assuming the table is empty and the first ID will be 1.
INSERT INTO asct_sshinfo (id, login_id, ip,port, password, created_at, updated_at) VALUES(1,'root', '192.168.219.206', 22,'1', '2025-12-13 00:00:00', '2025-12-13 15:00:00');
INSERT INTO asct_sshinfo (id, login_id, ip,port, password, created_at, updated_at) VALUES(2,'root', '192.168.219.7', 22,'1', '2025-12-12 00:00:00', '2025-12-12 16:00:00');
INSERT INTO asct_sshinfo (id, login_id, ip,port, password, created_at, updated_at) VALUES(3,'root', '192.168.219.111', 22,'1', '2024-12-03 00:00:00', '2024-12-03 17:00:00');
INSERT INTO asct_sshinfo (id, login_id, ip,port, password, created_at, updated_at) VALUES(4,'root', '192.168.219.209', 22,'1', '2023-01-01 00:00:00', '2023-01-01 18:00:00');
INSERT INTO asct_sshinfo (id, login_id, ip,port, password, created_at, updated_at) VALUES(5,'root', '192.168.219.210', 22,'1', '2022-01-01 20:00:00', '2022-01-01 19:00:00');

-- Link SSHInfo records with User records.
-- This assumes you have users with IDs 1, 2, etc., in your auth_user table.

-- Link SSHInfo(id=1) to User(id=1)
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (1, 1);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (1, 2);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (1, 3);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (1, 4);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (1, 5);

-- Link SSHInfo(id=2) to User(id=1) and User(id=2)
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (2, 1);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (2, 2);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (2, 3);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (2, 4);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (3, 1);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (3, 2);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (3, 3);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (4, 1);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (4, 2);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (5, 1);
INSERT INTO asct_sshinfo_user (sshinfo_id, user_id) VALUES (5, 2);
