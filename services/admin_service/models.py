# models.py

reservations = [
    {"id": 1, "name": "홍길동", "car_number": "12가 3456", "date": "2025-02-16", "time": "10:00 AM"},
    {"id": 2, "name": "김철수", "car_number": "45나 6789", "date": "2025-02-17", "time": "02:30 PM"},
    {"id": 3, "name": "이영희", "car_number": "78다 1234", "date": "2025-02-18", "time": "06:45 PM"},
]


parkinglots = [
    {"id": 1, "name": "A주차장", "latitude": 37.5123, "longitude": 127.0456, "type": "지상", "capacity": 100, "fee": True, "hours": "24시간"},
    {"id": 2, "name": "B주차장", "latitude": 37.5678, "longitude": 127.0987, "type": "지하", "capacity": 50, "fee": False, "hours": "07:00 - 22:00"},
    {"id": 3, "name": "C주차장", "latitude": 37.6234, "longitude": 127.1456, "type": "지상", "capacity": 80, "fee": True, "hours": "09:00 - 21:00"}
]