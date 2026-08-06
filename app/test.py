from app.services.booking_service import extract_booking

print(
    extract_booking(
        "Book an interview for tomorrow at 3 PM. My name is Subash. Email is subash@gmail.com."
    )
)