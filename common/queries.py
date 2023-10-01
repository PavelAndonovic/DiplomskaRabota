GET_ALL_TABLE_NAMES = "SELECT name FROM sqlite_master WHERE type='table'"

GET_SAMPLE_DATA_FROM_TABLE = "select * from {table_name} limit {row_limit}"