# BidMaster AI

A production-ready, AI-powered RFP bidding system built to predict proposal success and automate decision workflows for enterprise sponsors.

## Overview

BidMaster AI fuses classical machine learning and cutting-edge LLMs with Retrieval-Augmented Generation (RAG) to tackle class imbalance in RFP datasets. It achieves 67% weighted accuracy while integrating seamlessly into business pipelines.

## Features

* Predicts bid outcomes using Random Forest, Naive Bayes, and LLM-based pipelines.
* REST APIs built with Flask and FastAPI for real-time deployment.
* Automated SMS/email notifications via Twilio and Gmail SMTP.
* Dockerized for scalable and reproducible deployment.

## Tech Stack

* Python, Pandas, NumPy, Scikit-learn, XGBoost
* LLMs (OpenAI API), RAG architecture
* Flask, FastAPI, Twilio, Gmail SMTP
* Docker

## Usage

```bash
docker build -t bidmaster .
docker run -p 5000:5000 bidmaster
```

