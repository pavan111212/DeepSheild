from fastapi import FastAPI

app = FastAPI()

# Root route
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

# Health check route
@app.get("/health")
def health():
    return {"status": "ok"}

# 👉 Keep your existing routes below this line
# Example:
# @app.post("/predict")
# def predict(data: InputData):
#     # your ML logic here
#     return {"result": "something"}
