CREATE TABLE IF NOT EXISTS accounting_subjects(
	subject_code VARCHAR(15),
	name VARCHAR(50) NOT NULL,
	superior_subject_code VARCHAR(15),
	type VARCHAR(10) NOT NULL,
	type_detail VARCHAR(10),
	PRIMARY KEY (subject_code),
	FOREIGN KEY (superior_subject_code) REFERENCES accounting_subjects(subject_code) ON DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS general_voucher (
    date DATE NOT NULL,
	record_date DATETIME NOT NULL DEFAULT NOW(),
	voucher_no VARCHAR(10),
	attachments_number TINYINT NOT NULL,
	checked TINYINT NOT NULL DEFAULT 0 CHECK ( checked in (0, 1) ),
	PRIMARY KEY (voucher_no)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS accounting_subjects_balance(
	time VARCHAR(6) NOT NULL,
	subject_code VARCHAR(15) NOT NULL,
	opening_balance DECIMAL(19, 4) NOT NULL,
	credit DECIMAL(19, 4) NOT NULL,
	debit DECIMAL(19, 4) NOT NULL,
	PRIMARY KEY (time, subject_code),
	FOREIGN KEY (subject_code) REFERENCES accounting_subjects(subject_code) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS voucher_entry (
	voucher_no VARCHAR(10) NOT NULL,
	abstract VARCHAR(50) NOT NULL,
	subject_code VARCHAR(15) NOT NULL,
	credit_debit VARCHAR(1) check ( credit_debit in ("借", "贷") ),
	total DECIMAL(19, 4) NOT NULL,
	FOREIGN KEY (voucher_no) REFERENCES general_voucher(voucher_no) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (subject_code) REFERENCES accounting_subjects(subject_code) ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS voucher_attachment (
	voucher_no VARCHAR(10) NOT NULL,
	attachment_url VARCHAR(100) NOT NULL,
	for_voucher TINYINT NOT NULL DEFAULT 0,
	FOREIGN KEY (voucher_no) REFERENCES general_voucher(voucher_no) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

