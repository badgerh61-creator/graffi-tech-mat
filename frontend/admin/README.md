Graffi Admin — Production static package

This archive contains:
- frontend-admin-src/ (source scaffold, Vite + React)
- frontend-admin-dist/ (prebuilt static site ready to serve)
- Dockerfile to serve the static site via nginx

To run the static admin locally with Docker:
1. docker build -t graffi-admin-static .
2. docker run -p 80:80 graffi-admin-static

Or place frontend-admin-dist contents into your backend's static folder (e.g., backend/frontend/admin/dist).
