from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'super_secret_bus_key'

# In-memory database: 10 seats initially available
bus_seats = {f"Seat {i}": "Available" for i in range(1, 11)}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bus Booking System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #333; }
        .seat-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
        .seat { padding: 15px; text-align: center; border: 1px solid #ccc; border-radius: 4px; font-weight: bold; }
        .Available { background-color: #d4edda; color: #155724; }
        .Booked { background-color: #f8d7da; color: #721c24; }
        select, button { width: 100%; padding: 10px; margin-top: 10px; font-size: 16px; }
        button { background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .message { padding: 10px; margin-bottom: 15px; border-radius: 4px; text-align: center; background-color: #e2e3e5; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚌 Bus Seat Booking</h2>
        
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="message">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <div class="seat-grid">
            {% for seat, status in seats.items() %}
                <div class="seat {{ status }}">{{ seat }}<br>({{ status }})</div>
            {% endfor %}
        </div>

        <form action="/book" method="POST">
            <label for="seat">Choose an available seat:</label>
            <select name="seat_id" id="seat">
                {% for seat, status in seats.items() %}
                    {% if status == 'Available' %}
                        <option value="{{ seat }}">{{ seat }}</option>
                    {% endif %}
                {% endfor %}
            </select>
            <button type="submit">Book Seat</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, seats=bus_seats)

@app.route('/book', edit_request_methods=['POST'], methods=['POST'])
def book_seat():
    seat_id = request.form.get('seat_id')
    if seat_id in bus_seats and bus_seats[seat_id] == "Available":
        bus_seats[seat_id] = "Booked"
        flash(f"Successfully booked {seat_id}!")
    else:
        flash("Seat unavailable or invalid selection.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
