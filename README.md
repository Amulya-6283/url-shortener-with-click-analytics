# 🔗 URL Shortener with Click Analytics (Serverless)

A lightweight **Bitly-style URL shortener** built using **AWS Serverless architecture**.  
The application allows users to generate short URLs, redirect users to the original URL, and track basic click analytics through an admin dashboard.

---

## 🚀 Live Architecture Overview

**Frontend**
- Static website hosted on **Amazon S3**
- HTML, CSS, JavaScript (responsive UI)

**Backend**
- **API Gateway (HTTP API)**
- **AWS Lambda (Python)**
- **Amazon DynamoDB** for storage

**Observability**
- **Amazon CloudWatch Logs**

---

## 🧩 Features

### 🔹 User Features
- Generate short URLs from long URLs
- Share short links publicly
- Automatic redirection to the original URL

### 🔹 Analytics
- Track click count per short URL
- Store creation time and last accessed time

### 🔹 Admin Features
- View all shortened links
- Monitor click counts and recent activity

---

## DynamoDB Schema
**Table:** `links`

| Attribute       | Description |
|-----------------|-------------|
| `code` (PK)     | Short URL identifier |
| `target_url`    | Original long URL |
| `created_at`    | Creation timestamp |
| `click_count`   | Number of redirects |
| `last_accessed` | Last access timestamp |

---

## API Endpoints
- **POST `/links`** → Create a short URL  
- **GET `/{code}`** → Redirect to original URL + increment click count  
- **GET `/admin/links`** → List all links with analytics  

Example short link:
https://<api-id>.execute-api.us-east-1.amazonaws.com/abc123

---

## Deployment
- Frontend deployed on **Amazon S3**
- Backend deployed using **AWS Lambda**
- APIs exposed via **API Gateway**
- Data stored in **DynamoDB**

---

## Security & IAM
- Public access only for redirect endpoint
- Admin routes protected via IAM
- Least-privilege IAM policies applied

---

## Learnings
- Designed a complete serverless architecture
- Built REST APIs using Lambda and API Gateway
- Implemented DynamoDB data modeling
- Gained hands-on experience with AWS observability
