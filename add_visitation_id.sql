-- Add visitation_id column to visitors table
ALTER TABLE visitors ADD COLUMN visitation_id INT(11) DEFAULT NULL;

-- Add foreign key constraint
ALTER TABLE visitors ADD CONSTRAINT fk_visitors_visitation FOREIGN KEY (visitation_id) REFERENCES visitation_requests (id) ON DELETE SET NULL;

-- Add unique key if needed (though schema has it for vehicles, check if for visitors)
-- ALTER TABLE visitors ADD UNIQUE KEY unique_visitation_id (visitation_id);