ALTER TABLE visitors MODIFY COLUMN status ENUM('Expected','Inside','Exited','Cancelled') DEFAULT NULL;
