LOCK_TABLES = "LOCK TABLE info, ids IN ACCESS EXCLUSIVE MODE;"

CHECK_STOCK = "SELECT stock->'reserved' FROM info;"
CHECK_ID = "SELECT * FROM ids WHERE order_id = (%s);"
CHECK_USER = """SELECT * FROM ids WHERE number = (%s);"""

INSERT_ID = "INSERT INTO ids VALUES (%s, %s);"
UPDATE_STOCK = "UPDATE info SET stock = stock || hstore('reserved', (%s));"
