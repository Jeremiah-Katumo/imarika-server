
CREATE TABLE branches (
  branch_id int(11) NOT NULL,
  branch_name varchar(60) NOT NULL,
  branch_street varchar(100) NOT NULL,
  branch_address tinytext NOT NULL,
  branch_email varchar(100) NOT NULL,
  branch_phone varchar(100) DEFAULT NULL,
  branch_directions varchar(100) DEFAULT NULL,
  branchCreated_date timestamp NOT NULL DEFAULT current_timestamp(),
  branchUpdated_date date DEFAULT NULL,
  branchCreated_by int(11) DEFAULT NULL,
  branchUpdated_by int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE departments (
  department_id int(11) NOT NULL,
  department_title varchar(100) NOT NULL,
  department_image varchar(100) DEFAULT NULL,
  departmentCreated_date timestamp NOT NULL DEFAULT current_timestamp(),
  departmentUpdated_date date DEFAULT NULL,
  departmentCreated_by int(11) DEFAULT NULL,
  departmentUpdated_by int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE downloads (
  downloadFile_id int(11) NOT NULL,
  downloadFile_title varchar(255) NOT NULL,
  downloadFile_name varchar(255) DEFAULT NULL,
  downloadFile_category varchar(60) NOT NULL,
  downloadFile_data longblob DEFAULT NULL,
  downloadFileCreated_date timestamp NOT NULL DEFAULT current_timestamp(),
  downloadFileUpdated_date date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE events (
  event_id int(11) NOT NULL,
  event_name varchar(100) DEFAULT NULL,
  event_date datetime DEFAULT NULL,
  event_description varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE faqs (
  id int(11) NOT NULL,
  question varchar(100) NOT NULL,
  answer varchar(200) NOT NULL,
  created_date timestamp NOT NULL DEFAULT current_timestamp(),
  updated_date date DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  org_id int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE files (
  file_id int(11) NOT NULL,
  filePath varchar(255) DEFAULT NULL,
  fileName varchar(255) DEFAULT NULL,
  fileData longblob NOT NULL,
  fileCreated_date timestamp NOT NULL DEFAULT current_timestamp(),
  fileUpdated_date date DEFAULT NULL,
  fileCreated_by int(11) DEFAULT NULL,
  fileUpdated_by int(11) DEFAULT NULL,
  vacancyApplication_id int(11) DEFAULT NULL,
  tender_id int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE images (
  id int(11) NOT NULL,
  title varchar(100) DEFAULT NULL,
  filename varchar(100) DEFAULT NULL,
  org_id int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE latestnews (
  news_id int(11) NOT NULL,
  news_heading varchar(255) NOT NULL,
  news_info varchar(255) NOT NULL,
  newsCreated_date timestamp NOT NULL DEFAULT current_timestamp(),
  newsUpdated_date date DEFAULT NULL,
  newsCreated_by int(11) DEFAULT NULL,
  newsUpdated_by int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE messages (
  id int(11) NOT NULL,
  name varchar(100) DEFAULT NULL,
  org_id int(11) DEFAULT NULL,
  email varchar(100) DEFAULT NULL,
  subject varchar(200) DEFAULT NULL,
  message text DEFAULT NULL,
  status varchar(10) DEFAULT NULL,
  created_date timestamp NOT NULL DEFAULT current_timestamp(),
  updated_date date DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  updated_by int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE orgs (
  id int(11) NOT NULL,
  name varchar(100) DEFAULT NULL,
  org_uuid varchar(255) NOT NULL,
  about text DEFAULT NULL,
  location text DEFAULT NULL,
  contacts longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(contacts)),
  welcome_message text DEFAULT NULL,
  background text DEFAULT NULL,
  mission text DEFAULT NULL,
  vision text DEFAULT NULL,
  core_values longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(core_values)),
  created_date timestamp NOT NULL DEFAULT current_timestamp(),
  updated_date date DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  org_status varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE products (
  product_id int(11) NOT NULL,
  product_title varchar(255) NOT NULL,
  product_description varchar(255) NOT NULL,
  product_image varchar(255) DEFAULT NULL,
  product_category varchar(100) NOT NULL,
  productSub_category varchar(100) NOT NULL,
  productCreated_date timestamp NOT NULL DEFAULT current_timestamp(),
  productUpdated_date date DEFAULT NULL,
  productCreated_by int(11) DEFAULT NULL,
  productUpdated_by int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE team_members (
  id int(11) NOT NULL,
  name varchar(100) DEFAULT NULL,
  org_id int(11) DEFAULT NULL,
  profile_picture varchar(100) DEFAULT NULL,
  position varchar(100) DEFAULT NULL,
  social_media_links longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(social_media_links)),
  phone varchar(100) DEFAULT NULL,
  email varchar(100) DEFAULT NULL,
  created_date timestamp NOT NULL DEFAULT current_timestamp(),
  updated_date date DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  updated_by int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE tenders (
  tender_id int(11) NOT NULL,
  tender_title varchar(100) NOT NULL,
  tenderCreated_date timestamp NOT NULL DEFAULT current_timestamp(),
  tenderClosing_date date NOT NULL,
  tenderUpdated_date date DEFAULT NULL,
  tenderCreated_by int(11) DEFAULT NULL,
  tenderUpdated_by int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE users (
  id int(11) NOT NULL,
  username varchar(30) DEFAULT NULL,
  email varchar(50) DEFAULT NULL,
  full_name varchar(100) DEFAULT NULL,
  hashed_password varchar(100) DEFAULT NULL,
  disabled tinyint(1) DEFAULT NULL,
  is_superuser tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE vacancies (
  vacancy_id int(11) NOT NULL,
  title varchar(255) DEFAULT NULL,
  category varchar(20) NOT NULL,
  description text DEFAULT NULL,
  requirements text DEFAULT NULL,
  duration date DEFAULT NULL,
  how_to_apply text DEFAULT NULL,
  reference_number varchar(255) NOT NULL,
  created_date timestamp NOT NULL DEFAULT current_timestamp(),
  updated_date date DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  updated_by int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE vacancy_applications (
  vacancyApplication_id int(11) NOT NULL,
  vacancyApplication_category varchar(20) NOT NULL,
  vacancyApplicationCreated_date timestamp NOT NULL DEFAULT current_timestamp(),
  vacancyApplicationUpdated_date date DEFAULT NULL,
  vacancyApplicationCreated_by int(11) DEFAULT NULL,
  vacancyApplicationUpdated_by int(11) DEFAULT NULL,
  vacancy_id int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


ALTER TABLE branches
  ADD PRIMARY KEY (branch_id),
  ADD KEY ix_branches_branch_id (branch_id),
  ADD KEY fk_branch_created_by (branchCreated_by),
  ADD KEY fk_branch_updated_by (branchUpdated_by);


ALTER TABLE departments
  ADD PRIMARY KEY (department_id),
  ADD KEY ix_departments_department_id (department_id),
  ADD KEY fk_department_created_by (departmentCreated_by),
  ADD KEY fk_department_updated_by (departmentUpdated_by);


ALTER TABLE downloads
  ADD PRIMARY KEY (downloadFile_id),
  ADD UNIQUE KEY ix_downloads_downloadFile_name (downloadFile_name),
  ADD KEY ix_downloads_downloadFile_id (downloadFile_id);


ALTER TABLE events
  ADD PRIMARY KEY (event_id),
  ADD KEY ix_events_event_id (event_id),
  ADD KEY ix_events_event_description (event_description),
  ADD KEY ix_events_event_name (event_name);


ALTER TABLE faqs
  ADD PRIMARY KEY (id),
  ADD KEY fk_faq_created_by (created_by),
  ADD KEY fk_faq_updated_by (updated_by),
  ADD KEY fk_faqs_org (org_id);


ALTER TABLE files
  ADD PRIMARY KEY (file_id),
  ADD KEY ix_files_fileName (fileName),
  ADD KEY ix_files_filePath (filePath),
  ADD KEY ix_files_file_id (file_id),
  ADD KEY fk_files_created_by (fileCreated_by),
  ADD KEY fk_files_updated_by (fileUpdated_by),
  ADD KEY fk_files_vacancy (vacancyApplication_id),
  ADD KEY fk_files_tender (tender_id);


ALTER TABLE images
  ADD PRIMARY KEY (id),
  ADD KEY ix_images_title (title),
  ADD KEY ix_images_id (id),
  ADD KEY ix_images_filename (filename),
  ADD KEY fk_images_org (org_id);


ALTER TABLE latestnews
  ADD PRIMARY KEY (news_id),
  ADD KEY ix_latestnews_news_id (news_id),
  ADD KEY fk_news_created_by (newsCreated_by),
  ADD KEY fk_news_updated_by (newsUpdated_by);


ALTER TABLE messages
  ADD PRIMARY KEY (id),
  ADD KEY ix_messages_email (email),
  ADD KEY fk_messages_created_by (created_by),
  ADD KEY fk_messages_updated_by (updated_by),
  ADD KEY fk_messages_org (org_id);


ALTER TABLE orgs
  ADD PRIMARY KEY (id),
  ADD UNIQUE KEY org_uuid (org_uuid),
  ADD UNIQUE KEY name (name),
  ADD KEY fk_orgs_created_by (created_by),
  ADD KEY fk_orgs_updated_by (updated_by);


ALTER TABLE products
  ADD PRIMARY KEY (product_id),
  ADD KEY ix_products_product_id (product_id),
  ADD KEY fk_products_created_by (productCreated_by),
  ADD KEY fk_products_updated_by (productUpdated_by);


ALTER TABLE team_members
  ADD PRIMARY KEY (id),
  ADD UNIQUE KEY email (email),
  ADD KEY fk_team_created_by (created_by),
  ADD KEY fk_team_updated_by (updated_by),
  ADD KEY fk_team_members_org (org_id);


ALTER TABLE tenders
  ADD PRIMARY KEY (tender_id),
  ADD KEY ix_tenders_tender_id (tender_id),
  ADD KEY fk_tenders_created_by (tenderCreated_by),
  ADD KEY fk_tenders_updated_by (tenderUpdated_by);


ALTER TABLE users
  ADD PRIMARY KEY (id),
  ADD KEY ix_users_username (username),
  ADD KEY ix_users_email (email),
  ADD KEY ix_users_id (id);


ALTER TABLE vacancies
  ADD PRIMARY KEY (vacancy_id),
  ADD UNIQUE KEY reference_number (reference_number),
  ADD KEY ix_jobs_reference_number (reference_number),
  ADD KEY ix_vacancies_title (title),
  ADD KEY ix_vacancies_vacancy_id (vacancy_id),
  ADD KEY fk_vacancies_created_by (created_by),
  ADD KEY fk_vacancies_updated_by (updated_by);


ALTER TABLE vacancy_applications
  ADD PRIMARY KEY (vacancyApplication_id),
  ADD KEY vacancy_id (vacancy_id),
  ADD KEY ix_vacancy_applications_vacancyApplication_id (vacancyApplication_id);


ALTER TABLE branches
  MODIFY branch_id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE departments
  MODIFY department_id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE downloads
  MODIFY downloadFile_id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE events
  MODIFY event_id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE faqs
  MODIFY id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE files
  MODIFY file_id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE images
  MODIFY id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE latestnews
  MODIFY news_id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE messages
  MODIFY id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE orgs
  MODIFY id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE products
  MODIFY product_id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE team_members
  MODIFY id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE tenders
  MODIFY tender_id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE users
  MODIFY id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE vacancies
  MODIFY vacancy_id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE vacancy_applications
  MODIFY vacancyApplication_id int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE branches
  ADD CONSTRAINT fk_branch_created_by FOREIGN KEY (branchCreated_by) REFERENCES users (id),
  ADD CONSTRAINT fk_branch_updated_by FOREIGN KEY (branchUpdated_by) REFERENCES users (id);


ALTER TABLE departments
  ADD CONSTRAINT fk_department_created_by FOREIGN KEY (departmentCreated_by) REFERENCES users (id),
  ADD CONSTRAINT fk_department_updated_by FOREIGN KEY (departmentUpdated_by) REFERENCES users (id);


ALTER TABLE faqs
  ADD CONSTRAINT faqs_ibfk_1 FOREIGN KEY (org_id) REFERENCES orgs (id),
  ADD CONSTRAINT fk_faq_created_by FOREIGN KEY (created_by) REFERENCES users (id),
  ADD CONSTRAINT fk_faq_updated_by FOREIGN KEY (updated_by) REFERENCES users (id),
  ADD CONSTRAINT fk_faqs_org FOREIGN KEY (org_id) REFERENCES orgs (id);


ALTER TABLE files
  ADD CONSTRAINT files_ibfk_1 FOREIGN KEY (vacancyApplication_id) REFERENCES vacancy_applications (vacancyApplication_id),
  ADD CONSTRAINT files_ibfk_2 FOREIGN KEY (tender_id) REFERENCES tenders (tender_id),
  ADD CONSTRAINT fk_files_created_by FOREIGN KEY (fileCreated_by) REFERENCES users (id),
  ADD CONSTRAINT fk_files_tender FOREIGN KEY (tender_id) REFERENCES tenders (tender_id),
  ADD CONSTRAINT fk_files_updated_by FOREIGN KEY (fileUpdated_by) REFERENCES users (id),
  ADD CONSTRAINT fk_files_vacancy FOREIGN KEY (vacancyApplication_id) REFERENCES vacancies (vacancy_id);


ALTER TABLE images
  ADD CONSTRAINT fk_images_org FOREIGN KEY (org_id) REFERENCES orgs (id),
  ADD CONSTRAINT images_ibfk_1 FOREIGN KEY (org_id) REFERENCES orgs (id);


ALTER TABLE latestnews
  ADD CONSTRAINT fk_news_created_by FOREIGN KEY (newsCreated_by) REFERENCES users (id),
  ADD CONSTRAINT fk_news_updated_by FOREIGN KEY (newsUpdated_by) REFERENCES users (id);


ALTER TABLE messages
  ADD CONSTRAINT fk_messages_created_by FOREIGN KEY (created_by) REFERENCES users (id),
  ADD CONSTRAINT fk_messages_org FOREIGN KEY (org_id) REFERENCES orgs (id),
  ADD CONSTRAINT fk_messages_updated_by FOREIGN KEY (updated_by) REFERENCES users (id),
  ADD CONSTRAINT messages_ibfk_1 FOREIGN KEY (org_id) REFERENCES orgs (id);


ALTER TABLE orgs
  ADD CONSTRAINT fk_orgs_created_by FOREIGN KEY (created_by) REFERENCES users (id),
  ADD CONSTRAINT fk_orgs_updated_by FOREIGN KEY (updated_by) REFERENCES users (id);


ALTER TABLE products
  ADD CONSTRAINT fk_products_created_by FOREIGN KEY (productCreated_by) REFERENCES users (id),
  ADD CONSTRAINT fk_products_updated_by FOREIGN KEY (productUpdated_by) REFERENCES users (id);


ALTER TABLE team_members
  ADD CONSTRAINT fk_team_created_by FOREIGN KEY (created_by) REFERENCES users (id),
  ADD CONSTRAINT fk_team_members_org FOREIGN KEY (org_id) REFERENCES orgs (id),
  ADD CONSTRAINT fk_team_updated_by FOREIGN KEY (updated_by) REFERENCES users (id),
  ADD CONSTRAINT team_members_ibfk_1 FOREIGN KEY (org_id) REFERENCES orgs (id);


ALTER TABLE tenders
  ADD CONSTRAINT fk_tenders_created_by FOREIGN KEY (tenderCreated_by) REFERENCES users (id),
  ADD CONSTRAINT fk_tenders_updated_by FOREIGN KEY (tenderUpdated_by) REFERENCES users (id);

ALTER TABLE vacancies
  ADD CONSTRAINT fk_vacancies_created_by FOREIGN KEY (created_by) REFERENCES users (id),
  ADD CONSTRAINT fk_vacancies_updated_by FOREIGN KEY (updated_by) REFERENCES users (id);

ALTER TABLE vacancy_applications
  ADD CONSTRAINT vacancy_applications_ibfk_1 FOREIGN KEY (vacancy_id) REFERENCES vacancies (vacancy_id);
COMMIT;
