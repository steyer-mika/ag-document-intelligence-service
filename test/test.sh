# POST Request with File Upload
curl -X POST "http://localhost:8000/jobs" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@./native.pdf;type=application/pdf"

curl -X POST "http://localhost:8000/jobs" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@./scan_default.pdf;type=application/pdf"

curl -X POST "http://localhost:8000/jobs" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@./scan_bad.pdf;type=application/pdf"