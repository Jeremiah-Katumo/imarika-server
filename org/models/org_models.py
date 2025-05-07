from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, JSON, Text, DateTime, Index
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import uuid
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Org(Base):
    __tablename__ = "orgs"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    org_uuid = Column(String(255), unique=True, nullable=False, default=uuid.uuid4)
    about = Column(Text, nullable=True, default=None)
    location = Column(Text, nullable=True, default=None)
    contacts = Column(JSON, nullable=True, default=None)
    welcome_message = Column(Text, nullable=True, default=None)
    background = Column(Text, nullable=True, default=None)
    mission = Column(Text, nullable=True, default=None)
    vision = Column(Text, nullable=True, default=None)
    core_values = Column(JSON, nullable=True, default=None)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_date = Column(Date, nullable=True, default=None)
    created_by = Column(Integer, nullable=True, default=None)
    updated_by = Column(Integer, nullable=True, default=None)
    org_status = Column(String(10), default='active')

    messages = relationship("ContactMessage", back_populates="org")
    team_members = relationship("TeamMember", back_populates="team_org")
    faqs = relationship("Faq", back_populates="faq_org")
    images = relationship("Image", back_populates="image_org")


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    org_id = Column(Integer, ForeignKey("orgs.id"))
    profile_picture = Column(String(100), nullable=True, default=None)
    position = Column(String(100), nullable=True, default=None)
    social_media_links = Column(JSON, nullable=True, default=None)
    phone = Column(String(100), nullable=True, default=None)
    email = Column(String(100), unique=True)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_date = Column(Date, nullable=True, default=None)
    created_by = Column(Integer, nullable=True, default=None)
    updated_by = Column(Integer, nullable=True, default=None)

    team_org = relationship("Org", back_populates="team_members")

class Faq(Base):
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True)
    question = Column(String(100), nullable=False)
    answer = Column(String(200), nullable=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_date = Column(Date, nullable=True, default=None)
    created_by = Column(Integer, nullable=True, default=None)
    updated_by = Column(Integer, nullable=True, default=None)
    org_id = Column(Integer, ForeignKey("orgs.id"))
    
    faq_org = relationship("Org", back_populates="faqs")


class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    filename = Column(String(100), index=True)
    org_id = Column(Integer, ForeignKey("orgs.id"))

    image_org = relationship("Org", back_populates="images")


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), index=True)
    email = Column(String(50), index=True)
    full_name = Column(String(100))
    hashed_password = Column(String(100))
    disabled = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    # messages = relationship("ContactMessage", back_populates="user")


class Vacancy(Base):
    __tablename__ = "vacancies"

    vacancy_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    category = Column(String(20), nullable=False)
    description = Column(Text(3000))
    requirements = Column(Text(3000))
    duration = Column(Date, nullable=True, default=None)
    how_to_apply = Column(Text(300))
    reference_number = Column(String(255), nullable=False, unique=True)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_date = Column(Date, nullable=True, default=None)
    created_by = Column(Integer, nullable=True, default=None)
    updated_by = Column(Integer, nullable=True, default=None)

    vacancyApplication = relationship("VacancyApplication", back_populates="vacancy")
    
    __table_args__ = (
        Index('ix_jobs_reference_number', 'reference_number', mysql_length=255),
    )


# class Internship(Base):
#     __tablename__ = "internships"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255), index=True)
#     description = Column(Text(3000))
#     requirements = Column(Text(3000))
#     duration = Column(Date, nullable=True, default=None)
#     reference_number = Column(Text(20), unique=True, index=True)
#     how_to_apply = Column(Text(300))

#     internshipApplication = relationship("InternshipApplication", back_populates="internship")

#     __table_args__ = (
#         Index('ix_internships_reference_number', 'reference_number', mysql_length=255),
#     )


class VacancyApplication(Base):
    __tablename__ = "vacancy_applications"
    
    vacancyApplication_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    # vacancyApplication_status = Column(String(10), default="Pending")
    vacancyApplication_category = Column(String(20), nullable=False)
    vacancyApplicationCreated_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    vacancyApplicationUpdated_date = Column(Date, nullable=True, default=None)
    vacancyApplicationCreated_by = Column(Integer, nullable=True, default=None)
    vacancyApplicationUpdated_by = Column(Integer, nullable=True, default=None)
    vacancy_id = Column(Integer, ForeignKey("vacancies.vacancy_id"))

    vacancy = relationship("Vacancy", back_populates="vacancyApplication")
    vacancyApplication_files = relationship("File", back_populates="vacancyApplication")
    # jobApplication_user = relationship("User", back_populates="applications")


# class InternshipApplication(Base):
#     __tablename__ = "internship_applications"
    
#     internshipApplication_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
#     internshipApplication_status = Column(String(10), default="Pending")
#     internship_id = Column(Integer, ForeignKey("internships.id"))

#     internship = relationship("Internship", back_populates="internshipApplication")
#     internshipApplication_files = relationship("File", back_populates="internshipApplication")


class File(Base):
    __tablename__ = "files"
    
    file_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filePath = Column(String(255), index=True)
    fileName = Column(String(255), index=True)
    fileData = Column(LONGBLOB, nullable=False)
    fileCreated_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    fileUpdated_date = Column(Date, nullable=True, default=None)
    fileCreated_by = Column(Integer, nullable=True)
    fileUpdated_by = Column(Integer, nullable=True)
    vacancyApplication_id = Column(Integer, ForeignKey("vacancy_applications.vacancyApplication_id"))
    tender_id = Column(Integer, ForeignKey("tenders.tender_id"))
    
    vacancyApplication = relationship("VacancyApplication", back_populates="vacancyApplication_files")
    tenders = relationship("Tender", back_populates="tender_files")


class ContactMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    org_id = Column(Integer, ForeignKey("orgs.id"))
    email = Column(String(100), index=True)
    subject = Column(String(200))
    message = Column(Text)
    status = Column(String(10), default='new')
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_date = Column(Date, nullable=True, default=None)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    org = relationship("Org", back_populates="messages")
    # user = relationship("User", back_populates="messages")
    # writer = relationship("User", foreign_keys=[created_by], backref="writer_of_message")
    # updater = relationship("User", foreign_keys=[updated_by], backref="updater_of_message")
    

class Download(Base):
    __tablename__ = "downloads"

    downloadFile_id = Column(Integer, primary_key=True, index=True)
    downloadFile_title = Column(String(255), nullable=False) 
    downloadFile_name = Column(String(255), unique=True, index=True)
    downloadFile_category = Column(String(60), nullable=False, default=None)
    downloadFile_data = Column(LONGBLOB)
    downloadFileCreated_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    downloadFileUpdated_date = Column(Date, nullable=True, default=None)
    # downloadFileCreated_by = Column(Integer, nullable=True, default=None)
    # downloadFileUpdated_by = Column(Integer, nullable=True, default=None)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_title = Column(String(255), nullable=False)
    product_description = Column(String(255), nullable=False)
    product_image = Column(String(255), nullable=True, default=None)
    product_category = Column(String(100), nullable=False)
    productSub_category = Column(String(100), nullable=False)
    productCreated_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    productUpdated_date = Column(Date, nullable=True, default=None)
    productCreated_by = Column(Integer, nullable=True, default=None)
    productUpdated_by = Column(Integer, nullable=True, default=None)


class Branch(Base):
    __tablename__ = "branches"

    branch_id = Column(Integer, primary_key=True, index=True)
    branch_name = Column(String(60), nullable=False)
    branch_street = Column (String(100), nullable=False)
    branch_address = Column(Text(30), nullable=False)
    branch_email = Column(String(100), nullable=False)
    branch_phone = Column(String(100), nullable=True, default=None)
    branch_directions = Column(String(100), nullable=True, default=None)
    branchCreated_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    branchUpdated_date = Column(Date, nullable=True, default=None)
    branchCreated_by = Column(Integer, nullable=True, default=None)
    branchUpdated_by = Column(Integer, nullable=True, default=None)


class Tender(Base):
    __tablename__ = "tenders"

    tender_id = Column(Integer, primary_key=True, index=True)
    tender_title = Column(String(100), nullable=False)
    tenderCreated_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    tenderClosing_date = Column(Date, nullable=False)
    tenderUpdated_date = Column(Date, nullable=True, default=None)
    tenderCreated_by = Column(Integer, nullable=True, default=None)
    tenderUpdated_by = Column(Integer, nullable=True, default=None)

    tender_files = relationship("File", back_populates="tenders")


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    department_title = Column(String(100), nullable=False) 
    department_image = Column(String(100), nullable=True, default=None)
    departmentCreated_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    departmentUpdated_date = Column(Date, nullable=True, default=None)
    departmentCreated_by = Column(Integer, nullable=True, default=None)
    departmentUpdated_by = Column(Integer, nullable=True, default=None)


class LatestNews(Base):
    __tablename__ = "latestnews"

    news_id = Column(Integer, primary_key=True, index=True)
    news_heading = Column(String(255), nullable=False)
    news_info = Column(String(255), nullable=False)
    newsCreated_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    newsUpdated_date = Column(Date, nullable=True, default=None)
    newsCreated_by = Column(Integer, nullable=True, default=None)
    newsUpdated_by = Column(Integer, nullable=True, default=None)


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(100), index=True)
    event_date = Column(DateTime, default=datetime.utcnow)
    event_description = Column(String(100), index=True)