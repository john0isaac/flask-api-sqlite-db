-- TestCase
INSERT INTO `test_case` VALUES (1, 'First Test', 'First Test Description');
INSERT INTO `test_case` VALUES (2, 'Second Test', NULL);
INSERT INTO `test_case` VALUES (3, 'Third Test', 'Third Test Description');

-- Asset
INSERT INTO `asset` VALUES (1, 'First Asset');
INSERT INTO `asset` VALUES (2, 'Second Asset');
INSERT INTO `asset` VALUES (3, 'Third Asset');

-- Execution
INSERT INTO `execution` (id, test_case_id, asset_id, status, details, timestamp) VALUES (1, 1, 3, TRUE, 'Success', '2024-02-28 14:35:30.333333');
INSERT INTO `execution` (id, test_case_id, asset_id, status, details, timestamp) VALUES (2, 3, 1, FALSE, 'Failure', '2024-02-29 15:35:30.333333');
INSERT INTO `execution` (id, test_case_id, asset_id, status, details, timestamp) VALUES (3, 2, 1, FALSE, 'Failure', '2024-03-01 16:35:30.333333');
INSERT INTO `execution` (id, test_case_id, asset_id, status, details, timestamp) VALUES (4, 1, 2, TRUE, 'Success', '2024-03-02 17:35:30.333333');
INSERT INTO `execution` (id, test_case_id, asset_id, status, details, timestamp) VALUES (5, 3, 2, TRUE, 'Success', '2024-03-03 18:35:30.333333');