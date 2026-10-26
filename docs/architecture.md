# UbuntuMed — System Architecture

## Overview

UbuntuMed is built using a modern, 3-tier architecture designed to separate the user interface, the business logic, and the AI models. This ensures the system is scalable, maintainable, and ready for cloud deployment.

## Architecture Diagram

```text
[ User's Web Browser ]
          |
          | HTTP Requests (HTML/JS)
          v
[ Frontend: Flask Application ] (Port 5000)
          |
          | REST API Calls (JSON)
          v
[ Backend: FastAPI Application ] (Port 8000)
   |          |           |
   v          v           v
[ CSV Data ] [ ML Models ] [ NLP Chatbot Model ]
 (Prototype  (Random Forest, (TF-IDF + Logistic
  Database)   Isolation Forest) Regression)
```
