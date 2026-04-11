-- queries.sql
-- Query 1: View all pets
SELECT pet_id,
    name,
    species,
    age,
    available
FROM Pet
ORDER BY pet_id;
-- Query 2: View available pets
SELECT pet_id,
    name,
    species,
    age,
    available
FROM Pet
WHERE available = TRUE
ORDER BY pet_id;
-- Query 3: Count applications per pet
SELECT p.pet_id,
    p.name AS pet_name,
    COUNT(a.application_id) AS application_count
FROM Pet p
    LEFT JOIN AdoptionApplication a ON p.pet_id = a.pet_id
GROUP BY p.pet_id,
    p.name
ORDER BY p.pet_id;
-- Query 4: View approved applications
SELECT application_id,
    user_id,
    pet_id,
    status,
    submitted_at,
    notes
FROM AdoptionApplication
WHERE status = 'Approved'
ORDER BY application_id;
-- Query 5: View all applications
SELECT application_id,
    user_id,
    pet_id,
    status,
    submitted_at,
    notes
FROM AdoptionApplication
ORDER BY application_id;
-- Query 6: View applications by pet
SELECT application_id,
    user_id,
    pet_id,
    status,
    submitted_at,
    notes
FROM AdoptionApplication
WHERE pet_id = 101
ORDER BY application_id;
-- Query 7: View applications by user
SELECT application_id,
    user_id,
    pet_id,
    status,
    submitted_at,
    notes
FROM AdoptionApplication
WHERE user_id = 1
ORDER BY application_id;
-- Query 8: Show each application with user and pet names
SELECT a.application_id,
    u.name AS user_name,
    p.name AS pet_name,
    a.status,
    a.submitted_at,
    a.notes
FROM AdoptionApplication a
    JOIN UserTable u ON a.user_id = u.user_id
    JOIN Pet p ON a.pet_id = p.pet_id
ORDER BY a.application_id;
