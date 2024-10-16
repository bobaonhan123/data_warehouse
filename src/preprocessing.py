from datetime import datetime
from import_data import import_time
from .import_data import import_product
from .import_data import import_store
from .import_data import import_prod_in_store
from .import_data import import_sales_by_time
from .import_data import import_transaction


start_time = datetime.now()

import_time.import_time()
import_store.import_store()
import_product.import_product()
import_prod_in_store.import_prod_in_store()
import_sales_by_time.import_sales_by_time()
import_transaction.import_transaction()

time_taken = datetime.now() - start_time
print("Time taken: ", time_taken)