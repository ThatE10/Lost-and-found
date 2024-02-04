import concurrent.futures

import uvicorn

from ml_model.classification import app, ml_core
from routing.main import app as form_app

classify = ''

def run_form_routes():
    uvicorn.run(form_app, port=8000)

if __name__ == "__main__":
    global classify
    ml_core = ml_core(run_local=True,classification_API='')
    predict = ml_core.classify
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(ml_core.start_server)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future2 = executor.submit(run_form_routes)

            print('this is horrid')

