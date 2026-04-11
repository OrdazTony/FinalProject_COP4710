INSERT INTO UserTable (user_id, name, email)
VALUES (1, 'Alice Johnson', 'alice@example.com'),
    (2, 'Brian Lee', 'brian@example.com'),
    (3, 'Carla Mendes', 'carla@example.com'),
    (4, 'David Smith', 'david@example.com');
INSERT INTO Pet (pet_id, name, species, age, available)
VALUES (101, 'Buddy', 'Dog', 3, TRUE),
    (102, 'Mittens', 'Cat', 2, TRUE),
    (103, 'Rocky', 'Dog', 7, FALSE),
    (104, 'Coco', 'Bird', 0, TRUE),
    (105, 'Luna', 'Cat', 12, TRUE);
-- application_id is NOT inserted manually
-- PostgreSQL will create it automatically
INSERT INTO AdoptionApplication (user_id, pet_id, status, submitted_at, notes)
VALUES (
        1,
        101,
        'Pending',
        '2026-04-01 10:30:00',
        'Looking for a family dog'
    ),
    (
        2,
        102,
        'Approved',
        '2026-04-02 14:00:00',
        'Has experience with cats'
    ),
    (3, 103, 'Rejected', '2026-04-03 09:15:00', NULL),
    (
        1,
        105,
        'Withdrawn',
        '2026-04-04 16:45:00',
        'Moved to a smaller apartment'
    ),
    (4, 101, 'Pending', '2026-04-05 11:20:00', NULL);
