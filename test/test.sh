# POST Request with File Upload
curl -X POST "http://localhost:8000/jobs" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@./test/native.pdf;type=application/pdf"

curl -X POST "http://localhost:8000/jobs" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@./test/scan_default.pdf;type=application/pdf"

curl -X POST "http://localhost:8000/jobs" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@./test/scan_bad.pdf;type=application/pdf"