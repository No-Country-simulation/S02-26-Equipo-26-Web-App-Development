CREATE TYPE user_role AS ENUM ('Admin', 'Caregiver', 'Patient');
CREATE TYPE doc_type AS ENUM ('ID_card', 'Criminal_record', 'Certification', 'Insurance');
CREATE TYPE doc_status AS ENUM ('Pending', 'Approved', 'Rejected');
CREATE TYPE payment_status AS ENUM ('Pending', 'Success', 'Failed');