-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports WHERE year = 2020 AND month = 7 AND day = 28;
-- Theft time: 10:15am
-- Theft location: Chamberlin Street courthouse

SELECT transcript FROM interviews WHERE month = 7 AND day = 28 AND transcript LIKE '%Courthouse%';
-- Interview: Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
-- I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
-- As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)
AND people.id IN (SELECT person_id FROM bank_accounts JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number WHERE atm_transactions.year = 2020 AND atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.atm_location = "Fifer Street" AND transaction_type = "withdraw")
AND people.phone_number IN (SELECT caller FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60)
AND people.passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute ASC LIMIT 1));

-- Theif name: Ernest

SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute);
-- City: London

SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60 AND caller = (SELECT phone_number FROM people WHERE name = 'Ernest'));
-- Accomplice: Berthold

