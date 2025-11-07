from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection

app = Flask(__name__)
app.secret_key = 'music_store_secret'

# Home
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- Customers ----------------
@app.route('/customers')
def customers():
    q = request.args.get('q','')
    conn = get_connection()
    with conn.cursor() as cur:
        if q:
            cur.execute("""
                SELECT * FROM customer 
                WHERE full_name LIKE CONCAT('%%', %s, '%%') 
                OR email LIKE CONCAT('%%', %s, '%%')
                ORDER BY customer_id DESC
            """, (q, q))
        else:
            cur.execute("SELECT * FROM customer ORDER BY customer_id DESC")
        rows = cur.fetchall()
    conn.close()
    return render_template('customers.html', customers=rows, q=q)

@app.route('/customers/add', methods=['POST'])
def add_customer():
    name = request.form.get('full_name')
    email = request.form.get('email')
    country = request.form.get('country')
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO customer (full_name, email, country) VALUES (%s,%s,%s)", (name,email,country))
        conn.commit()
    conn.close()
    flash('Customer added.')
    return redirect(url_for('customers'))

@app.route('/customers/edit/<int:id>', methods=['GET','POST'])
def edit_customer(id):
    conn = get_connection()
    if request.method=='POST':
        name = request.form.get('full_name'); email = request.form.get('email'); country = request.form.get('country')
        with conn.cursor() as cur:
            cur.execute("UPDATE customer SET full_name=%s, email=%s, country=%s WHERE customer_id=%s", (name,email,country,id))
            conn.commit()
        conn.close()
        flash('Customer updated.'); return redirect(url_for('customers'))
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM customer WHERE customer_id=%s", (id,))
        row = cur.fetchone()
    conn.close()
    return render_template('edit_customer.html', c=row)

@app.route('/customers/delete/<int:id>')
def delete_customer(id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM customer WHERE customer_id=%s", (id,))
        conn.commit()
    conn.close()
    flash('Customer deleted.')
    return redirect(url_for('customers'))

# ---------------- Artists ----------------
@app.route('/artists')
def artists():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM artist ORDER BY artist_id DESC")
        rows = cur.fetchall()
    conn.close()
    return render_template('artists.html', artists=rows)

@app.route('/artists/add', methods=['POST'])
def add_artist():
    name = request.form.get('name')
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO artist (name) VALUES (%s)", (name,))
        conn.commit()
    conn.close()
    flash('Artist added.')
    return redirect(url_for('artists'))

@app.route('/artists/delete/<int:id>')
def delete_artist(id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM artist WHERE artist_id=%s", (id,))
        conn.commit()
    conn.close()
    flash('Artist deleted.')
    return redirect(url_for('artists'))

# ---------------- Albums ----------------
@app.route('/albums')
def albums():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT album.album_id, album.title, artist.name as artist FROM album LEFT JOIN artist ON album.artist_id = artist.artist_id ORDER BY album.album_id DESC")
        rows = cur.fetchall()
        cur.execute("SELECT * FROM artist ORDER BY name")
        artists = cur.fetchall()
    conn.close()
    return render_template('albums.html', albums=rows, artists=artists)

@app.route('/albums/add', methods=['POST'])
def add_album():
    title = request.form.get('title'); artist_id = request.form.get('artist_id') or None
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO album (title, artist_id) VALUES (%s,%s)", (title, artist_id))
        conn.commit()
    conn.close()
    flash('Album added.')
    return redirect(url_for('albums'))

@app.route('/albums/delete/<int:id>')
def delete_album(id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM album WHERE album_id=%s", (id,))
        conn.commit()
    conn.close()
    flash('Album deleted.')
    return redirect(url_for('albums'))

# ---------------- Tracks ----------------
@app.route('/tracks', methods=['GET', 'POST'])
def tracks():
    conn = get_connection()
    with conn.cursor() as cur:
        # Handle adding new track
        if request.method == 'POST':
            title = request.form.get('title')
            album_id = request.form.get('album_id') or None
            price = request.form.get('unit_price') or 0
            stock = request.form.get('stock_quantity') or 0
            cur.execute(
                "INSERT INTO track (title, album_id, unit_price, stock_quantity) VALUES (%s,%s,%s,%s)",
                (title, album_id, price, stock)
            )
            conn.commit()
            flash("Track added successfully.")
            return redirect(url_for('tracks'))

        # Handle search query
        q = request.args.get('q', '')
        if q:
            cur.execute("""
                SELECT 
                    t.track_id, 
                    t.title, 
                    a.title AS album, 
                    t.unit_price, 
                    t.stock_quantity 
                FROM track t 
                LEFT JOIN album a ON t.album_id = a.album_id 
                WHERE t.title LIKE CONCAT('%%', %s, '%%') 
                ORDER BY t.track_id DESC
            """, (q,))
        else:
            cur.execute("""
                SELECT 
                    t.track_id, 
                    t.title, 
                    a.title AS album, 
                    t.unit_price, 
                    t.stock_quantity 
                FROM track t 
                LEFT JOIN album a ON t.album_id = a.album_id 
                ORDER BY t.track_id DESC
            """)
        tracks = cur.fetchall()

        # Fetch album list for dropdown
        cur.execute("SELECT * FROM album ORDER BY title")
        albums = cur.fetchall()
    conn.close()

    return render_template('tracks.html', tracks=tracks, albums=albums, q=q)


@app.route('/tracks/add', methods=['POST'])
def add_track():
    title = request.form.get('title'); album_id = request.form.get('album_id') or None
    price = request.form.get('unit_price') or 0; stock = request.form.get('stock_quantity') or 0
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO track (title, album_id, unit_price, stock_quantity) VALUES (%s,%s,%s,%s)", (title,album_id,price,stock))
        conn.commit()
    conn.close()
    flash('Track added.')
    return redirect(url_for('tracks'))

@app.route('/tracks/delete/<int:id>')
def delete_track(id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM track WHERE track_id=%s", (id,))
        conn.commit()
    conn.close()
    flash('Track deleted.')
    return redirect(url_for('tracks'))

@app.route('/tracks/edit/<int:id>', methods=['GET','POST'])
def edit_track(id):
    conn = get_connection()
    if request.method=='POST':
        title = request.form.get('title'); album_id = request.form.get('album_id') or None
        price = request.form.get('unit_price') or 0; stock = request.form.get('stock_quantity') or 0
        with conn.cursor() as cur:
            cur.execute("UPDATE track SET title=%s, album_id=%s, unit_price=%s, stock_quantity=%s WHERE track_id=%s", (title,album_id,price,stock,id))
            conn.commit()
        conn.close()
        flash('Track updated.'); return redirect(url_for('tracks'))
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM track WHERE track_id=%s", (id,))
        t = cur.fetchone()
        cur.execute("SELECT * FROM album ORDER BY title")
        albums = cur.fetchall()
    conn.close()
    return render_template('edit_track.html', t=t, albums=albums)

# ---------------- Orders ----------------
@app.route('/orders')
def orders():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT o.order_id, c.full_name, o.order_date, o.total_amount FROM orders o LEFT JOIN customer c ON o.customer_id = c.customer_id ORDER BY o.order_id DESC")
        rows = cur.fetchall()
    conn.close()
    return render_template('orders.html', orders=rows)

@app.route('/orders/new', methods=['GET','POST'])
def new_order():
    conn = get_connection()
    if request.method=='POST':
        cust_id = request.form.get('customer_id') or None
        items = []
        total = 0
        # gather quantities for each track field named qty_<track_id>
        with conn.cursor() as cur:
            # create order
            cur.execute("INSERT INTO orders (customer_id, total_amount) VALUES (%s, %s)", (cust_id, 0))
            order_id = cur.lastrowid
            # iterate all form keys for qty_
            for k, v in request.form.items():
                if k.startswith('qty_') and v and int(v) > 0:
                    track_id = int(k.split('_',1)[1])
                    qty = int(v)
                    cur.execute("SELECT unit_price, stock_quantity FROM track WHERE track_id=%s", (track_id,))
                    tr = cur.fetchone()
                    price = float(tr['unit_price'] or 0)
                    stock = int(tr['stock_quantity'] or 0)
                    if stock < qty:
                        # rollback and show message
                        conn.rollback()
                        flash(f'Not enough stock for track id {track_id} (available {stock}).')
                        return redirect(url_for('new_order'))
                    line = round(price * qty, 2)
                    total += line
                    cur.execute("INSERT INTO order_item (order_id, track_id, quantity, unit_price, line_total) VALUES (%s,%s,%s,%s,%s)", (order_id, track_id, qty, price, line))
                    # reduce stock
                    cur.execute("UPDATE track SET stock_quantity = stock_quantity - %s WHERE track_id=%s", (qty, track_id))
            # update total
            cur.execute("UPDATE orders SET total_amount=%s WHERE order_id=%s", (total, order_id))
            conn.commit()
        flash('Order created.')
        return redirect(url_for('orders'))
    # GET -> render form
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM customer ORDER BY full_name")
        customers = cur.fetchall()
        cur.execute("SELECT t.track_id, t.title, a.title as album, t.unit_price, t.stock_quantity FROM track t LEFT JOIN album a ON t.album_id = a.album_id ORDER BY t.title")
        tracks = cur.fetchall()
    conn.close()
    return render_template('new_order.html', customers=customers, tracks=tracks)

@app.route('/orders/delete/<int:id>')
def delete_order(id):
    conn = get_connection()
    with conn.cursor() as cur:
        # When order deleted, order_items cascade delete
        # restore stock quantities from order_items
        cur.execute("SELECT track_id, quantity FROM order_item WHERE order_id=%s", (id,))
        items = cur.fetchall()
        for it in items:
            cur.execute("UPDATE track SET stock_quantity = stock_quantity + %s WHERE track_id=%s", (it['quantity'], it['track_id']))
        cur.execute("DELETE FROM orders WHERE order_id=%s", (id,))
        conn.commit()
    conn.close()
    flash('Order deleted and stock restored.')
    return redirect(url_for('orders'))

@app.route('/invoice/<int:id>')
def invoice(id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT o.order_id, o.order_date, o.total_amount, c.full_name, c.email, c.country FROM orders o LEFT JOIN customer c ON o.customer_id = c.customer_id WHERE o.order_id=%s", (id,))
        order = cur.fetchone()
        cur.execute("SELECT oi.quantity, oi.unit_price, oi.line_total, t.title FROM order_item oi JOIN track t ON oi.track_id = t.track_id WHERE oi.order_id=%s", (id,))
        items = cur.fetchall()
    conn.close()
    return render_template('invoice.html', order=order, items=items)

# ---------------- Reports ----------------
@app.route('/reports')
def reports():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT DATE_FORMAT(order_date, '%%Y-%%m') AS month, SUM(total_amount) AS total_sales FROM orders GROUP BY month ORDER BY month DESC")
        monthly = cur.fetchall()
        cur.execute("SELECT t.title, SUM(oi.quantity) AS sold FROM order_item oi JOIN track t ON oi.track_id = t.track_id GROUP BY t.title ORDER BY sold DESC LIMIT 5")
        top_tracks = cur.fetchall()
        cur.execute("SELECT c.full_name, SUM(o.total_amount) AS spent FROM orders o JOIN customer c ON o.customer_id = c.customer_id GROUP BY c.full_name ORDER BY spent DESC LIMIT 5")
        top_customers = cur.fetchall()
    conn.close()
    return render_template('reports.html', monthly=monthly, top_tracks=top_tracks, top_customers=top_customers)

if __name__ == '__main__':
    app.run(debug=True)
