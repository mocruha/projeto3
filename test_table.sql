-- Test table creation script
CREATE TABLE IF NOT EXISTS test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    value INTEGER
);

-- Insert some test data
INSERT INTO test_table (name, value) VALUES
    ('Test 1', 100),
    ('Test 2', 200),
    ('Test 3', 300);