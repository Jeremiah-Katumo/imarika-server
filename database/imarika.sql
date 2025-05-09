CREATE TABLE orgs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE,
    org_uuid VARCHAR(255) UNIQUE,
    about TEXT,
    location TEXT,
    contacts LONGTEXT,
    welcome_message TEXT,
    background TEXT,
    mission TEXT,
    vision TEXT,
    core_values LONGTEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date DATE,
    created_by INT,
    updated_by INT,
    org_status VARCHAR(10)
);

CREATE TABLE branches (
    branch_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id INT,
    branch_name VARCHAR(60),
    branch_street VARCHAR(100),
    branch_address TEXT,
    branch_email VARCHAR(100),
    branch_phone VARCHAR(100),
    branch_directions VARCHAR(100),
    branchCreated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    branchUpdated_date DATE,
    branchCreated_by INT,
    branchUpdated_by INT,
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id INT,
    department_title VARCHAR(100),
    department_image VARCHAR(100),
    departmentCreated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    departmentUpdated_date DATE,
    departmentCreated_by INT,
    departmentUpdated_by INT,
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE downloads (
    downloadFile_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id INT,
    downloadFile_title VARCHAR(255),
    downloadFile_name VARCHAR(255) UNIQUE,
    downloadFile_category VARCHAR(60),
    downloadFile_data LONGBLOB,
    downloadFileCreated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    downloadFileUpdated_date DATE,
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id INT,
    event_name VARCHAR(100),
    event_date DATETIME,
    event_description VARCHAR(100),
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE faqs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    question VARCHAR(100),
    answer VARCHAR(200),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date DATE,
    created_by INT,
    updated_by INT,
    org_id INT,
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE files (
    file_id INT PRIMARY KEY AUTO_INCREMENT,
    filePath VARCHAR(255),
    fileName VARCHAR(255),
    fileData LONGBLOB,
    fileCreated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fileUpdated_date DATE,
    fileCreated_by INT,
    fileUpdated_by INT,
    vacancyApplication_id INT,
    tender_id INT,
    FOREIGN KEY (vacancyApplication_id) REFERENCES vacancy_applications(vacancyApplication_id),
    FOREIGN KEY (tender_id) REFERENCES tenders(tender_id)
);

CREATE TABLE images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    filename VARCHAR(100),
    org_id INT,
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE latestnews (
    news_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id INT,
    news_heading VARCHAR(255),
    news_info VARCHAR(255),
    newsCreated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    newsUpdated_date DATE,
    newsCreated_by INT,
    newsUpdated_by INT,
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    org_id INT,
    email VARCHAR(100),
    subject VARCHAR(200),
    message TEXT,
    status VARCHAR(10),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date DATE,
    created_by INT,
    updated_by INT,
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id INT,
    product_title VARCHAR(255),
    product_description VARCHAR(255),
    product_image VARCHAR(255),
    product_category VARCHAR(100),
    productSub_category VARCHAR(100),
    productCreated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    productUpdated_date DATE,
    productCreated_by INT,
    productUpdated_by INT,
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE team_members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    org_id INT,
    profile_picture VARCHAR(100),
    position VARCHAR(100),
    social_media_links LONGTEXT,
    phone VARCHAR(100),
    email VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date DATE,
    created_by INT,
    updated_by INT,
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE tenders (
    tender_id INT PRIMARY KEY AUTO_INCREMENT,
    tender_title VARCHAR(100),
    tenderCreated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tenderClosing_date DATE,
    tenderUpdated_date DATE,
    tenderCreated_by INT,
    tenderUpdated_by INT
);

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(30),
    email VARCHAR(50),
    full_name VARCHAR(100),
    hashed_password VARCHAR(100),
    disabled BOOLEAN,
    is_superuser BOOLEAN
);

CREATE TABLE vacancies (
    vacancy_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id INT,
    title VARCHAR(255),
    category VARCHAR(20),
    description TEXT,
    requirements TEXT,
    duration DATE,
    how_to_apply TEXT,
    reference_number VARCHAR(255),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date DATE,
    created_by INT,
    updated_by INT,
    FOREIGN KEY (org_id) REFERENCES orgs(id)
);

CREATE TABLE vacancy_applications (
    vacancyApplication_id INT PRIMARY KEY AUTO_INCREMENT,
    vacancyApplication_category VARCHAR(20),
    vacancyApplicationCreated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vacancyApplicationUpdated_date DATE,
    vacancyApplicationCreated_by INT,
    vacancyApplicationUpdated_by INT,
    vacancy_id INT,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies(vacancy_id)
);
