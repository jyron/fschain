from fastapi import FastAPI
import pandas as pd
import uvicorn

app = FastAPI()


@app.get("/index/f/{ticker}")
def get_index_score(ticker: str):
    df = pd.read_csv("data/company_financial_indexes.csv")
    df = df[df["ticker"] == ticker.upper()]
    return df.to_dict(orient="records")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)