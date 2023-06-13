import uvicorn
from api import app

# Corre en http://127.0.0.1:8000 o http://0.0.0.0:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=7860)
