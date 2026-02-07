# 🐾 PetStore API Test Framework

Hey there! This is my take on building a robust, environment-agnostic testing suite for the PetStore API. I built this to demonstrate not just "passing tests," but how a real-world automation framework handles flaky environments, dynamic data, and CI/CD integration.

## 🛠 Why I Built It This Way

While the requirements mentioned a local mock, I wanted to ensure this framework was **production-ready**.

One of the coolest challenges I solved was **Environment Parity**. I noticed the local mock server uses plural endpoints (`/pets`), while the public Swagger production API uses singular endpoints (`/pet`). Instead of having two versions of the code, I built logic that automatically detects the `BASE_URL` and routes the requests correctly.

### Key Technical Highlights:

* **Self-Healing Data:** Rather than hardcoding IDs (which break when data is deleted), the schema tests dynamically "discover" a valid Pet ID from the API at runtime.
* **Thread-Safe Execution:** I implemented `threading.Lock()` to ensure that when tests run in parallel, they don't step on each other's toes when accessing shared setup data.
* **Crash-Proof Logging:** Public APIs often throw back HTML or XML error pages when they're grumpy. I built a safe JSON parser that validates the status code and content type before attempting to parse, preventing those annoying `JSONDecodeError` crashes.

---

## 🚀 Getting Started

### 1. Setup

First, grab the dependencies. I recommend using a virtual environment:

```bash
pip install -r requirements.txt

```

### 2. Environment Configuration

Create a `.env` file in the root directory. You can toggle between the recruiter's mock and the public API just by changing the URL:

```env
# For Local Mocking
BASE_URL=http://localhost:5000

# For Production Testing
# BASE_URL=https://petstore.swagger.io/v2

```

### 3. Running the Suite

To see the full "story" of the tests (including the live logs I set up for debugging), run:

```bash
pytest -s --log-cli-level=INFO

```

---

## 🏗 Framework Architecture

* **`api_helpers.py`**: The "engine room." It handles all HTTP verbs and contains the URL-joining logic that keeps the code clean.
* **`test_pet.py`**: Focuses on the Pet lifecycle, XSS injection resilience (negative testing), and schema validation.
* **`test_store.py`**: Handles order workflows. Note that I’ve accounted for the fact that the public API returns a `405` for `PATCH` requests, whereas the local mock supports them.
* **`schemas.py`**: Centralized JSON schemas for easy maintenance.

---

## 🤖 CI/CD Power

I've integrated **GitHub Actions** into this repo. Every time code is pushed, the suite runs against the public Swagger API. This provides a constant "health check" and ensures that new changes don't break existing functionality.

## 📝 Final Thoughts

This project was a great exercise in handling the "messiness" of real APIs—like singular/plural mismatches and unexpected 405 errors. It’s built to be readable, maintainable, and most importantly, reliable.

## 👨‍💻 Author

**Sri Purohith** [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/sri-p-9286925/)
*Last Updated: February 7, 2026*