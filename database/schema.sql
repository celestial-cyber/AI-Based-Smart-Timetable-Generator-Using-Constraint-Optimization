CREATE TABLE departments (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE faculty (
    faculty_id INT PRIMARY KEY AUTO_INCREMENT,
    faculty_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    dept_id INT,
    designation VARCHAR(100),

    FOREIGN KEY (dept_id)
    REFERENCES departments(dept_id)
);

CREATE TABLE subjects (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    hours_per_week INT NOT NULL,
    is_lab BOOLEAN DEFAULT FALSE,
    semester INT NOT NULL,
    dept_id INT,

    FOREIGN KEY (dept_id)
    REFERENCES departments(dept_id)
);

CREATE TABLE rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_name VARCHAR(50) UNIQUE NOT NULL,
    room_type ENUM('classroom', 'lab') NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE classes (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_id INT,
    year INT NOT NULL,
    semester INT NOT NULL,
    section VARCHAR(10) NOT NULL,
    strength INT,

    FOREIGN KEY (dept_id)
    REFERENCES departments(dept_id)
);

CREATE TABLE faculty_subjects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    faculty_id INT,
    subject_id INT,

    FOREIGN KEY (faculty_id)
    REFERENCES faculty(faculty_id),

    FOREIGN KEY (subject_id)
    REFERENCES subjects(subject_id)
);

CREATE TABLE timetable (
    timetable_id INT PRIMARY KEY AUTO_INCREMENT,
    class_id INT,
    subject_id INT,
    faculty_id INT,
    room_id INT,
    day VARCHAR(20),
    period INT,

    FOREIGN KEY (class_id)
    REFERENCES classes(class_id),

    FOREIGN KEY (subject_id)
    REFERENCES subjects(subject_id),

    FOREIGN KEY (faculty_id)
    REFERENCES faculty(faculty_id),

    FOREIGN KEY (room_id)
    REFERENCES rooms(room_id)
);