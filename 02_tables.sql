-- Location Table
-- This table stores geographic data for countries and cities.
CREATE TABLE LOCATION (
    location_id SERIAL PRIMARY KEY,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL
);

-- Base User Table
-- This table maintains core identity and login credentials for every user.
CREATE TABLE "USER" (
    user_id SERIAL PRIMARY KEY,
    location_id INT REFERENCES LOCATION(location_id),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(225) NOT NULL,
    phone_number VARCHAR(20),
    role user_role NOT NULL,
    address_line VARCHAR(225),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patient Specialization
-- This table holds medical records for users registered as patients.
CREATE TABLE PATIENT (
    patient_id INT PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
    medical_history TEXT
);

-- Caregiver Specialization
-- This table tracks professional rates and verification status for caregivers.
CREATE TABLE CAREGIVER (
    caregiver_id INT PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
    hourly_rate DECIMAL(10,2),
    bank_account VARCHAR(25),
    is_verified BOOLEAN DEFAULT FALSE
);

-- Admin Specialization
-- This table defines the permission levels for system administrators.
CREATE TABLE ADMIN (
    admin_id INT PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
    access_level INT
);

-- Family Relationship
-- This table links family members to a specific patient.
CREATE TABLE FAMILY (
    family_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES PATIENT(patient_id),
    relationship VARCHAR(50)
);

-- Caregiver Documentation
-- This table manages files and validation status for caregiver credentials.
CREATE TABLE DOCUMENT (
    document_id SERIAL PRIMARY KEY,
    caregiver_id INT REFERENCES CAREGIVER(caregiver_id),
    file_url VARCHAR(500) NOT NULL,
    document_type doc_type NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATE,
    verification_status doc_status DEFAULT 'Pending',
    rejection_reason TEXT,
    verified_by INT REFERENCES ADMIN(admin_id)
);

-- Payments
-- This table records financial transactions and payment status for caregivers.
CREATE TABLE PAYMENT (
    payment_id SERIAL PRIMARY KEY,
    caregiver_id INT REFERENCES CAREGIVER(caregiver_id),
    amount DECIMAL(10,2) NOT NULL,
    transaction_id VARCHAR(255) UNIQUE,
    status payment_status DEFAULT 'Pending',
    payment_date DATE
);

-- Shift Report
-- This table documents the duration and details of completed work shifts.
CREATE TABLE SHIFT_REPORT (
    report_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES PATIENT(patient_id),
    caregiver_id INT REFERENCES CAREGIVER(caregiver_id),
    payment_id INT REFERENCES PAYMENT(payment_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    total_hours DECIMAL(5,2),
    report_description TEXT
);