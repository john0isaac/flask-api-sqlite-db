GRANT ALL PRIVILEGES ON DATABASE testdb TO john;

-- TestCase
INSERT INTO `test_case` VALUES (1, 'First Test');
INSERT INTO `test_case` VALUES (2, 'Second Test');
INSERT INTO `test_case` VALUES (3, 'Third Test');

-- Asset
INSERT INTO `asset` VALUES (1, 'First Asset');
INSERT INTO `asset` VALUES (2, 'Second Asset');
INSERT INTO `asset` VALUES (3, 'Third Asset');

-- Execution
INSERT INTO `execution` VALUES (1, 1, 3, TRUE, 'Success');
INSERT INTO `execution` VALUES (2, 2, 2, FALSE, 'Failure');
INSERT INTO `execution` VALUES (3, 3, 1, FALSE, 'Failure');
INSERT INTO `execution` VALUES (4, 1, 3, TRUE, 'Success');
INSERT INTO `execution` VALUES (5, 2, 2, TRUE, 'Success');