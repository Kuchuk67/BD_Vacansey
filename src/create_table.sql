CREATE TABLE industries (
    industries_id character(10) PRIMARY KEY,
    industries_name varchar(255) NOT NULL
    );
CREATE TABLE company (
    company_id int PRIMARY KEY,
    name varchar(255) NOT NULL,
    site_url varchar(255),
    industries character(10),
    FOREIGN KEY (industries) REFERENCES industries(industries_id)
    );
CREATE TABLE vacancies (
    vacancies_id int PRIMARY KEY,
    vacancies_name varchar(255),
    salary_from int,
    salary_to int,
    salary_avg int,
    address varchar(255),
    snippet varchar(255),
    responsibility varchar(255),
    schedule varchar(80),
    company_id int REFERENCES company(company_id) NOT NULL
        );